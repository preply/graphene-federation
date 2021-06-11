FROM python:3.8.10-alpine3.13

WORKDIR project
RUN apk add curl

COPY ./requirements.txt ./
COPY ./src/ ./src/
RUN pip install -r requirements.txt
RUN pip freeze

EXPOSE 5000
CMD ls -lh && python ./src/app.py
