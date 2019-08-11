FROM python:3.6-alpine3.9

WORKDIR integration_tests
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./

EXPOSE 5000
CMD [ "pytest", "-s"]
