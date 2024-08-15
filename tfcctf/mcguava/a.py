import threading
import subprocess

# Định nghĩa một hàm để chạy file .py khác
def run_another_py_file(file_path):
    subprocess.call(['python', file_path])

# Số lượng thread bạn muốn chạy
num_threads = 10

# Đường dẫn tới file .py bạn muốn chạy
file_to_run = './solve.py'

# Tạo và khởi chạy các thread
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=run_another_py_file, args=(file_to_run,))
    threads.append(thread)
    thread.start()

# Chờ cho tất cả các thread hoàn thành
for thread in threads:
    thread.join()