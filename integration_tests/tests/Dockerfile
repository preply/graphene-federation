FROM python:3.6-alpine3.9

RUN pip install --upgrade pip

WORKDIR project
COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD [ "pytest", "-s"]
