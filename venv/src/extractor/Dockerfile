FROM python:3

ADD ./ /app

RUN apt update && apt upgrade

RUN apt install -y tesseract-ocr libtesseract-dev

RUN cd /app && pip install -r requirements.txt

ENV MQTT_PORT=1883
ENV MQTT_TOPIC=plates
ENV TEXT_TOPIC=text

CMD [ "python", "/app/Main.py" ]
