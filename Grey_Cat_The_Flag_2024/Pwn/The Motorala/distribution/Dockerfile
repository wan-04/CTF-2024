FROM ubuntu:22.04 AS app
FROM pwn.red/jail

COPY --from=app / /srv
COPY ./chall /srv/app/run
COPY ./pin /srv/app/pin
COPY ./flag.txt /srv/app/flag.txt

RUN chmod 444 /srv/app/flag.txt
RUN chmod +x /srv/app/run
