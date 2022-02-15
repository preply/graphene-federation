FROM python:3.8.10-alpine3.13 AS deps

RUN apk add curl \
 && python -m pip install --upgrade pip \
 && mkdir -p /opt/service \
 && mkdir -p /opt/lib

FROM deps AS python-deps
WORKDIR /opt/service
COPY ./requirements.txt ./
RUN pip install -r requirements.txt \
 && pip freeze

FROM python-deps AS base
ENV GRAPHENE_FEDERATION_INTEGRATION_TEST_SERVICE=""
WORKDIR /opt/service
COPY ./src/ ./
EXPOSE 5003
CMD ["ls", "-lh", "&&", "uvicorn", "--host 0.0.0.0", "--port 5003", "--reload", "--log-level debug", "app:app"]
