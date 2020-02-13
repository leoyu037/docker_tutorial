FROM python:3.8-slim as base-image

WORKDIR /app

# Install Python dependencies
COPY setup.py setup.py
RUN pip install -e .

# ------------------------------------------------------------------------------

FROM base-image as unit-test-image

# Install test dependencies
RUN pip install -e '.[testing]'

# Copy source code
COPY app.py app.py

# Copy test code and run tests. Build won't continue unless tests pass
COPY tests/ tests/
RUN pytest tests/

# ------------------------------------------------------------------------------

FROM base-image as final-image

# Copy source code
COPY app.py app.py

CMD exec flask run -h 0.0.0.0 -p 80

EXPOSE 80
