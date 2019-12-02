#!/bin/bash

# clean up
docker stop mq;
docker rm mq;
docker rmi detector;
docker rmi extractor;

# run MQTT
docker run -d --name mq -p 1883:1883 -p 9001:9001  eclipse-mosquitto;
MQ_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mq);
echo $MQ_IP;

# build images
docker build -t detector ./dectector
docker build -t extractor ./extractor

# run containers
docker run -d -e MQTT_HOST="${MQ_IP}" detector;
docker run -d -e MQTT_HOST="${MQ_IP}" extractor
