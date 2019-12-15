import json
import os

from PIL import Image
from io import BytesIO
import base64
import pytesseract
import re

import pika

PATTERN = "^[A-Z]{2}[0-9]{3}[A-Z]{2}$"
TEXT_TOPIC = "text"

def extract_text(base4):
    img = Image.open(BytesIO(base64.b64decode(base4)))
    raw = pytesseract.image_to_string(img)
    if re.match(PATTERN, raw):
        return raw
    clean = re.findall("[A-Z0-9]", raw)
    clean_string = "".join(clean)
    (first, second, third) = re\
        .match(r"([A-Z]+)([0-9]+)([A-Z]+)", clean_string)\
        .groups()
    return first[-2:] + second + third[:2]


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    payload = json.loads(body)
    img = payload["plate"]
    plate = extract_text(img)
    payload_to_send = '{"id": "' + payload['id'] + '", "plate": "' + plate + '"}'
    print(payload_to_send)
    ch.basic_publish(exchange='', routing_key='text', body=payload_to_send)


mq_host = os.getenv('RABBITMQ_HOST')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=mq_host))
channel = connection.channel()

channel.queue_declare(queue='plate')
channel.basic_consume(queue='plate', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
