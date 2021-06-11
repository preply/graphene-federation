FROM python:3.8.10-alpine3.13

WORKDIR project
RUN apk add curl
RUN apk add tree

COPY ./ ./

RUN pip install -r requirements.txt
RUN ls -lh
RUN pip install $(ls -t | grep *.whl | head -n1)

EXPOSE 5003
CMD tree . && cd ./src/django_project/ && python manage.py runserver 5003
