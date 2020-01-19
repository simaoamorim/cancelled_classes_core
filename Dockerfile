FROM alpine:latest as corebase

RUN apk add python3
RUN mkdir /core

FROM corebase
COPY ./src/*.py /core/
RUN mkdir /core/db
RUN chmod +x /core/*.py
EXPOSE 8080/tcp

WORKDIR /core/
CMD python3 ./main.py
