import struct

def big_to_little_endian(value):
    # Convert the value from big endian to little endian
    little_endian = struct.pack('>Q', value)
    little_endian_value = struct.unpack('<Q', little_endian)[0]
    return little_endian_value

# Example usage
value = 0xB03B5FEB005F0000
little_endian_value = big_to_little_endian(value)
print("Big Endian Value:", (little_endian_value))
print("Little Endian Value:", hex(little_endian_value))