# LC-3 assembler in python

LC-3 assembler written in pure python

## Getting Started

### Assemble

```
python3 lc3.py [file]  # lc3 *.asm file
# Output *.obj file that can be run with simulator
```

### Run tests:

```
python3 run-tests.py
```

### Debug

To debug, you can use simple disassembler written by me:

```
python3 disasm.py [obj-file]
```

I found it very usefull trying to understand what went wrong (invalid address in symbol table, invalid LC count, invalid opcode encoding, etc.).

There is a lot of debug information printing out when assembling but it can be ignored or deleted.

### Learning LC-3

You can find usefull information and Instruction Set Architecture (ISA) [here](https://github.com/justinmeiners/lc3-vm) and [here](https://github.com/paul-nameless/lc3-vm)

Also you may find usefull desctiptions in `assembler.h` file to better understand how to implement it [here](https://github.com/davedennis/LC3-Assembler)


### Download

You can download simulator [here](http://highered.mheducation.com/sites/0072467509/student_view0/lc-3_simulator.html)

Or use my own implementation written in pure [python](https://github.com/paul-nameless/lc3-vm)

You can find 2048 game written in lc3 [here](https://github.com/rpendleton/lc3-2048)
