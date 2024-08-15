x_max, y_max, x_min, y_min = (x+r)/2, (y+r)/2, (x-r)/2, (y-r)/2
x_a, y_a = x, y
x_o, y_o = x_max, y_max
for i in range(3):
    if (x > 0):
        x_o = x_min
    if (y > 0):
        y_o = y_min
    r = abs(math.sqrt((x_a - x)**2 + (y_a - y)**2) + math.sqrt((x_o - x)**2 + (y_o - y)**2))