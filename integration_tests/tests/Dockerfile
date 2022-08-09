FROM python:3.10-alpine

WORKDIR project
COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD [ "pytest", "-s"]
