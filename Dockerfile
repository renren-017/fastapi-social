FROM python:3.10

ENV PYTHONBUFFERED 1

RUN mkdir /fastapi-social

WORKDIR /fastapi-social

COPY . .

RUN pip install -r requirements.txt


