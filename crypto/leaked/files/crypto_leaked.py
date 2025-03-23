import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secret import FLAG


class EllipticCurve:
    def __init__(self, a, b, p, G, n):
        self.a = a  # Curve coefficient a
        self.b = b  # Curve coefficient b
        self.p = p  # Prime modulus
        self.G = G  # Base point (generator)
        self.n = n  # Order of the base point

    def is_on_curve(self, P):
        if P is None:
            return True
        x, y = P
        return (y**2 - x**3 - self.a * x - self.b) % self.p == 0

    def point_add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        if P == Q:
            return self.point_double(P)

        if x1 == x2 and y1 != y2:
            return None

        m = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        x3 = (m**2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def point_double(self, P):
        if P is None:
            return None

        x, y = P

        if y == 0:
            return None

        m = ((3 * x**2 + self.a) * pow(2 * y, -1, self.p)) % self.p
        x3 = (m**2 - 2 * x) % self.p
        y3 = (m * (x - x3) - y) % self.p

        return (x3, y3)

    def scalar_mult(self, k, P):
        R = None
        Q = P

        while k:
            if k & 1:
                R = self.point_add(R, Q)
            Q = self.point_double(Q)
            k >>= 1

        return R

    def generate_keypair(self):
        private_key = random.randint(1, self.n - 1)
        public_key = self.scalar_mult(private_key, self.G)
        return private_key, public_key

    def encrypt_message(self, message, private_key):
        key = hashlib.sha256(str(private_key).encode()).digest()
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return iv + ciphertext

    def decrypt_message(self, encrypted_message, private_key):
        key = hashlib.sha256(str(private_key).encode()).digest()
        iv = encrypted_message[:16]
        ciphertext = encrypted_message[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()


# secp256k1 parameters
a = 0
b = 7
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (
    55066263022277343669578718895168534326250603453777594175500187360389116729240,
    32670510020758816978083085130507043184471273380659243275938904335757337482424,
)
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

curve = EllipticCurve(a, b, p, G, n)

# Generate a keypair
private_key, public_key = curve.generate_keypair()
print("Public Key:", public_key)

# Encrypt and decrypt a message
encrypted = curve.encrypt_message(FLAG, private_key)
print("Encrypted:", encrypted.hex())

"""
Public Key: (70511256471380151994507020859017662796463915663104143313762476537493175101944, 101377985350777571501295413323425826317536381509542380876760459710190189823343)
Encrypted: 85df4965181aeec6cacf3c023d5be68f29854924f4aa39bf9731ecf33872d32cfaf4c4af7daee0e31ea5faa47c8848f91a8707bb7f0db4ed118d98f07a0434344d435edd1000fc901848147d5cc9106b
"""
