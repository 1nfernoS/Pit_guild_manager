FROM tiangolo/meinheld-gunicorn-flask:python3.7-alpine3.8
ENV TZ="Europe/Moscow"

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache jpeg-dev zlib-dev libjpeg mariadb-dev freetype-dev tzdata
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

RUN apk del build-deps

COPY cron-tasks /etc/crontabs/root