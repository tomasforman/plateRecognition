FROM python:3

ADD ./ /app

RUN apt update && apt upgrade

RUN apt install -y tesseract-ocr libtesseract-dev

RUN cd /app && pip install -r requirements.txt

ENV RABBITMQ_HOST=127.0.0.1

CMD [ "python", "/app/Main.py" ]
