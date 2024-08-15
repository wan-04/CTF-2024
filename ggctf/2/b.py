value = 16777215
byte_value = value.to_bytes(3, 'big')  # Chuyển đổi thành byte với 3 byte và byte order là 'big'

with open("key", "wb") as file:
    file.write(byte_value)