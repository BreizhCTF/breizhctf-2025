import os

os.environ.setdefault("TERM", "linux")
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from Crypto.Util.number import long_to_bytes
import time
from Crypto.Protocol.SecretSharing import Shamir
from datetime import datetime
from sage.all import (
    PolynomialRing,
    Zmod,
    Sequence,
    vector,
    prod,
    polygens,
    power,
    Polynomial,
    ZZ,
    QQ,
)
from random import randrange
import itertools


def small_roots(f, bounds, m=1, d=None):
    if not d:
        d = f.degree()

    if isinstance(f, Polynomial):
        (x,) = polygens(f.base_ring(), f.variable_name(), 1)
        f = f(x)

    R = f.base_ring()
    N = R.cardinality()

    # f /= f.coefficients().pop(0)
    leading = 1 / f.coefficients().pop(0)
    f = f.map_coefficients(lambda x: x * leading)
    f = f.change_ring(ZZ)

    G = Sequence([], f.parent())
    for i in range(m + 1):
        base = N ** (m - i) * f**i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)

    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)

    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)
    B = B.dense_matrix().LLL()

    B = B.change_ring(QQ)

    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)
    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B * monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots

    return []


def aes_decrypt(key, ciphertext):
    iv = bytes.fromhex(ciphertext[:32])
    ciphertext = bytes.fromhex(ciphertext[32:])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


def combine_shares(shares):
    key = Shamir.combine(shares)
    return key


if len(sys.argv) < 3:
    print("Usage solve.py <host> <port> [DEBUG]")
    exit(1)

_, host, port = sys.argv

r = remote(host, int(port))

# Get ciphertext
print(r.recvuntil(b"e : ").decode())
ciphertext = bytes.fromhex(r.recvuntil(b"\n").strip().decode())
print(ciphertext.hex())

# get share1, share2, share3
print(r.recvuntil(b"Time) : ").decode())
share_agent1 = bytes.fromhex(r.recvuntil(b"\n").strip().decode())
print(share_agent1.hex())
print(r.recvuntil(b"Time) : ").decode())
share_agent2 = bytes.fromhex(r.recvuntil(b"\n").strip().decode())
print(share_agent2.hex())
print(r.recvuntil(b"Time) : ").decode())
share_agent3 = bytes.fromhex(r.recvuntil(b"\n").strip().decode())
print(share_agent3.hex())
print(r.recvuntil(b"Quitter\n").decode())


def get_current_secret(agent_nb):
    r.sendline(str(agent_nb).encode())

    r.recvuntil(b"le : ")
    date = int(
        datetime.strptime(
            r.recvuntil(b"\n").strip().decode(), "%Y-%m-%d %H:%M:%S"
        ).timestamp()
    )
    r.recvuntil(b" : ")
    secret = int(r.recvuntil(b"\n").strip().decode())

    return secret, date


# get current secret 1, 2, 3
print("Récupération des secrets des 3 agents 1/3")
secret_agent_1_1, date_1_1 = get_current_secret(1)
secret_agent_2_1, date_2_1 = get_current_secret(2)
secret_agent_3_1, date_3_1 = get_current_secret(3)

# wait 1 minute
time.sleep(10)
# get current secret 1, 2, 3
print("Récupération des secrets des 3 agents 2/3")
secret_agent_1_2, date_1_2 = get_current_secret(1)
secret_agent_2_2, date_2_2 = get_current_secret(2)
secret_agent_3_2, date_3_2 = get_current_secret(3)

# wait 1 minute
time.sleep(10)
# get current secret 1, 2, 3
print("Récupération des secrets des 3 agents 3/3")
secret_agent_1_3, date_1_3 = get_current_secret(1)
secret_agent_2_3, date_2_3 = get_current_secret(2)
secret_agent_3_3, date_3_3 = get_current_secret(3)


# with r1_0, r1_1, r1_2 : recover parameter v1, and z to emulate the sequence generation
def generate_sequence(seed, z, length):
    sequence = []
    n = 128
    value = seed
    for _ in range(length):
        value = value * z % 2**n
        sequence.append(value >> 18)
    return sequence


def attack(h0, h1, h2):
    # load('coppersmith.sage')
    bounds = (2**18, 2**18, 2**18)

    roots = tuple(randrange(bound) for bound in bounds)

    n = 128
    Zmodn = Zmod(2**n)
    P = PolynomialRing(Zmodn, names=("y0", "y1", "y2"))  # Define the ring
    y0, y1, y2 = P.gens()

    H0 = Zmodn(h0 * 2**18)
    H1 = Zmodn(h1 * 2**18)
    H2 = Zmodn(h2 * 2**18)

    f = y1 * y1 - y0 * y2 + 2 * H1 * y1 - H0 * y2 - H2 * y0 + H1 * H1 - H0 * H2
    for m in (1, 2, 3, 4):
        for d in (1, 2):
            roots = small_roots(f, bounds, m, d)
            if len(roots) > 0:
                break

    d0, d1, d2 = roots[0]
    v0, v1, v2 = H0 + d0, H1 + d1, H2 + d2

    try:
        z = v1 * pow(v0, -1, 2**128) % 2**128
    except:
        try:
            z = v2 * pow(v1, -1, 2**128) % 2**128
        except:
            print("Inverse error")
            z = None

    return z, v0


# get secret time locked
# recover shares 1 with the secret time locked as key
t = 1742079600

convert_int_bytes = lambda secret, t: pad(long_to_bytes(int(secret[t])), 16)


# number of minutes between our dates and the locked_time
z_1, seed_1 = attack(secret_agent_1_1, secret_agent_1_2, secret_agent_1_3)
length_needed = int((1742076000 - date_1_1) / 10)

if z_1:
    print("PRNG 1 cassé")
    sequence_agent_1 = generate_sequence(seed_1, z_1, length_needed)
    y1 = aes_decrypt(convert_int_bytes(sequence_agent_1, -1), share_agent1.hex())
    print("Share 1 retrouvé")
else:
    y1 = None

z_2, seed_2 = attack(secret_agent_2_1, secret_agent_2_2, secret_agent_2_3)
if z_2:
    print("PRNG 2 cassé")
    sequence_agent_2 = generate_sequence(seed_2, z_2, length_needed)
    y2 = aes_decrypt(convert_int_bytes(sequence_agent_2, -1), share_agent2.hex())
    print("Share 2 retrouvé")
else:
    y2 = None

if not (z_1 and z_2):
    z_3, seed_3 = attack(secret_agent_3_1, secret_agent_3_2, secret_agent_3_3)
    if z_3:
        print("PRNG 3 cassé")
        sequence_agent_3 = generate_sequence(seed_3, z_3, length_needed)
        y3 = aes_decrypt(convert_int_bytes(sequence_agent_3, -1), share_agent3.hex())
        print("Share 3 retrouvé")
    else:
        y3 = None
else:
    y3 = None

# Combine shares with shamir
shares = [(i + 1, y[:16]) for i, y in enumerate((y1, y2, y3)) if y != None]

key = combine_shares(shares)

# Decrypt AES
flag = aes_decrypt(key, ciphertext.hex())
print(f"FLAG : {unpad(flag,16).decode()}")
