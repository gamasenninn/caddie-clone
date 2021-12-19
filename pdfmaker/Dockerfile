FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY /app /app

RUN apt-get update && apt-get install -y vim
RUN apt-get install -y git
RUN pip install reportlab