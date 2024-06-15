# HOUSE OF WATER (HOW)

## Giới thiệu

- House of Water được viết bởi @udp_ctf - Water Paddler / Blue Water là một kĩ thuật sử dụng UAF để tạo 1 chunk trong tcache metadata. Khi đó ta có thể malloc các chunk mà ta thích.

## BUG

- Điều mà mình thấy khá thú vị ở kĩ thuật này ở việc sử dụng chính metadata của tcache để tạo 1 fake chunk. Nói sơ qua thì ở các libc mới đây, đã bổ sung một chunk (được gọi là tcache metadata) trong heap để lưu trữ số lượng chunk và linked list của chunk được free vào tcache. Trong metadata ấy được chia 2 vùng, một vùng để lưu số lượng chunk đc free trong bin của từng size và một vùng ngay dưới đó chứa con trỏ của các chuck được free. Nhưng bug ở đây là việc 2 vùng này nằm liền kề nhau khiến cho ta có thể tạo 1 fake chunk với size là 0x10001
- Để đọc kĩ hơn về kĩ thuật này, các bạn có thể đọc ở đây https://github.com/shellphish/how2heap/blob/master/glibc_2.35/house_of_water.c, được tóm tắt theo hướng sau:
- free 0x3e0 and 0x3f0 để set các byte số lượng của 2 chunk này trong metadata là 1 `010001`
- đưa 3 chunk 0x90 vào unsorted-bin
- free 2 chunk 0x20 0x30 để làm FWD và BCK cho fake chunk

## Mô phỏng
- Giải
