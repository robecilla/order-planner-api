FROM python:3.8

WORKDIR /api

ADD . /api

RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]
