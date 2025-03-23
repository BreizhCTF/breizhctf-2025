import math
import random
import socket
import threading

from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


def load_rsa_public_key(public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(), backend=default_backend()
        )
    return public_key


def encrypt_rc4_key(rc4_key, public_key):
    encrypted_key = public_key.encrypt(
        rc4_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None,
        ),
    )
    return encrypted_key


GRID_SIZE = 15


# Lower Whythoff sequence function
def why_s(n):
    return math.floor(n * ((1 + math.sqrt(5)) / 2))


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


# Fonction pour obtenir une position initiale aléatoire
def generate_random_position(couplesBADposition):
    x = 0
    y = 0
    while x == 0 or y == 0 or x == y or (x, y) in couplesBADposition:
        x = random.randint(3, GRID_SIZE)  # Vous pouvez ajuster les limites ici
        y = random.randint(3, GRID_SIZE)  # Vous pouvez ajuster les limites ici
    return (x, y)


# Fonction de validation du mouvement
def is_valid_move(currentPosition, move):
    current_x, current_y = currentPosition
    next_x, next_y = move

    # Le mouvement doit être :
    # - vers le bas (mouvement vertical en y)
    # - vers la gauche (mouvement horizontal en x)
    # - en diagonale
    # On permet de se déplacer sur plusieurs cases
    if next_x > GRID_SIZE or next_y > GRID_SIZE:
        return False
    elif next_x > current_x or next_y > current_y:
        return False
    elif next_x == current_x and next_y == current_y:
        return False

    return (
        next_x == current_x
        or next_y == current_y
        or (current_x - next_x == current_y - next_y)
    )


def handle_client(client_socket, client_address):
    try:
        print(f"[-] Client connecté depuis {client_address}")
        couplesBADposition = generate_couples(GRID_SIZE)

        R_KEY = client_socket.recv(16)
        public_key = load_rsa_public_key("public_key.pem")
        # Chiffrer la clé RC4
        encrypted_rc4_key = encrypt_rc4_key(R_KEY, public_key)
        encrypted_rc4_key_b = encrypted_rc4_key.hex().encode()
        client_socket.sendall(encrypted_rc4_key_b)

        client_socket.recv(1)  # print("[-] Byte to skip", client_socket.recv(1))

        clientWINs = 0
        for i in range(3):
            lastPosition = generate_random_position(
                couplesBADposition
            )  # Position initiale aléatoire
            intialPosition = bytearray(2)
            intialPosition[0] = lastPosition[0]
            intialPosition[1] = lastPosition[1]
            client_socket.sendall(intialPosition)

            while True:
                # Recevoir le mouvement du client
                move = client_socket.recv(4)
                client_socket.recv(
                    1
                )  # print("[-] Byte to skip", client_socket.recv(1))

                if not move:
                    client_socket.close()
                    exit(-1)

                move = (move[0], move[1])

                # Vérifier si le mouvement du client est valide
                if not is_valid_move(lastPosition, move):
                    client_socket.close()
                    exit(-1)

                # Vérifier si le client a gagné
                if move == (0, 0):
                    clientWINs += 1
                    break

                # Calculer le prochain mouvement du serveur
                nextMove = next_move(move, couplesBADposition)
                lastPosition = nextMove

                # Envoyer le mouvement du serveur au client
                next_move_to_send = bytearray(2)
                next_move_to_send[0] = nextMove[0]
                next_move_to_send[1] = nextMove[1]
                client_socket.sendall(next_move_to_send)

                # Vérifier si le hacker a gagné
                if nextMove == (0, 0):
                    break

        if clientWINs == 3:
            with open("private_key.pem", "rb") as key_file:
                client_socket.sendall(
                    b"G4m3_gg_FOR_7H3_qU33n}: "
                    + b"".join(key_file.readlines())
                    + b"\x00"
                )

    finally:
        client_socket.close()


# Configuration du serveur
def start_server():

    host, port = "0.0.0.0", 4444

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Serveur en attente de connexions...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address)
        )
        client_thread.start()


if __name__ == "__main__":
    start_server()
