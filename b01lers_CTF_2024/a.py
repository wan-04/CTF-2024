from pwn import *

io = remote("gold.b01le.rs", 5002)
# io = process(["python3","real_chal.py"])
sleep(0.1)
io.recvuntil(b'Treat or Trick, count my thing. \n')
flag_enc = io.recvline(keepends=False).decode()
flag_enc = bytes.fromhex(flag_enc)
print(flag_enc)
payload = "\r\n"*254
io.send(payload.encode())
sleep(5)
io.sendlineafter(b'Give me something to encrypt: ', 'aa'*96)


    
        
io.interactive()
