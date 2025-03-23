#!/usr/bin/env python3
import struct
import argparse
from Crypto.PublicKey import RSA
"""
This script requires pycryptodome
"""

def compute_n0inv(n):
    """ Compute n0inv = -n^(-1) mod 2^32 """
    r = 2**32
    n0inv = pow(n, -1, r)  # Modular inverse of n mod 2^32
    return (-n0inv) % r  # Ensure it's positive

def compute_rr(n):
    """ Compute R^2 mod n for Montgomery multiplication (R = 2^(len(n)*32)) """
    r = 1 << (len(bin(n)) - 2)  # R = 2^(bit length of n)
    rr = (r * r) % n  # R^2 mod n
    rr_words = [(rr >> (32 * i)) & 0xFFFFFFFF for i in range(32)]  # Convert to 32-bit words
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
    assert len(key_id) < 256, "Key id too long."
    KEY_ID = key_id.encode()

    # Write to binary file
    with open(output_bin, "wb") as f:
        f.write(b"BZH.CERT") # magic bytes :)
        f.write(struct.pack("<Q", e))  # rsa_pub_exponent (8 bytes)
        f.write(struct.pack("<I", n0inv))  # rsa_n0inv (4 bytes)
        f.write(struct.pack("<32I", *rr))  # rsa_rr (128 bytes)
        f.write(struct.pack("<32I", *rsa_pub_modulus))  # rsa_pub_modulus (128 bytes)
        f.write(struct.pack("<I", len(KEY_ID))) # len_key_id (4 bytes)
        f.write(KEY_ID)

    print(f"Successfully created '{output_bin}' from '{input_pem}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate RSA 1024-bit public key binary file from private.pem for BreizhBoot secure-boot implementation.")
    parser.add_argument("input_pem", help="Path to RSA 1024-bit private key (PEM format)")
    parser.add_argument("output_bin", help="Path to output binary file (e.g., pubkey.breizhcertificate)")
    parser.add_argument("key_id", help="String identifying the key (basically CN)")

    args = parser.parse_args()

    try:
        generate_pubkey(args.input_pem, args.output_bin, args.key_id)
    except Exception as e:
        print(f"Error: {e}")

