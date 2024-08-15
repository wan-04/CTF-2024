import math
import random
import numpy as np
grid_size = 1000000
array_2d = np.zeros((100, 100))
array_2d.fill(0)

GRID_SIZE = 1000000

# Số vòng chơi
NUM_ROUNDS = 100

# Tạo một điểm ngẫu nhiên trong lưới


def random_point():
    return (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

# Kiểm tra xem hidden point có nằm trong hình vuông không


def is_hit(hidden_point, center, radius):
    x, y = center
    hx, hy = hidden_point
    return (x - radius <= hx <= x + radius) and (y - radius <= hy <= y + radius)


# for i in range(5):
#     hidden_point = (2, 2)
#     guessed_point = (7, 3)
#     print(hidden_point)
#     print(guessed_point)
#     print("> ")
#     r = int(input())
#     # tolerance = GRID_SIZE * 0.01


#     if is_hit(hidden_point, guessed_point, r):
#         print("Success: Dự đoán chính xác!")
#     else:
#         print("Failure: Dự đoán sai.")


def random_point():
    return (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))


def is_hit(hidden_point, center, radius):
    x, y = center
    hx, hy = hidden_point
    return (x - radius <= hx <= x + radius) and (y - radius <= hy <= y + radius)


hidden_point = random_point()
for i in range(100):
    guess_point = random_point()
    r = 500000
    print(guess_point)
    x_max, y_max, x_min, y_min = guess_point[0] + \
        r, guess_point[1]+r, guess_point[0]-r, guess_point[1]-r
    # print(x, y_max//10000, x_min//10000, y_min//10000)
    if is_hit(hidden_point, guess_point, r):
        # print("Success: Dự đoán chính xác!")
        for i in range(y_min//20000, y_max//20000):
            for j in range(x_min//20000, x_max//20000):
                array_2d[i, j] += 1
    else:
        print("Failure: Dự đoán sai.")
max_index = np.argmax(array_2d)
y, x = np.unravel_index(max_index, array_2d.shape)
print(hidden_point)
print("Tọa độ (hàng, cột) của giá trị lớn nhất:", x*20000, y*20000)
