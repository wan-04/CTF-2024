import hashlib
from tqdm import tqdm

target_hash = "cbd4cdd046820600f68ff86ea41e35c46653c14564ec0e9571c00e0eed913b97"
suffix = "g4feS8TH0uUpPWKlkBsc0/LUz1WmO4Nt"

found = False
total_iterations = 0xffffffff  # Số lần lặp tối đa

with tqdm(total=total_iterations, ncols=80, unit="iter") as pbar:
    for XXXX in range(total_iterations):
        value = str(XXXX)
        hash_input = value + suffix
        hashed_value = hashlib.sha256(hash_input.encode()).hexdigest()

        if hashed_value == target_hash:
            found = True
            break

        pbar.update(1)  # Cập nhật thanh tiến trình

if found:
    print("Tìm thấy giá trị XXXX:", XXXX)
else:
    print("Không tìm thấy giá trị XXXX sau", total_iterations, "lần lặp.")