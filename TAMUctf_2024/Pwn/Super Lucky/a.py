randtbl = [38, 7719, 21238, 2437, 8855, 11797, 8365, 32285, 10450, 30612, 5853, 28100, 1142, 281, 20537, 15921, 8945]
fptr = 4
rptr = 1
for _ in range(7):
    new_sum = randtbl[fptr] + randtbl[rptr]
    new_rand = ((new_sum) >> 1) & 0x7fffffff
    print((new_rand))
    randtbl[fptr] = new_sum & 0xffffffff
    fptr += 1
    rptr += 1
