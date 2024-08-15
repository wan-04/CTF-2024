#!/usr/bin/python3

from pwn import *

exe = ELF('aes', checksec=False)

context.binary = exe

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
sln = lambda msg, num: sla(msg, str(num).encode())
sn = lambda msg, num: sa(msg, str(num).encode())

def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''


        c
        ''')
        input()


if args.REMOTE:
    p = remote('encrypted-runner.2024.ctfcompetition.com', 1337)
else:
    p = process(exe.path)
GDB()
sla(b'- exit', b'encrypt echo 1abc')
key_xor = 85



p.interactive()
