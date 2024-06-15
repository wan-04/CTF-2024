#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <string.h>

#define DEFAULT_MMAP_SIZE (1024*1024*10) //10MB

#define PASSED 0
#define FAILED 1

static inline char page_hash(int page)
{
        return (char)(page % 256);
}

static inline char *page_offset_to_addr(char *start, int page)
{
        return start + (getpagesize() * page);
}

int genfile(char *file, const size_t size)
{
        ssize_t bytes = 0;
        int fd = 0;
        char *buf;
        int i, page;

        if (!mkstemp(file))
                return FAILED;

        fd = open(file, O_RDWR);
        if (fd == -1)
                return FAILED;

        buf = malloc( getpagesize() );

        printf("Writing out %d pages to %s\n", (int)(size / getpagesize()), file);

        for (page = 0 ; page < (size / getpagesize()) ; page++)
        {
                for (i = 0 ; i < getpagesize() ; i++)
                        buf[i] = page_hash(page);

                bytes += write(fd, buf, getpagesize());
        }
        close(fd);
        sync();
        return PASSED;
}

int compare(char *remapped_file, char *file, unsigned long size)
{
        char *mmap_orig_file;
        int i = 0, fd = open(file, O_RDONLY);
        int err = FAILED;

        if (!remapped_file || fd == -1)
                return FAILED;

        /* map in the file from disk, again */
        if ((mmap_orig_file =
             mmap(0, size, PROT_READ, MAP_SHARED, fd,
                  0)) == MAP_FAILED) {
                goto out_mmap_fail;
        }

        /* walk the original backwards and compare it to the remapped
         * file going forwards, page by page.  they should be the
         * same.
         */
        int cur_remap_page = 0;
        int cur_orig_page  = (size / getpagesize()) - 1;

        while (cur_orig_page >= 0)
        {
                printf("compare %05d -> %05d\r", cur_remap_page, cur_orig_page);
                if ((i = memcmp(page_offset_to_addr(mmap_orig_file, cur_orig_page),
                                page_offset_to_addr(remapped_file, cur_remap_page),
                                getpagesize()) != 0)) {
                        err = FAILED;
                        goto out;
                }
                cur_remap_page++;
                cur_orig_page--;
        }
        printf("\n");
        err = PASSED;
 out:
        munmap(mmap_orig_file, size);
 out_mmap_fail:
        close(fd);
        return err;
}

int main(void)
{
        int fd;
        const char *tmp_default = "/tmp/remap-testXXXXXX";
        size_t size = DEFAULT_MMAP_SIZE;
        char file[256], *addr;

        int err = FAILED;
        int sys_pagesize = getpagesize();

        strcpy(file, tmp_default);
        genfile(file, size);

        /*
         *  Map in the file
         */
        fd = open(file, O_RDWR);
        if ((addr =
             mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd,
                  0)) == MAP_FAILED)
                goto out;

        /* Turn the file around with remap_file_pages; that is the
         * last page of the file on disk becomes the first page in
         * memory, the second last page the second page in memory,
         * etc.
         */
        int cur_mmap_page = (size / sys_pagesize) - 1;
        int cur_file_page = 0;
        while (cur_mmap_page >= 0)
        {
                remap_file_pages(page_offset_to_addr(addr, cur_mmap_page),
                                 sys_pagesize, 0, cur_file_page, 0);
                cur_mmap_page--;
                cur_file_page++;
        }
        printf("\n%ldd\n%ldd\n%ldd\n%ldd\n", page_offset_to_addr(addr, cur_mmap_page), sys_pagesize, cur_file_page);


        err = compare(addr, file, size);
        if (err == FAILED)
                printf("Test Failed!\n");
        else
                printf("Test Passed!\n");
 out:
        close(fd);
        unlink(file);
        exit(err);
}