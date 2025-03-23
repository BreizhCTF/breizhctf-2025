#!/usr/bin/env python3
import array
import sys

UINT16_MAX = 2 ** 16

ops = {
    0: 'BR',
    1: 'ADD',
    2: 'LD',
    3: 'ST',
    4: 'JSRR',
    5: 'AND',
    6: 'LDR',
    7: 'STR',
    8: 'RTI',
    9: 'NOT',
    10: 'LDI',
    11: 'STI',
    12: 'JMP',
    13: 'RES',
    14: 'LEA',
    15: 'TRAP',
    32: 'GETC',
    33: 'OUT',
    34: 'PUTS',
    35: 'IN',
    36: 'PUTSP',
    37: 'HALT'
}


def parse_op(op):
    return ops.get(op >> 12)


def main():
    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        origin = int.from_bytes(f.read(2), byteorder='big')
        dump = array.array("H", [origin])
        max_read = UINT16_MAX - origin
        dump.frombytes(f.read(max_read))
        dump.byteswap()
        for op in dump[1:]:
            print(
                f'{hex(origin)}: ({hex(op):>6}) {parse_op(op)} | '
                f'{chr(op) if op < 256 else ""}')
            origin += 1


if __name__ == '__main__':
    main()
