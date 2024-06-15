FROM ubuntu:22.04

RUN apt-get update -y
RUN apt-get install -y xinetd

RUN useradd -mU ticket

COPY ./flag.txt /flag
COPY ./share/ticket /home/ticket/ticket
COPY ./xinetd /etc/xinetd.d/ipc

RUN chmod 750 /home/ticket /home/ticket/ticket
RUN chown -R root:ticket /home/ticket

CMD ["/usr/sbin/xinetd","-dontfork"]
