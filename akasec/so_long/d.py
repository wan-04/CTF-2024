from PIL import Image
import numpy as np
def find_color_pixels(image_array, color):
    color_pixels = []
    for row in range(image_array.shape[0]):
        for col in range(image_array.shape[1]):
            if np.all(image_array[row, col] == color):
                color_pixels.append((row, col))
    return color_pixels

# Load the image
image_path = 'image.png'  # Đường dẫn đến tệp ảnh của bạn
image = Image.open(image_path)
image = image.convert('RGB')  # Chuyển đổi sang chế độ màu RGB

# Chuyển đổi ảnh thành mảng numpy
image_array = np.array(image)

# Màu sắc điểm bắt đầu và điểm kết thúc (ở đây ví dụ màu xanh và màu đỏ)
start_color = (0, 255, 0)  # Màu xanh (R, G, B)
end_color = (255, 0, 0)  # Màu đỏ (R, G, B)

# Tìm kiếm các điểm ảnh có màu sắc tương ứng
start_pixels = find_color_pixels(image_array, start_color)
end_pixels = find_color_pixels(image_array, end_color)

# In ra tọa độ của các điểm bắt đầu và điểm kết thúc
print("Các điểm bắt đầu:")
for pixel in start_pixels:
    print(pixel)
print("Các điểm kết thúc:")
for pixel in end_pixels:
    print(pixel)