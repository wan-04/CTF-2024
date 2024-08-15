import random
import numpy as np
import math
array_2d = np.zeros((25, 25))


def create_hidden_point():
    # Margin to ensure doesnt spawn on edge
    return (random.randint(10000, 100000-10000), random.randint(10000, 100000-10000))


def is_hit(hidden_point, center, radius):
    x, y = center
    hx, hy = hidden_point
    return (x - radius <= hx <= x + radius) and (y - radius <= hy <= y + radius)


h = create_hidden_point()
points = []
r = 250000

for i in range(10):
    g = create_hidden_point()
    if is_hit(h, g, r):
        for angle in range(0, 360, 90):
            x = g[0] + r * math.cos(math.radians(angle))
            y = g[1] + r * math.sin(math.radians(angle))
            x = x if x > 0 else 0
            y = y if y > 0 else 0
            points.append((int(x), int(y)))
        print(points)
        