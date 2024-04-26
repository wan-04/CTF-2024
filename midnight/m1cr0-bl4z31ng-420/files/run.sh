#!/bin/bash
qemu-system-microblazeel  -m 256 -serial mon:stdio -display none  -kernel linux.bin -initrd initrd.image.gz -nographic -M petalogix-s3adsp1800 -net user,hostfwd=tcp::4040-:4040 -net nic


