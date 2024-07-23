FROM ubuntu@sha256:ac58ff7fe25edc58bdf0067ca99df00014dbd032e2246d30a722fa348fd799a5

RUN apt-get update
RUN apt-get install -y qemu qemu-system-x86 qemu-utils socat cpio gzip wget 

EXPOSE 1337

RUN useradd -d /home/ctf -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd
RUN ulimit -c 0

WORKDIR /home/ctf


USER ctf
CMD socat tcp-l:1337,reuseaddr,fork EXEC:"/bin/sh",pty,stderr