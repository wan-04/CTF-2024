import threading
import os
import time
def execute_file():
    os.system('python3 solve.py REMOTE')

threads = []

for _ in range(10):
    thread = threading.Thread(target=execute_file)
    threads.append(thread)
    thread.start()
    time.sleep(5)
    

for thread in threads:
    thread.join()