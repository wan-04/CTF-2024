#!/usr/bin/python3

from pwn import *
import time
import random


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
    p = remote('challs.nusgreyhats.org', 31111)
else:
    p = process(['python3', 'time_1.py'])
# GDB()
random.seed(int(time.time()))
n = random.randint(1000000000000000, 10000000000000000-1)
sla(b':', str(n))

p.interactive()
