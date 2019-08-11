FROM python:3.6-alpine3.9

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src/ src/

EXPOSE 5000
CMD [ "python", "src/app.py"]
