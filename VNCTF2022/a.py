#!/usr/bin/python3

import sys
import os
import stat

script = f'''#!/usr/bin/python3

from pwn import *

exe = ELF('{sys.argv[1] if len(sys.argv) != 1 else ""}', checksec=False)
{("libc = ELF('" + sys.argv[2] + "', checksec=False)") if len(sys.argv) != 2 else ("libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6', checksec=False)")}
context.binary = exe

def GDB():
        if not args.REMOTE:
                gdb.attach(p, gdbscript=\'\'\'


                c
                \'\'\')
                input()

info = lambda msg: log.info(msg)
sla = lambda msg, data: p.sendlineafter(msg, data)
sa = lambda msg, data: p.sendafter(msg, data)
sl = lambda data: p.sendline(data)
s = lambda data: p.send(data)

if args.REMOTE:
        p = remote('')
else:
        p = process(exe.path)

GDB()

p.interactive()
'''

with open('solve.py', 'wt') as f:
    f.write(script)
os.chmod('solve.py', 0o755)
os.system('code .')
