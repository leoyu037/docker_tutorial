FROM python:3-alpine

WORKDIR /app

COPY setup.py setup.py
RUN python setup.py install

COPY app.py app.py

CMD flask run -h 0.0.0.0 -p 80
