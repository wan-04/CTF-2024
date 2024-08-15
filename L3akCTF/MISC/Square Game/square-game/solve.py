#!/usr/bin/python3

from pwn import *
import math
# exe = ELF('a.py', checksec=False)

# context.binary = exe


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
    p = remote('localhost', 6669)
else:
    p = process(exe.path)


def find_max(x_max, y_max, x_min, y_min, x, y):
    math.sqrt((x_max-x))


GDB()
r = 500000
d = 0
p.recvuntil(b'Point is (')
x = int(p.recvuntil(b', ', drop=True).decode())
y = int(p.recvuntil(b')', drop=True).decode())
sla(b'Length>', str(r))
print(p.recvline())

x_max, y_max, x_min, y_min = (x+r)/2, (y+r)/2, (x-r)/2, (y-r)/2
x_a, y_a = x, y
x_o, y_o = x_max, y_max
for i in range(10):
    p.recvuntil(b'Point is (')
    x = int(p.recvuntil(b', ', drop=True).decode())
    y = int(p.recvuntil(b')', drop=True).decode())
    if (x > 0):
        x_o = x_min
    if (y > 0):
        y_o = y_min
    r = (math.sqrt((x_a - x)**2 + (y_a - y)**2) +
         math.sqrt((x_o - x)**2 + (y_o - y)**2))
    x_max, y_max, x_min, y_min = (x+r)/2, (y+r)/2, (x-r)/2, (y-r)/2
    
    sla(b'Length>', str(round(r)))
    print(p.recvline())
    print(x, y)
    input()


p.interactive()
