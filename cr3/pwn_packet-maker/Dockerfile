FROM ubuntu:22.04

RUN apt update && apt install -y socat
RUN useradd ctf

ADD ./packet-maker /home/ctf/
ADD ./flag.txt /

RUN chmod 755 /home/ctf/packet-maker
RUN chmod 444 /flag.txt
RUN chown -R root:ctf /home/ctf

CMD socat -T60 -t60 tcp-l:10001,reuseaddr,fork EXEC:"/home/ctf/packet-maker",su=ctf
