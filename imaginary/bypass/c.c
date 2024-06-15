// Implementation of Murmur hash for 64-bit size_t.
size_t
_Hash_bytes(const void *ptr, size_t len, size_t seed)
{
    static const size_t mul = (((size_t)0xc6a4a793UL) << 32UL) + (size_t)0x5bd1e995UL;
    const char *const buf = static_cast<const char *>(ptr);

    // Remove the bytes not divisible by the sizeof(size_t).  This
    // allows the main loop to process the data as 64-bit integers.
    const size_t len_aligned = len & ~(size_t)0x7;
    const char *const end = buf + len_aligned;
    size_t hash = seed ^ (len * mul);
    for (const char *p = buf; p != end; p += 8)
    {
        const size_t data = shift_mix(unaligned_load(p) * mul) * mul;
        hash ^= data;
        hash *= mul;
    }
    if ((len & 0x7) != 0)
    {
        const size_t data = load_bytes(end, len & 0x7);
        hash ^= data;
        hash *= mul;
    }
    hash = shift_mix(hash) * mul;
    hash = shift_mix(hash);
    return hash;
}


/*
seed = 0xC70F6907
*/