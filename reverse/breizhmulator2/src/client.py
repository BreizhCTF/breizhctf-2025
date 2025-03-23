import sys
import socket
import sys
import os
import struct


"""
Ce code vous permet d'envoyer à l'émulateur une ROM après avoir déployé une instance.

Ne pas oublier de remplacer l'IP et le PORT !

PS: On est sur un challenge de reverse pas de pwn ;) ;)
"""


def send_file(hostname: str, port: int, filename: str) -> None:
    if not os.path.exists(filename):
        print("[!] Fichier introuvable.")
        return

    file_size = os.path.getsize(filename)
    if file_size > 4 * 1024 * 1024:
        print("[!] Fichier trop volumineux (> 4MB).")
        return

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((hostname, port))

        # Envoi de la taille du fichier (8 octets, format big-endian)
        client.send(struct.pack("!Q", file_size))

        # Envoi du fichier en chunks
        with open(filename, 'rb') as f:
            while chunk := f.read(4096):
                client.send(chunk)

        print("[✓] Fichier envoyé avec succès.")

        # Réception de la demande d'entrée utilisateur
        prompt = client.recv(1024).decode()
        print(prompt, end="")
        user_input = input().strip()
        if user_input == '':
            user_input = "NO USER INPUT PROVIDED"
        client.send(user_input.encode())

        # Affichage de la sortie du programme exécuté sur le serveur
        response = client.recv(4096)
        print("[OUTPUT SERVEUR]:\n", response)

    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: python {sys.argv[0]} <hostname> <port> <fichier>")
        exit(1)

    hostname, port, file = sys.argv[1:]    
    send_file(hostname, int(port), file)
