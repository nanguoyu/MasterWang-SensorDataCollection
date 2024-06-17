FROM python:3.8-slim

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir flask pymongo

EXPOSE 5000

ENV NAME World

CMD ["python", "app.py"]
