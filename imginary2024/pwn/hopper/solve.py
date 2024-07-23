#!/usr/bin/python3

from pwn import *

exe = ELF('vuln_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
    p = remote('')
else:
    p = process(exe.path)
GDB()

def cr(size, pa):
    sla(b'choice> ', b'1')
    sla(b'size> ', str(size))
    sla(b'content> ', pa)
def rm(idx):
    sla(b'choice> ', b'2')
    sla(b'idx> ', str(idx))
def sh(idx):
    sla(b'choice> ', b'3')
    sla(b'idx> ', str(idx))
cr(0x20, b'wan')
rm(0)
cr(8, b'wan')
# cr(0x10, b'wan')
# rm(0)
p.interactive()
