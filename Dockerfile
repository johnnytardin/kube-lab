FROM python:3.11.9-slim

WORKDIR /app

COPY . .

# hadolint ignore=DL3008,DL3013
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && poetry install --no-dev


CMD ["python", "run.py"]