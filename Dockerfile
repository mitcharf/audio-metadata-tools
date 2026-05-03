FROM python:3.14-slim

RUN mkdir -p /music /db /backups /logs

COPY . /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends make && \
    rm -rf /var/lib/apt/lists/* && \
	pip install -U pip setuptools && \
    pip install -e ".[dev]"

CMD ["tail", "-f", "/dev/null"]
