#!/usr/bin/python3

from pwn import *

exe = ELF('simpleqiling_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''


                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('103.163.24.78', 10010)
else:
    p = process("python3 qi.py simpleqiling_patched".split())

# GDB()
pa = b'a'*8*5
sa(b'say', pa)

##########

p.interactive()
