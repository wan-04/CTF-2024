FROM gcc:13.3.0

RUN apt-get update \
    && apt-get install --no-install-recommends -y socat

COPY . /usr/src/myapp

WORKDIR /usr/src/myapp

COPY challenge flag.txt ./

EXPOSE 14124

CMD socat -T60 TCP-L:14124,fork,reuseaddr EXEC:"./challenge",pty,stderr,setsid,sane,raw,echo=0
