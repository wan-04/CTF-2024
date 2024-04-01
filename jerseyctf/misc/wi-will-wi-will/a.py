file = open('a.txt', 'w')
for i in range(0, 0x10000000000):
    res = hex(i)[2:]
    file.write(res)