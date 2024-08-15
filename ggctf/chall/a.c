#include <stdint.h>
#include <stdio.h>
uint8_t BYTE1(uint32_t value) {
    return (value >> 16) & 0xFF;
}

uint8_t BYTE2(uint32_t value) {
    return (value >> 8) & 0xFF;
}

uint8_t BYTE3(uint32_t value) {
    return value & 0xFF;
}
uint8_t reverse_alphabet[1000] = {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 255, 255, 255, 255, 84, 255, 255, 255, 85, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int64_t decode85(uint8_t *plain, uint8_t *plt, uint64_t *a3, uint64_t len)
{
    uint64_t v5;
    uint64_t v6;
    uint64_t v7;
    uint64_t v8;
    uint8_t v9;
    int j;
    uint64_t v11;
    uint64_t i;
    uint64_t v13;

    v13 = 0;
    if (len % 5 != 0)
        return 0;
    for (i = 0; i < len; i += 5)
    {
        v11 = 0;
        for (j = 4; j >= 0; --j)
        {
            v9 = reverse_alphabet[*(uint8_t *)(i + j + plt)];
            if (v9 == 0xFF)
                return 0;
            v11 = v9 + 85 * v11;
        }
        if (v11 > 0x1010100FF)
            return 0;
        if (v13 >= *a3)
            return 0;
        *(uint8_t *)(plain + v13) = v11;
        v5 = v13++;
        if (v11 <= 0x10100FFFF)
        {
            if (v13 >= *a3)
                return 0;
            *(uint8_t *)(plain + v13) = BYTE1(v11);
            v6 = v13++;
            if (v11 <= 0x100FFFFFF)
            {
                if (v13 >= *a3)
                    return 0;
                *(uint8_t *)(plain + v13) = BYTE2(v11);
                v7 = v13++;
                if (v11 <= 0xFFFFFFFF)
                {
                    if (v13 >= *a3)
                        return 0;
                    *(uint8_t *)(plain + v13) = BYTE3(v11);
                    v8 = v13++;
                }
            }
        }
    }
    if (4 * (len / 5) - 4 >= v13)
        return 0;
    if (v13 >= *a3)
        return 0;
    *(uint8_t *)(plain + v13) = 0;
    *a3 = v13;
    return 1;
}

// Khai báo hàm decode85 ở đây

int main()
{
    // Chuỗi encoded_data là dữ liệu đã được mã hóa Ascii85
    uint8_t encoded_data[] = "N2Qab";
    uint8_t decoded_data[1000]; // Mảng để lưu dữ liệu đã giải mã
    uint64_t decoded_length = sizeof(decoded_data);
    uint64_t len = 1024;
    // Gọi hàm decode85 để giải mã dữ liệu
    int result = decode85(decoded_data, encoded_data, &len, decoded_length);
    if (result)
    {
        printf("Decoded data: %s\n", decoded_data);
        printf("Decoded length: %lu\n", decoded_length);
    }
    else
    {
        printf("Decoding failed.\n");
    }

    return 0;
}