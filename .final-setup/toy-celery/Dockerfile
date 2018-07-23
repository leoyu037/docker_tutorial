FROM python:3.6-alpine

ENV DIR /srv
WORKDIR ${DIR}

# Install system dependencies
RUN apk add --update --no-cache \
        bash \
        curl \
        postgresql-dev && \
    rm -rf /var/cache/apk/*

# Install psycopg2
RUN apk add --update --no-cache --virtual build-dependencies \
        gcc musl-dev && \
    pip install psycopg2 && \
    apk del build-dependencies

# Install python dependencies
COPY ./setup.py ${DIR}/
RUN pip install -e .

# Copy source code
COPY ./toy_app/ ${DIR}/toy_app/
COPY ./scripts/ ${DIR}/scripts/

CMD ["./scripts/start-celery.sh"]
