#include <fcntl.h>
#include <stdio.h>

int main() {
    // Mở tệp tin "data.txt" trong thư mục gốc
    int dirfd = AT_FDCWD;
    const char *pathname = "flag";
    int flags = 300;
    int fd = openat(dirfd, pathname, flags);
    printf(AT_FDCWD);
    // printf("AT_FDCWD");
    // Kiểm tra xem tệp tin có được mở thành công hay không
    if (fd == -1) {
        perror("openat");
        return 1;
    }

    // Đóng tệp tin
    close(fd);

    return 0;
}