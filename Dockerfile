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
    poetry config virtualenvs.create false && poetry install --no-dev && \
    groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "run.py"]