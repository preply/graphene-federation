FROM python:3.8.10-alpine3.13

WORKDIR project
COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD [ "pytest", "-s"]
