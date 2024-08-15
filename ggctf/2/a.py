from tqdm import *
import subprocess
from Crypto.Cipher import AES
key = [0x0f, 0x5b, 0x1c, 0x83, 0x3a, 0x51,
       0x19, 0x7a, 0x07, 0x1d, 0xaa, 0xf8, 0xfb]
# 0f 5b 1c 83 3a 51 19 7a 07 1d aa f8 fb
# for num in key:
#     print(num ^ 82, end=', ')
key = [93, 9, 78, 209, 104, 3, 75, 40, 85, 79, 248, 170, 169]
# for i in trange(a,b):
# Chuyển đổi thành byte với 3 byte và byte order là 'big'
# tmp = '0f5b1c833a51197a071daaf8fb'
# tmp = bytes.fromhex(tmp)
# for i in trange(0, 16777215):
#     value = i.to_bytes(3, 'big')
#     with open("key", "wb")as fi:
#         fi.write(value+tmp)
#     inp = 'decrypt fe fe d6 ce 53 59 d0 e8 86 09 05 75 b2 f1 e0 c7'
#     res = subprocess.check_output("./aes", input=inp.encode())
#     if b'echo test' in bytes.fromhex(res.decode()):
#         print(i)
#         break

# >>> 97 ^ 0x33
# 82
