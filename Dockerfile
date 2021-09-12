FROM python:3.7-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT bash