import json
import os

import requests
import time
import re

from paho import mqtt

SECRET_KEY = 'sk_558e7c9c0cfe79e0b6682a4b'
PATTERN = "^[A-Z]{2}[0-9]{3}[A-Z]{2}$"
URL = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % SECRET_KEY


def on_message(client, userdata, msg):
    start = time.time()
    payload = json.loads(msg.payload)
    img = payload["plate"]
    r = requests.post(URL, data=img)
    resp = r.json()
    candidates = resp["results"][0]["candidates"]
    filtered = list(filter(lambda c: re.match(PATTERN, c['plate']), candidates))
    plate = filtered[0]["plate"]
    print(plate)
    print(time.time() - start)
    payload = '{"id": "' + id + '", "plate": "' + plate + '"}'
    client.publish("text", payload)


mqtt_client = mqtt.Client()
mqtt_client.connect(os.getenv('MQTT_PORT'))
mqtt_client.subscribe("plates")
mqtt_client.on_message = on_message
print("Waiting for messages .....")
mqtt_client.loop_forever()

