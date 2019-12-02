import json
import os

from PIL import Image
from io import BytesIO
import base64
import pytesseract
import re

import paho.mqtt.client as mqtt

PATTERN = "^[A-Z]{2}[0-9]{3}[A-Z]{2}$"
TEXT_TOPIC = os.getenv("TEXT_TOPIC")

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


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    img = payload["plate"]
    plate = extract_text(img)
    payload = '{"id": "' + id + '", "plate": "' + plate + '"}'
    client.publish(TEXT_TOPIC, payload)


mqtt_client = mqtt.Client()
mq_port = os.getenv('MQTT_PORT')
mq_host = os.getenv('MQTT_HOST')
mq_topic = os.getenv('MQTT_TOPIC')
mqtt_client.connect(host=mq_host, port=int(mq_port))
mqtt_client.subscribe(mq_topic)
mqtt_client.on_message = on_message
print("Waiting for messages .....")
mqtt_client.loop_forever()

