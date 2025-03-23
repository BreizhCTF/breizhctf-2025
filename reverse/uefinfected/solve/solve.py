import socket
import math
from sys import argv

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import ARC4


if len(argv) != 3:
    print("usage: `python solve.py <HOST> <PORT>`")
    exit()


HOST = argv[1]
PORT = int(argv[2])
GRID_SIZE = 15


def decrypt_rc4(key, input_file, output_file):
    # Ouvre le fichier chiffré en mode lecture binaire
    with open(input_file, "rb") as f_in:
        encrypted_data = f_in.read()

    # Crée un objet de déchiffrement RC4 avec la clé donnée
    cipher = ARC4.new(key)

    # Déchiffre les données
    decrypted_data = cipher.decrypt(encrypted_data)

    # Sauve le fichier déchiffré
    with open(output_file, "wb") as f_out:
        f_out.write(decrypted_data)

    print(f"Fichier déchiffré sauvegardé sous : {output_file}")


# Fonction pour charger la clé privée RSA à partir d'une chaîne de caractères (PEM)
def load_rsa_private_key(private_key_pem):
    private_key = serialization.load_pem_private_key(
        private_key_pem, password=None, backend=default_backend()
    )
    return private_key


# Fonction pour déchiffrer une clé RC4 avec une clé privée
def decrypt_rc4_key(encrypted_rc4_key, private_key):
    decrypted_key = private_key.decrypt(
        encrypted_rc4_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )
    return decrypted_key


# Fonction pour générer les positions "BAD"
def generate_couples(GRID_SIZE):
    couplesBADposition = []
    k = 0
    while True:
        n = math.floor(k * ((1 + math.sqrt(5)) / 2))
        m = n + k
        couplesBADposition.append((n, m))
        couplesBADposition.append((m, n))  # symétrique
        if m >= GRID_SIZE:
            break
        k += 1
    return couplesBADposition


# Fonction qui gère la logique de déplacement
def next_move(last_position, couplesBADposition):
    for cp in couplesBADposition:
        if last_position[0] == cp[0] and last_position[1] > cp[1]:  # GRID_SIZE
            return cp
        elif last_position[1] == cp[1] and last_position[0] > cp[0]:  # Y
            return cp
        elif (
            abs(cp[0] - last_position[0]) == abs(cp[1] - last_position[1])
            and cp[0] < last_position[0]
            and cp[1] < last_position[1]
        ):  # |x1 - x2| = |y1 - y2|
            return cp

    choice = random.randint(0, 1)  # Choix aléatoire pour les cases restantes
    if choice == 0:
        x = random.randint(0, last_position[0] - 1)
        y = last_position[1]
    elif choice == 1:
        x = last_position[0]
        y = random.randint(0, last_position[1] - 1)
    return (x, y)


couplesBADposition = generate_couples(GRID_SIZE)

# Connexion au serveur
server_address = (HOST, PORT)  # Remplace par l'adresse et le port du serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

client_socket.send(b"A" * 16)

RSA_ = client_socket.recv(256)
print(RSA_)

client_socket.send(b"_")  # Junk byte bc qemu ft. edk2 are weird

for i in range(3):
    nextMove = (-1, -1)
    print("\nGame n°", i)
    while nextMove != (0, 0):
        move = client_socket.recv(2)

        move = (move[0], move[1])

        print("[-] Server initial move :", move)

        nextMove = next_move(move, couplesBADposition)
        print("[-] My winning move :", nextMove)
        # Envoyer le mouvement du serveur au client
        next_move_to_send = bytearray(4)
        next_move_to_send[0] = nextMove[0]
        next_move_to_send[1] = nextMove[1]
        next_move_to_send[2] = 0
        next_move_to_send[3] = 0

        client_socket.send(next_move_to_send)
        client_socket.send(b"_")  # Junk byte bc qemu ft. edk2 are weird

print("\n[+] GG WP !\n")

FLAG_PART, PRIVATE_KEY = client_socket.recv(1024).split(b": ")

print("[+] Last flag part :", FLAG_PART)

PRIVATE_KEY = PRIVATE_KEY.rstrip(b"\n\x00")


with open("your_key_my_queen", "r") as r:
    encrypted_rc4_key = bytes.fromhex(r.read(256))


# Charger la clé privée
private_key = load_rsa_private_key(PRIVATE_KEY)

# Déchiffrer la clé RC4
rc4_key = decrypt_rc4_key(encrypted_rc4_key, private_key)


print("[+] RC4 Key déchiffrée :", rc4_key.hex())


decrypt_rc4(rc4_key, "300.jpg", "300_decrypted.jpg")
