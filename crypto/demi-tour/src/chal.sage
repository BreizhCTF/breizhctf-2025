from utils import sanitize, get_a
from os import getenv
from re import match

FLAG = getenv("FLAG", "BZHCTF{0000000000000000}")
assert bool(match(r'^BZHCTF\{[0-9a-f]+\}$', FLAG))

FLAG = FLAG.strip("BZHCTF{}")
assert len(FLAG) == 16

k, l = 48, 50
n = 256
Zn = Zmod(n)

def hash(msg: str):
    msg = msg.encode()
    msg = sanitize(msg, l)

    x = vector(Zn, msg)
    A = Matrix(Zn, k, l, get_a())

    return bytes(A*x)

h = hash(FLAG)
print(h.hex())

