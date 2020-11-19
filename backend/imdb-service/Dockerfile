FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

COPY src /app

RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install IMDbPY
