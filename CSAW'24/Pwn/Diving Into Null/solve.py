#!/usr/bin/python3

from pwn import *





info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)
p = remote('null.ctf.csaw.io', 9191)
sl(b'echo /*/*/*/*')
print(p.recvall(timeout=1))
p.interactive()
