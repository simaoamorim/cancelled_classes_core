FROM alpine

RUN mkdir /core
COPY src/ /core/
WORKDIR /core
RUN apk add python3
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN chmod +x ./*.py

CMD python3 ./start.py