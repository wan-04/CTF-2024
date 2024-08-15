import threading
import subprocess

def run_script():
    # Thay đổi đường dẫn tới file Python cần chạy ở đây
    script_path = "a.py"
    
    # Chạy file Python bằng subprocess
    subprocess.run(["python", script_path])

def run_with_threads(num_threads):
    threads = []
    
    for _ in range(num_threads):
        thread = threading.Thread(target=run_script)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    num_threads = 10
    run_with_threads(num_threads)