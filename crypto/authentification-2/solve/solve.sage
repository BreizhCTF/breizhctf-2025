# Testé avec Sage 10.5
import os
os.environ.setdefault("TERM", "xterm-256color")

from pwn import xor
from json import dumps
import requests
load("gf.sage")

# 0. Récupération de {HOST,PORT} depuis argv
from sys import argv
if len(argv) != 2:
    print("usage: `sage solve.sage <URL>`")
    exit()

URL = argv[1]

# 1. Récupération d'un ct avec clair connu
def build_pt(username, role="guest"):
    return dumps({
        "username": username,
        "role": role
    })

# On prend un pt de taille | 16 pour ne pas s'embêter avec du padding
# le JSON sera de taille 33+len(username), on choisit donc un username
# de taille 143 pour être bon
username = "skilo" + "o"*(143 - len("skilo"))
pt = build_pt(username)

# Je mets un `while True` car je relance jusqu'à avoir une
# racine unique (plus simple que de toutes les tester)
while True:
    # On reset la db
    url = f'{URL}/reset-db'
    _ = requests.get(url)

    # Register
    url = f'{URL}/register'
    headers = { 'User-Agent': 'solve-script' }
    data = {"username": username, "password": "a"}
    _ = requests.post(url, headers=headers, data=data, allow_redirects=False)

    # Login to get token
    url = f'{URL}/login'
    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
    token = response.cookies["auth"].replace("\\073", ";").strip('"')
    ct, tag = map(bytes.fromhex, token.split(";"))

    # 2. On peut maintenant récup le keystream...
    keystream = xor(ct, pt.encode())

    # ...et forger le payload désiré (de len <= ct ET de len | 16)
    target_pt = build_pt("skilooooo", "super_admin")
    forged_ct = xor(target_pt.encode(), keystream[:len(target_pt)])

    # 3. Forgeons maintenant le tag, on sait que :
    # Avec C le ciphertext et A les AAD (les deux de la taille d'un bloc)
    # Posons lC = bitlen(C) ; lA = bitlen(A) ; paddé en big endian sur 8 octets
    # T = X + (A*H^3 + C*H^2 + (lA||lC)*H^1)
    # Grâce à l'erreur d'implem => X est = keystream[:16]
    # 1 eqn 1 inconnu => facile mais car degree != 1 on n'aura pas forcément une solution unique.
    lA = b"\x00"*8
    lC = (int(len(ct)*8)).to_bytes(8, "big")
    X = bytes_to_gf(keystream[:16])
    Cs = [ct[i:i+16] for i in range(0, len(ct), 16)]
    Cs = [bytes_to_gf(c) for c in Cs]

    R.<H> = PolynomialRing(Fp)
    # C'est ici que le fait d'avoir len(C) | 16 aide
    f = sum(Cs[i]*H**(len(Cs) - i + 1) for i in range(len(Cs)))
    l = bytes_to_gf(lA+lC)
    T = X + (f + l*H)
    T = bytes_to_gf(tag) - T
    I = Ideal(T)
    G = I.groebner_basis()

    racines = G[0].roots()
    print("nb racine =", len(racines))

    if len(racines) != 1:
        continue

    H = racines[0][0]

    # On build T pour notre `forged_ct`
    lA = b"\x00"*8
    lC = (int(len(forged_ct)*8)).to_bytes(8, "big")
    forged_Cs = [forged_ct[i:i+16] for i in range(0, len(forged_ct), 16)]
    forged_Cs = [bytes_to_gf(c) for c in forged_Cs]

    f = sum(forged_Cs[i]*H**(len(forged_Cs) - i + 1) for i in range(len(forged_Cs)))
    l = bytes_to_gf(lA+lC)
    T = X + (f + l*H)

    forged_tag = gf_to_bytes(T)
    token = forged_ct.hex() + ";" + forged_tag.hex()

    session = requests.Session()
    token = '"' + token.replace(";", "\\073") + '"'
    session.cookies.set("auth", token)
    url = f'{URL}/admin'
    response = session.get(url, headers=headers)
    flag = 'BZHCTF' + response.text.split("BZHCTF")[1].split("}")[0] + "}"
    print(f"{flag = }")
    break

