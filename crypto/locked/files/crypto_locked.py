#!/usr/bin/env python3
from Crypto.Protocol.SecretSharing import Shamir
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes
from time import time
import datetime
from secret import FLAG

INIT_TIMESTAMP = 1737299303  # Sun Jan 19 2025 16:08:23 GMT+01 
MAX_TIMESTAMP = 1743465600   # Tue Apr 01 2025 02:00:00 GMT+02
LENGTH = (MAX_TIMESTAMP - INIT_TIMESTAMP) // 10

REF_TIME = int(time())

def aes_encrypt(key: bytes, plaintext: bytes):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext, 16))
    return cipher.iv.hex() + ciphertext.hex()


def aes_decrypt(key, ciphertext):
    iv = bytes.fromhex(ciphertext[:32])
    ciphertext = bytes.fromhex(ciphertext[32:])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), 16)
    return plaintext.hex()


def generate_master_key():
    key = random.randbytes(16)
    return key


def generate_shares(key, number_to_recover, number_of_shares):
    shares = Shamir.split(number_to_recover, number_of_shares, key)
    return shares


def combine_shares(shares):
    key = Shamir.combine(shares)
    return key


def generate_secret_sequence(length):
    """
    Générer la séquence de secret
    """
    secret_sequence = []

    n = 128
    seed = random.randint(1, 2**n)

    z = random.randint(1, 2**n)

    if z%2 == 0: z += 1

    value = seed
    for _ in range(length):
        value = value*z % 2**n
        secret_sequence.append(value >> 18)

    return secret_sequence


def key_release(secret, share, t):
    r = aes_encrypt(pad(long_to_bytes(secret[t]), 16), share)

    return r


def get_secret_t(secret_sequence: list):
    """
    Révéler le secret correspondant (1 secret toutes les 10 secondes)
    """
    current_t = ((int(time()) - REF_TIME + 1740079600)// 10) * 10
    print(f"Secret pour le : {datetime.datetime.fromtimestamp(current_t).strftime('%Y-%m-%d %H:%M:%S')}")
    index_minute = (current_t - INIT_TIMESTAMP) // 10

    return secret_sequence[index_minute]


K = generate_master_key()

# Chiffrement du FLAG
C = aes_encrypt(K, FLAG)

# Création des morceaux (shares) à partir de K
shares = generate_shares(K, 2, 3)

LOCKED_TIME = 1742079600  # Donnée protégée jusqu-au 16 Mars 2025 à 00h :)
print(f"Donnée vérouillée jusqu'au : {datetime.datetime.fromtimestamp(LOCKED_TIME).strftime('%Y-%m-%d %H:%M')}")
print(f"Donnée chiffrée : {C}")
t = (LOCKED_TIME - INIT_TIMESTAMP) // 10

# Agent de confiance 1
s1 = generate_secret_sequence(LENGTH)
y1 = shares[0][1]
r1 = key_release(s1, y1, t)

print(f"Chiffré du morceau (Encrypted Share) de l'Agent 1 pour le temps de référence (Locked Time) : {r1}")

# Agent de confiance 2
s2 = generate_secret_sequence(LENGTH)
y2 = shares[1][1]
r2 = key_release(s2, y2, t)

print(f"Chiffré du morceau (Encrypted Share) de l'Agent 2 pour le temps de référence (Locked Time) : {r2}")

# Agent de confiance 3
s3 = generate_secret_sequence(LENGTH)
y3 = shares[2][1]
r3 = key_release(s3, y3, t)

print(f"Chiffré du morceau (Encrypted Share) de l'Agent 3 pour le temps de référence (Locked Time) : {r3}")

while True:
    print("1- Récupérer le secret courant de l'Agent 1")
    print("2- Récupérer le secret courant de l'Agent 2")
    print("3- Récupérer le secret courant de l'Agent 3")
    print("4- Quitter")

    try:
        choice = int(input())
    except:
        print("Opération non autorisée !!")
        exit()

    if choice == 1:
        print(f"Secret courant de l'Agent 1 : {get_secret_t(s1)}")
    elif choice == 2:
        print(f"Secret courant de l'Agent 2 : {get_secret_t(s2)}")
    elif choice == 3:
        print(f"Secret courant de l'Agent 3 : {get_secret_t(s3)}")
    else:
        break
