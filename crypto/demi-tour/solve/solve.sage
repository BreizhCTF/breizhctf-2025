# Récuperation de la location des fichiers :
#   - output.txt
#   - A.txt

from sys import argv
if len(argv) != 3:
    print("usage : sage solve.sage <OUTPUT_PATH> <A_PATH>")

f = open(argv[1], "r")
a_path = argv[2]

# Début solve
from itertools import product
from utils import get_a
from re import match

k, l = 48, 50
n = 256
Zn = Zmod(n)
beta = 2

# Récupération de la matrice publique
A = Matrix(Zn, k, l, get_a(a_path))

# Récupération du hash
h = f.read().strip()
h = list(bytes.fromhex(h))
f.close()

# Pre-image le truc
y = Matrix(ZZ, h).T
A = A.lift()
M = block_matrix(1, 3, [A, -y, identity_matrix(k)*n])
kerM = M.right_kernel().matrix()
llled = kerM.LLL()

re_msg = None
for i,r in enumerate(llled.rows()):
    r = r[:l]

    if all([x in range(-beta, beta+1) for x in r]):
        re_msg = list(r)
   
# B5 to bytes
def qtb(a: list[int]):
    # Expand base 5
    a = sum((ai+beta)*5**i for i,ai in enumerate(a))

    # Convert to base 256
    res = []
    
    while a > 0:
        res.append(a % 256)
        a //= 256

    return bytes(res)

def xor(a: bytes, b: bytes):
    assert len(a) == len(b)
    return bytes([aa^^bb for aa,bb in zip(a, b)])

# Il faut bf car on connait pas la len de l'output de 'btq'
len_min = 50
for offset in range(0, 7):
    for sign in [1, -1]:
        for p in product(range(-beta, beta+1), repeat=((len_min+offset)-len_min)):
            cur_vec = [r*sign for r in re_msg] + list(p)
            cur_msg = qtb(cur_vec)
            
            if len(cur_msg) != 16:
                continue

            try:
                cur_msg = xor(cur_msg, b"\x10"*16)
                cur_msg = cur_msg.decode()
                res = bool(match(r'^[0-9a-f]+$', cur_msg))
                if res:
                    print("BZHCTF{" + cur_msg + "}")
                    exit()

            except UnicodeDecodeError as _:
                pass

