FROM python:3.14-slim

# Run commands up front that are less likely to change during
# development, so the docker layer can be cached, speeding up
# future Docker builds during development
RUN mkdir -p /music /db /backups /logs && \
	apt-get update && \
    apt-get install -y --no-install-recommends make && \
    rm -rf /var/lib/apt/lists/* && \
	pip install -U pip setuptools

COPY . /app
WORKDIR /app
RUN pip install -e ".[dev]"

CMD ["tail", "-f", "/dev/null"]
