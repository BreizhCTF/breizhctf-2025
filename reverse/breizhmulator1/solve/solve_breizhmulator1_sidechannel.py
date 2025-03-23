from qiling import Qiling
from qiling.const import QL_VERBOSE
from qiling.extensions import pipe
import string

LEN_FLAG = 52
FLAG = b""

currentINDEX = 0
currentCHAR = ""
nValid = 0
FOUNDED = False


def vm_after_XOR_hook(ql: Qiling) -> None:
    global nValid
    global FLAG
    global FOUNDED
    global currentINDEX

    if currentINDEX + 1 == len(FLAG):
        return

    ecx = ql.arch.regs.read("ECX")

    if ecx != 0:
        nValid = 0
        ql.emu_stop()

    elif nValid == 3 * currentINDEX + 2:
        FLAG += currentCHAR.encode()
        nValid = 0
        FOUNDED = True
        ql.emu_stop()

    else:
        nValid += 1
        return


for i in range(LEN_FLAG):
    currentINDEX = i

    for c in string.printable:
        currentCHAR = c
        rootfs = r"./rootfs/x8664_linux_glibc2.39/"
        ql = Qiling(["./vm", "/chall-out.obj"], rootfs, verbose=QL_VERBOSE.DISABLED)

        # Instrumentation
        base_addr = ql.loader.images[0].base
        hook_addr_vm_after_XOR = base_addr + 0x1A54
        ql.hook_address(vm_after_XOR_hook, hook_addr_vm_after_XOR)

        # Send flag
        ql.os.stdin = pipe.SimpleInStream(0)
        ql.os.stdin.write(FLAG + c.encode())
        ql.os.stdout = None

        # Emulate
        ql.run()

        if FOUNDED:
            print("[+]", FLAG)
            FOUNDED = False
            break
