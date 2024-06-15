#!/usr/bin/python3

from pwn import *

# exe = ELF('a', checksec=False)

# context.binary = exe
# context.error = exe

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


# This code snippet is checking if the script is running in remote mode or not. If `args.REMOTE` is
# True, it creates a remote connection to the IP address '20.80.240.190' on port 4440 using the
# `remote` function from the `pwn` library. If `args.REMOTE` is False, it creates a local process
# using the `process` function with the path of the executable file specified by `exe.path`.

# GDB()
m = 3
# while 1:
#     for d in range(13, 32):
#         p = remote('20.80.240.190', 4440)
#         context.log_level = 'error'
        
#         sla(b' Akasec?', b'Hamid Laarandas')
#         sla(b'dd/mm/yyyy)', "{:02d}/{:02d}/{:04d}".format(d, m, 2001))
#         res = p.recvline()
#         # if b'Incorrect answer,' not in res:
#         print(res, d, m)
#         p.close()
#         sleep(0.1)
p = remote('20.80.240.190', 4440)
sla(b' Akasec?', b'Hamid Laarandas')
sla(b'dd/mm/yyyy)', "13/03/2001")
sl("13hamid.laarandas37@gmail.com")
sl('+21651413200')
p.interactive()
