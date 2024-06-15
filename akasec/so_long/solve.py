#!/usr/bin/python3

from pwn import *
import numpy as np
from PIL import Image
import io
from base64 import *
import math
# exe = ELF('a.py', checksec=False)

# context.binary = exe


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)
def sln(msg, num): return sla(msg, str(num).encode())
def sn(msg, num): return sa(msg, str(num).encode())


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''


        c
        ''')
        input()


if args.REMOTE:
    p = remote('20.80.240.190', 4442)
# else:
    # p = process(exe.path)
GDB()


def img_to_pixel(image_path):
    img = Image.open(image_path)
    pixel = img.load()
    pixel_of_image = []
    for x in range(img.size[0]):
        out = []
        for y in range(img.size[1]):
            r, g, b = pixel[x, y]
            out.append("[" + str(r) + "," + str(g) + "," + str(b) + "] ")
        pixel_of_image.append(out)
    return pixel_of_image


def downsample_image(image_path, factor):
    img = Image.open(image_path)
    arr = np.array(img)
    print(img.width,img.height )
    # Calculate new dimensions
    new_width = img.width // factor
    new_height = img.height // factor

    # Create a new array to store the downsampled image
    downsampled_arr = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    for i in range(new_height):
        for j in range(new_width):
            # Get the 4x4 block
            block = arr[i*factor:(i+1)*factor, j*factor:(j+1)*factor]

            # Calculate the mean value of the block
            mean_val = block.mean(axis=(0, 1))

            # Assign the mean value to the downsampled array
            downsampled_arr[i, j] = mean_val

    # Create an Image from the downsampled array
    downsampled_image = Image.fromarray(downsampled_arr)
    downsampled_image.save("downsampled_image.png")

    return downsampled_image

def count_pixels(image_path):
    image = Image.open(image_path)
    # Chuyển đổi ảnh sang chế độ RGB
    image = image.convert("RGB")

    # Đếm số lượng pixel có giá trị nhất định
    count = 0
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if pixel == (255, 0, 0):
                count += 1
    return count

from collections import deque

def load_image(image_path):
    img = Image.open(image_path)
    return img

def find_start_end(img):
    start = None
    end = None
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y][:3]
            if (r, g, b) == (0, 255, 0):  # green
                start = (x, y)
            elif (r, g, b) == (255, 0, 0):  # red
                end = (x, y)
    return start, end

def convert_to_binary_maze(img):
    pixels = img.load()
    width, height = img.size
    maze = np.zeros((height, width), dtype=int)
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y][:3]
            if (r, g, b) == (0, 0, 0):  # black
                maze[y, x] = 1
            else:
                maze[y, x] = 0
    return maze

def bfs(maze, start, end):
    rows, cols = maze.shape
    queue = deque([(start, [start])])
    visited = set()
    visited.add(start)
    
    # Directions: up, down, left, right, up-left, up-right, down-left, down-right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    direction_names = ["move up", "move down", "move left", "move right", 
                       "move up-left", "move up-right", "move down-left", "move down-right"]

    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == end:
            return path
        
        for direction, name in zip(directions, direction_names):
            nx, ny = x + direction[0], y + direction[1]
            
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny, nx] == 0 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
                
    return None

def path_to_moves(path):
    moves = []
    directions = {
        (0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right",
        (-1, -1): "up-left", (1, -1): "up-right", (-1, 1): "down-left", (1, 1): "down-right"
    }
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        move = (x2 - x1, y2 - y1)
        moves.append(directions[move])
    
    return moves

def draw_path(img, path):
    pixels = img.load()
    for (x, y) in path:
        pixels[x, y] = (218, 165, 32)  # blue
    img.save("solved_maze.png")

for i in range(1000):
    p.recvuntil(b'1000:')
    b64 = p.recvuntil(b'Enter', drop=True)

    byte_data = b64decode(b64)
    byte_stream = io.BytesIO(byte_data)
    image = Image.open(byte_stream)
    image.save("image.png")

    factor = math.sqrt(count_pixels("image.png"))
    print(factor)
    # Downsample the image by a factor of 4
    downsampled_image = downsample_image("image.png", int(factor))

    # Load the image
    image_path = "downsampled_image.png"
    img = load_image(image_path)

    # Find start (green) and end (red) points
    start, end = find_start_end(img)
    if start is None or end is None:
        raise ValueError("Start or end point not found in the maze")

    # Convert image to binary maze
    maze = convert_to_binary_maze(img)

    # Find the path using BFS
    path = bfs(maze, start, end)
    if path is None:
        print("No path found from start to end")
    else:
        # # Convert the path to moves
        moves = path_to_moves(path)
        with open("moves.txt", "w") as f:
            f.write(" ".join(moves))
        with open("moves.txt", "r") as f:
            res = f.read()
        sla(b'moves:', res)
    


p.interactive()