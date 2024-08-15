#!/usr/bin/python3

from pwn import *

exe = ELF('chal', checksec=False)

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
        # b* 0x55555555633f
        # brva 0x2371 
        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)

# for i in range(11):
#     sla(b'command...', 'plain a85 ' + chr(0x61+i)*(128))

# GDB()

# sla(b'command...', f'plain a85 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
# sla(b'command...', b'plain a85 ' + b'â')
# sla(b'command...', f'plain hex â')
# sla(b'command...', f'plain plain 61\0\0\0')
# sla(b'command...', b'hex a85 ' + b'3631')
# sla(b'command...', b'hex a85\x0b'+ b'3631')
# sla(b'command...', b'hex\x0ba85\x0b'+ b'36\x0c31\x0b')
# sla(b'command...', b'a85 hex ' + b'K~|o|')
with open("text", "a")as f:
    for j1 in range(256):
        for j2 in range(256):
            for j3 in range(256):
                for j4 in range(256):
                        p = process(exe.path)
                    
                    for i in range(256):
                        if (i) not in [9, 10, 11, 12]:
                            sla(b'command...', 'plain a85 ' + chr(j1) +
                                chr(j2) + chr(j3) + chr(j4) + chr(i))
                            (p.recvline())
                            f.write(str(p.recvline())+str(j1)+' '+str(j2) +
                                    ' '+str(j3)+' '+str(j4)+' '+str(i)+' ''\n')


p.interactive()
'''
cache 0x5555555591e0
heap 0x5555555811e0

'''
