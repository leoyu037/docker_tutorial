FROM python:3-alpine

ENV DIR /srv
WORKDIR ${DIR}

# Install system dependencies
RUN apk add --update --no-cache \
        bash \
        curl && \
    rm -rf /var/cache/apk/*

# Install python dependencies
COPY ./setup.py ${DIR}/
RUN pip install -e .

# Copy source code
COPY ./toy_app/ ${DIR}/toy_app/
COPY ./scripts/ ${DIR}/scripts/

CMD ["./scripts/start-celery.sh"]
