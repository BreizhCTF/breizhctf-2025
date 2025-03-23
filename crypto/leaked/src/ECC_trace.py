import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import numpy as np
import matplotlib.pyplot as plt
from secret import FLAG

# Simulating power trace (with more noise and points per operation)
def simulate_power_trace(trace, points_per_operation=300):
    time_steps = trace.count("Add") * 200 + trace.count("Double") * 300 + len(trace) * 100  # More time steps due to multiple points per operation
    power_trace = np.zeros(time_steps)
    index = 0
    # Simulating power consumption based on the operations
    for i, operation in enumerate(trace):
        # For each operation, simulate multiple time steps
        if operation == "Add" :
            number = 200
        else:
            number = 300
        for j in range(number):
            if operation == "Add":
                power_trace[index] = np.random.normal(3.5, 2.5)  # Higher power for addition
            elif operation == "Double":
                power_trace[index] = np.random.normal(2.3, 1.7)  # Lower power for doubling
            index += 1  # Calculate time step index
        for j in range(100):
            power_trace[index] = np.random.normal(-0.2, 0.7)
            index += 1
    # Add significant random noise to make it more realistic
    noise = np.random.normal(-0.3, 0.3, time_steps)  # Larger noise to simulate real-world conditions
    power_trace += noise

    # Clip values to avoid extreme outliers
    power_trace = np.clip(power_trace, -17, 17)

    return power_trace

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
        return (y ** 2 - x ** 3 - self.a * x - self.b) % self.p == 0

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
        x3 = (m ** 2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        
        return (x3, y3)

    def point_double(self, P):
        if P is None:
            return None
        
        x, y = P
        
        if y == 0:
            return None
        
        m = ((3 * x ** 2 + self.a) * pow(2 * y, -1, self.p)) % self.p
        x3 = (m ** 2 - 2 * x) % self.p
        y3 = (m * (x - x3) - y) % self.p
        
        return (x3, y3)

    def scalar_mult(self, k, P):
        R = None
        Q = P

        power_trace = [] 
        
        while k:
            Q = self.point_double(Q)
            power_trace.append("Double")
            if k & 1:
                R = self.point_add(R, Q)
                power_trace.append("Add")
            k >>= 1
        
        return R, power_trace

    def generate_keypair(self):
        private_key = random.randint(1, self.n - 1)
        public_key, trace = self.scalar_mult(private_key, self.G)

        print(trace)

        power_trace = simulate_power_trace(trace)

        return private_key, public_key, power_trace

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
G = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
     32670510020758816978083085130507043184471273380659243275938904335757337482424)
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

curve = EllipticCurve(a, b, p, G, n)

# Generate a keypair
private_key, public_key, power_trace = curve.generate_keypair()
print("Private Key:", private_key)
print("Public Key:", public_key)

np.savetxt("trace.txt", power_trace, fmt="%.6f")  # Saves as a text file

# Plot the simulated power trace
plt.plot(power_trace)
plt.title("Simulated Power Trace for Double-and-Add (With Noise)")
plt.xlabel("Time Steps")
plt.ylabel("Power Consumption")
plt.show()

# Encrypt and decrypt a message
encrypted = curve.encrypt_message(FLAG, private_key)
print("Encrypted:", encrypted.hex())


