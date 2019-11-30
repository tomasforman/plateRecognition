FROM python:3.7.5

RUN mkdir /app
ADD . /app
RUN pip install -r /app/requirements.txt

ENV MQTT_PORT=127.0.0.1
CMD python /app/Main.py