import socket
import threading
import os
import random
import string
import struct
import subprocess

# Paramètres
HOST = '0.0.0.0'
PORT = 5000
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 4 * 1024 * 1024  # 4MB

# Création du dossier d'upload sécurisé
os.makedirs(UPLOAD_DIR, exist_ok=True)

def generate_random_filename():
    """Génère un nom de fichier aléatoire sécurisé."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def handle_client(client_socket, address):
    try:
        print(f"[+] Connexion de {address}")

        # Lire la taille du fichier (8 octets)
        file_size_data = client_socket.recv(8)
        if len(file_size_data) != 8:
            raise ValueError("Erreur de réception de la taille du fichier.")

        file_size = struct.unpack("!Q", file_size_data)[0]  # Convertir en entier
        if file_size > MAX_FILE_SIZE:
            raise ValueError("Fichier trop volumineux!")

        # Générer un nom aléatoire et stocker le fichier
        random_filename = generate_random_filename()
        filepath = os.path.join(UPLOAD_DIR, random_filename)

        received_size = 0
        with open(filepath, 'wb') as f:
            while received_size < file_size:
                chunk = client_socket.recv(min(4096, file_size - received_size))
                if not chunk:
                    break
                f.write(chunk)
                received_size += len(chunk)

        print(f"[✓] Fichier reçu et stocké sous : {filepath}")

        # Demande d'entrée utilisateur optionnelle
        client_socket.send(b"Entrez une entree utilisateur (ou tapez ENTER pour sauter) : ")
        user_input = client_socket.recv(4096).strip().decode()
        # Exécution sécurisée du fichier avec ./vm, en envoyant user_input en stdin
        command = ["/app/vm", filepath]

        p = subprocess.run(command, input=user_input, capture_output=True, text=True)
        stdout, stderr = p.stdout, p.stderr
        output = stdout + stderr

        client_socket.send(output.encode())

    except Exception as e:
        client_socket.send(f"[ERREUR] {str(e)}")
    finally:

        client_socket.close()
        print(f"[-] Connexion fermée : {address}")
        # Suppression du fichier si il existe
        if random_filename:
            try:
                if os.path.exists(filepath):  # Vérifier si le fichier existe avant de tenter de le supprimer
                    os.remove(filepath)
                    print(f"[✓] Fichier supprimé : {filepath}")
                else:
                    print(f"[INFO] Le fichier {filepath} n'existe pas, suppression ignorée.")
            except Exception as e:
                print(f"[ERREUR] Impossible de supprimer le fichier {filepath}: {str(e)}")


def start_server():
    """Démarre le serveur multi-clients."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((HOST, PORT))
    server.listen(15)
    print(f"[*] Serveur écoutant sur {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
