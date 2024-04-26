from hashlib import md5
from pwn import*
from Crypto.Cipher import AES

io = remote("challs.nusgreyhats.org", 32223)

# io = process(["python3","./filter_ciphertext.py"])

io.recvuntil(b'Encrypted secret: ')

enc_secret = io.recvuntil(b'\n',drop=True).decode()

io.recvuntil(b'iv: ')

iv_flag = bytes.fromhex(io.recvuntil(b'\n',drop=True).decode())

io.recvuntil(b'ct: ')

ct = bytes.fromhex(io.recvuntil(b'\n',drop=True).decode())


io.recvuntil(b'> ')
io.sendline(b'00000000000000000000000000000000'*2)
iv = io.recvuntil(b'\n',drop=True).decode()
iv = bytes.fromhex(iv)
iv = iv[16:]

enc_flag = bytes.fromhex(enc_secret)
b0 = enc_flag[:16]
b1 = enc_flag[16:32]
b2 = enc_flag[32:48]
b3 = enc_flag[48:64]
b4 = enc_flag[64:80]

res = b''

io.recvuntil(b'> ')
io.sendline(b1.hex().encode() + b0.hex().encode())
de_b0 = bytes.fromhex(io.recvuntil(b'\n',drop=True).decode())
dec_b0 = xor(xor(xor(de_b0[:16],de_b0[16:]),iv),b1)
print(dec_b0.hex())

io.recvuntil(b'> ')
io.sendline(b2.hex().encode() + b1.hex().encode())
de_b1 = bytes.fromhex(io.recvuntil(b'\n',drop=True).decode())
dec_b1 = xor(xor(xor(xor(de_b1[:16],de_b1[16:]),dec_b0),b2),b0)
print(dec_b1.hex())

io.recvuntil(b'> ')
io.sendline(b3.hex().encode() + b2.hex().encode())
de_b2 = bytes.fromhex(io.recvuntil(b'\n',drop=True).decode())
dec_b2 = xor(xor(xor(xor(de_b2[:16],de_b2[16:]),b3),b1),dec_b1)
print(dec_b2.hex(),"2")

io.recvuntil(b'> ')
io.sendline(b4.hex().encode() + b3.hex().encode())
de_b3 = bytes.fromhex(io.recvuntil(b'\n',drop=True).decode())
dec_b3 = xor(xor(xor(xor(de_b3[:16],de_b3[16:]),b4),b2),dec_b2)
print(dec_b3.hex(),"3")

b5 = b'a'*16

io.recvuntil(b'> ')
io.sendline(b5.hex().encode() + b4.hex().encode())
de_b4 = bytes.fromhex(io.recvuntil(b'\n',drop=True).decode())
dec_b4 = xor(xor(xor(xor(de_b4[:16],de_b4[16:]),b5),b3),dec_b3)
print(dec_b4.hex(),)

secret = dec_b0+dec_b1+dec_b2+dec_b3+dec_b4
print(secret.hex())
secret_key = md5(secret).digest()

cipher = AES.new(key = secret_key, iv = iv_flag, mode = AES.MODE_CBC)

print(cipher.decrypt(ct))