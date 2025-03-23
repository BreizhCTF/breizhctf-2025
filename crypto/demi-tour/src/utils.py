from Crypto.Util.Padding import pad
from ast import literal_eval

BLOCK_LEN = 16

# bytes to quinary 
def btq(a: bytes):
    a = sum(ai*256**i for i,ai in enumerate(a))

    charset = [-2, -1, 0, 1, 2]
    res = []
    
    while a > 0:
        res.append(charset[a % len(charset)])
        a //= len(charset)

    return res

def xor(a: bytes, b: bytes):
    assert len(a) == len(b)

    return bytes(
        [aa^bb for (aa,bb) in zip (a, b)]
    )

def sanitize(a: bytes, l: int):
    a = pad(a, BLOCK_LEN)
    out = b"\x00"*BLOCK_LEN

    for i in range(0, len(a), BLOCK_LEN):
        out = xor(out, a[i:i+BLOCK_LEN])

    return btq(out)[:l]

"""
Matrice générée avec la fonction : `random_matrix(Zn, k, l)`
            => R.A.S avec cette matrice
J'ai préféré la partager sous forme de fichier texte plutot que de donner la seed
pour éviter des problèmes d'intéropérabilités - entre les différentes versions
de SageMath - au niveau des fonctions `random_element`/`random_matrix`.
"""
def get_a():
    f = open("A.txt", "r")
    A = f.read() ; f.close()

    return literal_eval(A)

