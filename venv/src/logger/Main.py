import os

from paho import mqtt
from pymongo import MongoClient
import json

client = MongoClient()
db = client.plates

plates = db.plates


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    plate = {
        '_id': payload["id"],
        'plate': payload["plate"]
    }
    plates.insert_one(plate)


mqtt_client = mqtt.Client()
mqtt_client.connect(os.getenv('MQTT_PORT'))
mqtt_client.subscribe("text")
mqtt_client.on_message = on_message
print("Waiting for messages .....")
mqtt_client.loop_forever()

