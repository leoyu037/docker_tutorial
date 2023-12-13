FROM python:3.6-alpine

WORKDIR /app

# Install python dependencies
COPY setup.py setup.py
RUN pip install -e .

# Copy source code
COPY app.py app.py

CMD exec flask run -h 0.0.0.0 -p 80
