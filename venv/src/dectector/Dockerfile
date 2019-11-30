FROM python:3

ADD ./ /app

RUN apt update && apt upgrade

RUN cd /app && pip install -r requirements.txt

ENV MQTT_HOST=172.17.0.2
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=images


CMD [ "python", "/app/Main.py" ]
