load("sanitize.sage")
load("distinguisher.sage")

import os
os.environ.setdefault("TERM", "linux")

from sys import argv
if len(argv) != 3:
    print("usage: sage solve.sage <host> <port>")
    exit()

from pwn import remote
conn = remote(argv[1], int(argv[2]))

_ = conn.recvline().decode()

count = 0
seuil = 128
for _ in range(135):
    if count == seuil:
        print(conn.recvline().decode())
        conn.close()
        break

    A = conn.recvline().decode()
    A = A.split("sanitize_mat(A) = ")[1]
    A = isanitize_mat(A)

    t = conn.recvline().decode()
    t = t.split("sanitize_vec(t) = ")[1]
    t = isanitize_vec(t)
 
    res = distinguish(A, t)

    if res == True:
        conn.sendline(b"1")
    else:
        conn.sendline(b"0")

    _ = conn.recvline()
    res = conn.recvline()

    if b"wp" in res:
        count += 1
    
    print(f"{count}/{seuil}")

