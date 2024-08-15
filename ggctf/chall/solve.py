#!/usr/bin/python3

from pwn import *

exe = ELF('chal', checksec=False)

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


        c
        ''')
        input()


if args.REMOTE:
    p = remote('knife.2024.ctfcompetition.com', 1337)
else:
    p = process(exe.path)
GDB()
for i in range(8):
    sla(b'Awaiting command...', 'plain plain ' + hex(0x60+i))

colls = [
b'}NDV|$xdqf(<D%a=w6k?G*e&wlDtZf!#EGAa_hHHmt1IwPbanCVzSueZex;pCXtni',
b'0de41!wcb|(<D%a=w6k?G*e&wlDtZf!#EGAa_hHHmt1IwPbanCVzSueZex;pCXtni',
b'0de4195c7cZ(-Z|=w6k?G*e&wlDtZf!#EGAa_hHHmt1IwPbanCVzSueZex;pCXtni',
b'0de4195c7cc6fa1-U4n|G*e&wlDtZf!#EGAa_hHHmt1IwPbanCVzSueZex;pCXtni',
b'0de4195c7cc6fa16c947{ADh|lDtZf!#EGAa_hHHmt1IwPbanCVzSueZex;pCXtni',
b'0de4195c7cc6fa16c947bc14f69Xb|!#EGAa_hHHmt1IwPbanCVzSueZex;pCXtni',
b'0de4195c7cc6fa16c947bc14f666f0!!1R|a_hHHmt1IwPbanCVzSueZex;pCXtni',
]
for i in range(6):
    p.sendlineafter(b'command...\n', b'a85 plain ' + colls[i])
raw = bytes.fromhex('40764603e97c81764a6572043027ee1509e5b67f4fdf8001beb41f70f5883570eb1eb50f6825271caa847e79b057a10915b88a')
p.sendlineafter(b'command...\n', b'a85 plain ' + b'0de4195c7cc6fa16c947bc14f666f03e83aaea5aaf945c4949db74d8c7834abc|')
p.sendlineafter(b'command...\n', b'plain plain ' + b'00001CW0')



p.interactive()
