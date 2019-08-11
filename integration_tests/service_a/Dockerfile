FROM python:3.6-alpine3.9

WORKDIR service_a

COPY integration_tests/service_a/requirements.txt ./
COPY ./ federation_deps/
RUN pip install -r requirements.txt
RUN pip install federation_deps/

COPY integration_tests/service_a/src/ ./src/

EXPOSE 5000
CMD [ "python", "./src/app.py"]
