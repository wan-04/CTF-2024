# safe_link_double_protect

- Safe-linking được giới thiệu ở bản glibc 2.32 như một lớp bảo vệ linked-list của tcache.
- Khi một chunk được thêm vào tcache bin, chunk đó sẽ dịch 12 bit và xor với chunk trước đó.

```
chunk >> 12 ^ prev_chunk = key
```
- Thông thường, tôi sẽ cố gắng leak heap để tìm key nhưng ở kĩ thuật này. Chúng ta cần control metadata tcache