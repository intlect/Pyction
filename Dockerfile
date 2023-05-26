FROM python:3.9-slim-buster

WORKDIR /app

COPY app /app

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
