FROM python:3.8-slim

# Disable Python buffering in order to see the logs immediatly
ENV PYTHONUNBUFFERED=1

# Set the default working directory
WORKDIR /workdir

COPY . /workdir

# Install dependencies
RUN pip install -e ".[dev]"

CMD tail -f /dev/null
