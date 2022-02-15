FROM python:3.8-slim AS deps
ENV POETRY_VERSION=1.1.13
RUN apt-get update \
 && apt-get install -y build-essential python3-setuptools \
 && mkdir -p /opt/graphene_federation/

FROM deps AS python-deps
WORKDIR /opt/graphene_federation
COPY pyproject.toml poetry.lock ./
RUN pip install "poetry==$POETRY_VERSION" \
 && pip install --upgrade pip setuptools \
 && poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi


FROM python-deps AS base
# Disable Python buffering in order to see the logs immediatly
ENV PYTHONUNBUFFERED=1

# Set the default working directory
WORKDIR /opt/graphene_federation
COPY . /workdir

# Install dependencies
RUN poetry install
CMD ["tail", "-f", "/dev/null"]
