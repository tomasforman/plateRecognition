FROM python:3

ADD ./ /app

RUN cd /app && pip install -r requirements.txt

ENV MQTT_PORT=1883
ENV MQTT_TOPIC=images
ENV PLATES_TOPIC=plates

CMD [ "python", "/app/Main.py" ]
