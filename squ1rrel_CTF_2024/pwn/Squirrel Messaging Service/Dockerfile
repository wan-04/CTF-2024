FROM ubuntu:20.04 
RUN apt update
RUN apt install -y socat
RUN /usr/sbin/useradd --no-create-home -u 1000 user

COPY flag.txt /
COPY sms /home/user/



COPY nsjail.cfg /home/user/

CMD   socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"/home/user/sms"
