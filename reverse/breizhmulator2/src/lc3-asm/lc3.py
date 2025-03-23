#!/usr/bin/env python3
import array
import sys
import os

from collections import namedtuple


MAX_LINE_LENGTH = 4096
UINT16_MAX = 2 ** 16


REGS = {
    'R0': 0x0,
    'R1': 0x1,
    'R2': 0x2,
    'R3': 0x3,
    'R4': 0x4,
    'R5': 0x5,
    'R6': 0x6,
    'R7': 0x7,
}

TRAPS = {
    'GETC': 0x20,
    'OUT': 0x21,
    'PUTS': 0x22,
    'IN': 0x23,
    'PUTSP': 0x24,
    'HALT': 0x25,
    'LIST_FILES' : 0x26,
    'READ_FILE' : 0x27,
}

OPS = {
    'BR':  0x0,    # 0b0 branch
    'BRn': 0x0,    # 0b0 branch if n
    'BRz': 0x0,    # 0b0 branch
    'BRp': 0x0,    # 0b0 branch
    'BRzp': 0x0,   # 0b0 branch
    'BRnp': 0x0,   # 0b0 branch
    'BRnz': 0x0,   # 0b0 branch
    'BRnzp': 0x0,  # 0b0 branch

    'ADD': 0x1,    # 0b1 add
    'LD': 0x2,     # 0b10 load
    'ST': 0x3,     # 0b11 store
    'JSR': 0x4,    # 0b100 jump register
    'JSRR': 0x4,   # 0b100 jump register
    'AND': 0x5,    # 0b101 bitwise and
    'MOV': 0x6,    # 0b110 load register
    'STR': 0x7,    # 0b111 store register
    'MOD': 0x8,    # 0b1000 unused
    'MUL': 0x9,    # 0b1001 bitwise not
    'LDI': 0xA,    # 0b1010 load indirect
    'STI': 0xB,    # 0b1011 store indirect
    'RET': 0xC,    # 0b1100 return
    'JMP': 0xC,    # 0b1100 jump
    'XOR': 0xD,    # 0b1101 reserved (unused)
    'LEA': 0xE,    # 0b1110 load effective address
    'TRAP': 0xF,   # ob1111 execute trap

    **TRAPS
}


DOTS = {
    '.ORIG': None,
    '.END': None,
    '.FILL': None,
    '.BLKW': None,
    '.STRINGZ': None
}


class Type:
    LABEL = 'label'
    OP = 'op'
    DOT = 'dot'
    CONST = 'const'
    REG = 'reg'
    STR = 'str'


Token = namedtuple('Tok', 't, v')


def tok_op_args(line):
    args = []
    for arg in line.split(','):
        arg = arg.strip()
        if not arg:
            continue
        if arg in REGS:
            args.append(Token(Type.REG, arg))
        elif arg.startswith('#'):
            args.append(Token(Type.CONST, int(arg[1:])))
        elif arg.startswith('x'):
            args.append(Token(Type.CONST, int('0' + arg, 16)))
        elif arg.startswith('b'):
            args.append(Token(Type.CONST, int('0' + arg, 2)))
        else:
            args.append(Token(Type.LABEL, arg))
    return args


def is_int(arg):
    try:
        int(arg)
        return True
    except ValueError:
        return False


def tok_dot_args(arg):
    arg = arg.strip()
    if not arg:
        return []
    if arg.startswith('"'):
        arg = arg.replace('\\t', '\t')
        arg = arg.replace('\\n', '\n')
        arg = arg.replace("\\e", '\x1b')
        return [Token(Type.STR, arg.replace('"', ''))]
    elif arg.startswith('\''):
        arg = arg.replace('\\t', '\t')
        arg = arg.replace('\\n', '\n')
        arg = arg.replace("\\e", '\x1b')
        return [Token(Type.STR, arg.replace('\'', ''))]
    elif arg.startswith('x'):
        return [Token(Type.CONST, int('0' + arg, 16))]
    elif arg.startswith('b'):
        return [Token(Type.CONST, int('0' + arg, 2))]
    elif arg.startswith('#'):
        return [Token(Type.CONST, int(arg[1:], 10))]
    elif is_int(arg):
        return [Token(Type.CONST, int(arg, 10))]
    else:
        # else it's a label
        return [Token(Type.LABEL, arg)]
    return []


def tok(line):
    line = line.strip()
    if not line or line.startswith(';'):
        return None
    line = line.replace('\t', ' ')
    line, *_ = line.split(';', maxsplit=1)
    res = line.split(' ', maxsplit=1)

    if len(res) == 1:
        token, other = res[0].strip(), ''
    else:
        token, other = res[0].strip(), res[1].strip()

    if token in OPS:
        return [Token(Type.OP, token)] + tok_op_args(other)
    elif token.startswith('.'):
        return [Token(Type.DOT, token.upper())] + tok_dot_args(other)
    else:
        if other:
            return [Token(Type.LABEL, token)] + tok(other)
        else:
            return [Token(Type.LABEL, token)]


def check_syntax(tokens):
    # TODO:
    pass


def incr(lc, tokens): return lc + 1


def asm_pass_one(code):
    CONDS = {
        '.ORIG': lambda lc, tokens: tokens[1].v,
        '.BLKW': lambda lc, tokens: lc + tokens[1].v,
        '.FILL': incr,
        '.STRINGZ': lambda lc, tokens: lc + len(tokens[1].v) + 1,
        **{op: incr for op, _ in OPS.items()},
    }
    symbol_table = {}
    lines = []
    lc = 0  # location counter

    for line_number, line in enumerate(code.splitlines(), 1):
        assert len(line) < MAX_LINE_LENGTH, 'line is too long'
        tokens = tok(line)

        if not tokens:
            continue
        if tokens[0].v == '.END':
            break

        print(f'{hex(lc):>6} ({line_number}): {line.strip():<44} | {tokens}')
        check_syntax(tokens)

        if tokens[0].t == Type.LABEL:
            symbol_table[tokens[0].v] = lc

        if tokens[0].t != Type.LABEL:
            lc = CONDS[tokens[0].v](lc, tokens)
        elif len(tokens) != 1:
            lc = CONDS[tokens[1].v](lc, tokens[1:])

        lines.append((tokens, lc))

    print('LC:', hex(lc))
    return symbol_table, lines


def encode_ldr_str(op, sym, lc, toks):
    dr = REGS[toks[1].v] << 9
    base_r = REGS[toks[2].v] << 6
    assert toks[3].v < 2 ** 5
    offset6 = ((UINT16_MAX + toks[3].v) & 0b111111)
    return op | dr | base_r | offset6


def encode_add_and(op, sym, lc, toks):
    dr = REGS[toks[1].v] << 9
    sr1 = REGS[toks[2].v] << 6
    if toks[3].t == Type.REG:
        sr2 = REGS[toks[3].v]
        return op | dr | sr1 | sr2
    else:
        assert toks[3].v < 2 ** 5
        imm5 = ((UINT16_MAX + toks[3].v) & 0b11111)
        return op | dr | sr1 | 1 << 5 | imm5


def encode_br(op, sym, lc, toks):
    if toks[0].v == 'BR':
        op |= 1 << 11
        op |= 1 << 10
        op |= 1 << 9
    if 'n' in toks[0].v:
        op |= 1 << 11
    if 'z' in toks[0].v:
        op |= 1 << 10
    if 'p' in toks[0].v:
        op |= 1 << 9

    if toks[1].t == Type.LABEL:
        pcoffset9 = ((sym[toks[1].v] - lc) & 0b111111111)
    elif toks[1].t == Type.CONST:
        pcoffset9 = toks[1].v & 0b111111111
    else:
        raise Exception()

    return op | pcoffset9


def encode_ld_st(op, sym, lc, toks):
    dr = REGS[toks[1].v] << 9
    return op | dr | ((sym[toks[2].v] - lc) & 0b111111111)

def encode_mov_imm(op, sym, lc, toks):
    dr = REGS[toks[1].v] << 9
    return op | dr | (toks[2].v& 0b111111111)

def encode_traps(op, sym, lc, toks):
    return OPS['TRAP'] << 12 | TRAPS[toks[0].v]


encode = {
    'MOD': encode_add_and,
    'TRAP': lambda op, sym, lc, toks: op | toks[1].v & 0b11111111,
    'RET': lambda op, *_: op | 0b111 << 6,
    'JMP': lambda op, sym, lc, toks: op | REGS[toks[1].v] << 6,
    'MUL': encode_add_and,
    'JSR': lambda op, sym, lc, toks: op | 1 << 11 | ((sym[toks[1].v] - lc) & 0b11111111111),
    'JSRR': lambda op, sym, lc, toks: op | REGS[toks[1].v] << 6,
    'MOV': encode_mov_imm,
    'STR': encode_ldr_str,
    'AND': encode_add_and,
    'ADD': encode_add_and,
    'BR': encode_br,
    'BRn': encode_br,
    'BRz': encode_br,
    'BRp': encode_br,
    'BRzp': encode_br,
    'BRnp': encode_br,
    'BRnz': encode_br,
    'BRnzp': encode_br,
    'LD': encode_ld_st,
    'LEA': encode_ld_st,
    'LDI': encode_ld_st,
    'ST': encode_ld_st,
    'STI': encode_ld_st,
    'XOR': encode_add_and,
    'GETC': encode_traps,
    'OUT': encode_traps,
    'PUTS': encode_traps,
    'LIST_FILES' : encode_traps,
    'READ_FILE' : encode_traps,
    'IN': encode_traps,
    'PUTSP': encode_traps,
    'HALT': encode_traps,
}


def asm_pass_two(symbol_table, lines):
    CONDS = {
        '.BLKW': lambda tokens, data, sym, lc:
        data.fromlist([0x0 for _ in range(tokens[1].v)]),

        '.FILL': lambda tokens, data, sym, lc: tokens[1].t == Type.CONST and
        data.append(tokens[1].v) or tokens[1].t == Type.LABEL and
        data.append(sym[tokens[1].v]),

        '.STRINGZ': lambda tokens, data, sym, lc:
        data.fromlist([c for c in tokens[1].v.encode()]) or data.append(0x0),

        **{
            op: lambda toks, data, sym, lc:
            data.append(encode[toks[0].v](OPS[toks[0].v] << 12, sym, lc, toks))
            for op, _ in OPS.items()
        }
    }
    data = array.array("H", [])
    data.append(lines[0][0][1].v)

    for tokens, lc in lines[1:]:
        if tokens[0].v == '.END':
            break
        print(tokens)

        if tokens[0].t != Type.LABEL:
            CONDS[tokens[0].v](tokens, data, symbol_table, lc)
        elif len(tokens) != 1:
            CONDS[tokens[1].v](tokens[1:], data, symbol_table, lc)

    data.byteswap()
    return data


def dump_symbol_table(symbol_table):
    with open('2048-out.sym', 'w') as f:
        f.write('\n\n\n\n')
        for a, b in symbol_table.items():
            f.write(f'//\t{a:<16}  {hex(b)[2:].upper()}\n')


def main():
    if len(sys.argv) < 2:
        print('lc3.py [asm-file]')
        exit(2)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print('No such file')
        exit(2)

    with open(file_path) as f:
        code = f.read()

    print('STARTING PASS 1')
    symbol_table, lines = asm_pass_one(code)
    dump_symbol_table(symbol_table)

    print('STARTING PASS 2')
    bin_data = asm_pass_two(symbol_table, lines)
    print(bin_data.tobytes().hex())
    file_name = os.path.splitext(file_path)[0]
    file_name = f'{file_name}-out.obj'

    with open(file_name, 'wb') as f:
        f.write(bin_data.tobytes())
    print('Saved', file_name)


if __name__ == '__main__':
    main()
