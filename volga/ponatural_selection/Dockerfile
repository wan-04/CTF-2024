FROM ubuntu:23.04@sha256:5a828e28de105c3d7821c4442f0f5d1c52dc16acf4999d5f31a3bc0f03f06edd as chroot

RUN apt-get -y update --fix-missing
RUN apt-get -y upgrade
RUN apt-get -y update --fix-missing
RUN apt-get -y install socat python3 python3-pip bc bsdmainutils
RUN groupadd -r ctf && useradd -r -g ctf ctf

USER ctf
CMD socat TCP-L:8109,reuseaddr,fork EXEC:"./ponatural_selection"
EXPOSE 8109