import sys

chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~"

def a85(s):
    i = 0
    ct = ''
    while True:
        if i >= len(s):
            return ct
        if i + 1 == len(s):
            local_20 = s[i] + 0x101010000
        elif i + 2 == len(s):
            local_20 = s[i] + s[i+1] * 0x100 + 0x101000000
        elif i + 3 == len(s):
            local_20 = s[i] + (s[i+1] + (s[i+2] * 0x100)) * 0x100 + 0x100000000
        else:
            local_20 = s[i] + (s[i+1] + (s[i+2] + (s[i+3] * 0x100)) * 0x100) * 0x100
        for _ in range(5):
            ct += chars[local_20 % 85]
            local_20 = local_20 // 85
        i += 4

if __name__ == '__main__':
    s = sys.argv[1]
    s = bytes.fromhex(s)
    assert len(s) % 4 != 0, 'length of plaintext cannot be a multiple of 4'
    remaining_block_length = len(s) % 4
    n_blocks = len(s) // 4 + 1

    for i in range(min(n_blocks, 7)):
        idx = 0
        blocks = []
        for j in range(n_blocks):
            if j == i:
                blocks.append(s[idx:idx+remaining_block_length])
                idx += remaining_block_length
            else:
                blocks.append(s[idx:idx+4])
                idx += 4
        res = (''.join([a85(b) for b in blocks]))
        print(res)