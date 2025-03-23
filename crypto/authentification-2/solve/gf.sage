P.<x> = PolynomialRing(GF(2))
f = x**128 + x**7 + x**2 + x + 1
Fp.<a> = GF(2**128, modulus=f)

def bytes_to_gf(b):
    b_as_bits = "".join(bin(bb)[2:].zfill(8) for bb in b)
    b_as_bits = [int(bb) for bb in b_as_bits]

    return Fp(b_as_bits)

def gf_to_bytes(g):
    assert len(list(g)) == 128
    g = [str(a) for a in list(g)]
    g = ["".join(g[i:i+8]) for i in range(0, len(list(g)), 8)]

    return bytes([int(a, 2) for a in g])


