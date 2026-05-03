FROM python:3.14-slim

RUN mkdir -p /music /db /backups /logs

COPY . /app
WORKDIR /app

RUN pip install -e ".[dev]"

CMD ["tail", "-f", "/dev/null"]
