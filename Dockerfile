FROM alpine:latest as corebase

RUN apk add python3
RUN mkdir /core

FROM corebase
COPY ./src/*.py /core
RUN chmod +x /core/*.py
EXPOSE 8080/tcp

CMD python3 /core/main.py