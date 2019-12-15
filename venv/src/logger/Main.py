import os

import pika
from pymongo import MongoClient
import json

S3_DNS = "https://prs-plates.s3.amazonaws.com"

client = MongoClient()
db = client.plates
plates = db.plates

def callback(ch, method, properties, msg):
    payload = json.loads(msg)
    id = payload["id"]
    [camera_id, timestamp] = id.split("@")
    plate = {
        'plate': payload["plate"],
        'timestamp': timestamp,
        "camera": camera_id,
        "url": f"{S3_DNS}/{id}.jpg"
    }
    plates.insert_one(plate)


mq_host = os.getenv('RABBITMQ_HOST')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=mq_host))
channel = connection.channel()

channel.queue_declare(queue='plate')
channel.basic_consume(queue='plate', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()