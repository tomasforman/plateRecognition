import json
import os
from paho import mqtt

from venv.src.sender.email_service import send_email
from venv.src.sender.emails_repository import fetch_emails
from venv.src.sender.plates_repository import find_plate


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    plate = payload["plate"]
    plate_exists = find_plate(plate)
    if plate_exists:
        emails = fetch_emails()
        for email in emails:
            send_email(email, payload["id"], plate)


mqtt_client = mqtt.Client()
mqtt_client.connect(os.getenv('MQTT_PORT'))
mqtt_client.subscribe("text")
mqtt_client.on_message = on_message
print("Waiting for messages .....")
mqtt_client.loop_forever()
