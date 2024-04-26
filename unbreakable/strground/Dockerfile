FROM ubuntu:22.04


RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y socat gcc netcat net-tools

RUN useradd ctf 

WORKDIR /home/ctf
COPY ./source /home/ctf/

RUN chmod +x /home/ctf/chall

EXPOSE 1337

USER ctf
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:./chall,stderr

# sudo docker compose --build up 
