# syntax=docker/dockerfile:1
FROM python:3.10-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

ARG USERID
ARG GROUPID
RUN adduser --disabled-password --gecos "" -u $USERID user
USER user