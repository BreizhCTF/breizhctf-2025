import argparse
import base64
import hashlib
import os
from pwn import *
"""
This script requires pwntools
"""

def flash_chip(remote_conn, file_path):
	print("Flashing...")
	try:
		with open(file_path, "rb") as f:
			file_data = f.read()
	except IOError:
		print(f"Error: Unable to open file {file_path}. Ensure you have permission to read the file.")
		return

	if len(file_data) > 12 * 1024 * 1024:
		print("Error: File too large (must be under 12MB)")
		return

	b64_data = base64.b64encode(file_data).decode('utf-8')
	remote_conn.sendline(b"1")  # Select Flash chip memory option
	remote_conn.recvuntil(b"disk: ")
	remote_conn.sendline(b64_data.encode('utf-8'))

	response = remote_conn.recvline().decode('utf-8')
	print(response)
	print("Flashed.")

def kill_qemu(remote_conn):
	remote_conn.sendline(b"3")	# Select kill all qemu
	response = remote_conn.recvline()
	print(response)

def interactive_clean(proc):
    while True:
        try:
            line = proc.recvline(timeout=1).decode().replace("\r", "")  # Timeout after 1 sec
            print(line, end="")
        except EOFError:
            print("\n[ERREUR] Processus terminé.")
            break
        except Timeout:
            print("\n[ERREUR] Temps d'attente dépassé, aucune réponse reçue.")
        except KeyboardInterrupt:
            print("\n[INFO] Fermeture de la connexion.")
            proc.close()
            break

def boot_chip(remote_conn):
	remote_conn.sendline(b"2")  # Select Boot chip option
	response = remote_conn.recvline().decode('utf-8')
	interactive_clean(remote_conn)

def main():
	parser = argparse.ArgumentParser(description="Client for flashing and booting a RISC-V chip. (#2)")
	parser.add_argument("file_path", help="Path to fitImage file")
	parser.add_argument("ip", help="Server IP")
	parser.add_argument("port", type=int, help="Server port")
	args = parser.parse_args()

	# Suppress Pwntools logs
	context.log_level = 'critical'

	remote_conn = remote(args.ip, args.port)
	remote_conn.recvuntil(b"Menu:")

	flash_chip(remote_conn, args.file_path)
	kill_qemu(remote_conn)
	boot_chip(remote_conn)

	remote_conn.close()

if __name__ == "__main__":
	main()
