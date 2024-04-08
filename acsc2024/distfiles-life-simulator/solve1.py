from pwn import *
r = gdb.debug("./life_simulator")
# r = remote("localhost", 9000)
# r = remote("life-simulator.chal.2024.ctf.acsc.asia", 9000)
t = None
def gt(at=None): return at if at else t
def sl(x, t=None): return gt(t).sendline(byt(x))
def se(x, t=None): return gt(t).send(byt(x))
def sla(x, y, t=None): return gt(t).sendlineafter(byt(x), byt(y))
def sa(x, y, t=None): return gt(t).sendafter(byt(x), byt(y))
def ra(t=None): return gt(t).recvall()
def rl(t=None): return gt(t).recvline()
def rls(t=None): return rl(t)[:-1]
def re(x, t=None): return gt(t).recv(x)
def ru(x, t=None): return gt(t).recvuntil(byt(x))
def it(t=None): return gt(t).interactive()
def cl(t=None): return gt(t).close()



r.interactive()
