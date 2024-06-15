import numpy as np
from PIL import Image
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

def path_to_moves_aggregated(path):
    moves = []
    directions = {
        (0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right",
        (-1, -1): "up-left", (-1, 1): "up-right", (1, -1): "down-left", (1, 1): "down-right"
    }
    
    count = 1
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        move = (x2 - x1, y2 - y1)
        
        if moves and moves[-1] == directions[move]:
            count += 1
            if count == 4:
                count = 1
                moves.append(directions[move])
        else:
            count = 1
            moves.append(directions[move])

def draw_path(img, path):
    pixels = img.load()
    for (x, y) in path:
        pixels[x, y] = (218, 165, 32)  # blue
    img.save("solved_maze.png")

# Load the image
image_path = "image.png"
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
    moves = path_to_moves_aggregated(path)
    # with open("moves.txt", "w") as f:
    #     f.write(" ".join(moves))
    # print("Moves written to moves.txt")
    draw_path(img, path)
    print("Path found and drawn on solved_maze.png")