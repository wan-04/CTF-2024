#include <unistd.h>
#include <fcntl.h>
#include <sys/syscall.h>

#define __NR_openat2 437

int main()
{
    int dirfd = AT_FDCWD;                // Thay đổi thành file descriptor thư mục của bạn
    const char *pathname = "./flag.txt"; // Thay đổi thành đường dẫn tới file của bạn

    long long how[4];
    how[0] = 0;
    how[1] = 0;
    how[2] = 0;
    how[3] = 0;
    how[0] = O_RDONLY;
    int fd = syscall(__NR_openat2, dirfd, pathname, how, sizeof(how));
    // rsi 0xffffff9c, rdx = flag.txt, rcx = 0, r8 = 0x29
    if (fd == -1)
    {
        // Xử lý lỗi
        perror("sys_openat2");
        return 1;
    }

    // File đã được mở thành công
    // Tiếp tục xử lý tại đây

    return 0;
}


// #include <unistd.h>
// #include <sys/uio.h>
// #include <string.h>
// #include <stdio.h>
// int main() {
//     int fd = open("flag.txt", O_WRONLY);  // Mở file để ghi

//     if (fd == -1) {
//         // Xử lý lỗi khi không mở được file
//         perror("open");
//         return 1;
//     }

//     const char* buffer1 = "Hello, ";
//     size_t buffer1_len = strlen(buffer1);

//     const char* buffer2 = "world!";
//     size_t buffer2_len = strlen(buffer2);

//     struct iovec iov[2];
//     iov[0].iov_base = (void*)buffer1;
//     iov[0].iov_len = buffer1_len;
//     iov[1].iov_base = (void*)buffer2;
//     iov[1].iov_len = buffer2_len;

//     ssize_t bytes_written = writev(fd, iov, 2);
//     if (bytes_written == -1) {
//         // Xử lý lỗi khi không thể ghi dữ liệu
//         perror("writev");
//         return 1;
//     }

//     // Ghi dữ liệu thành công
//     printf("Đã ghi %zd byte vào file.\n", bytes_written);

//     close(fd);  // Đóng file

//     return 0;
// }