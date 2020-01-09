FROM python:3.6-alpine3.9

WORKDIR project
RUN apk add curl

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python", "./src/app.py"]
