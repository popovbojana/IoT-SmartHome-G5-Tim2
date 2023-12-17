from flask import Flask, request
import json
import paho.mqtt.client as mqtt
import time
import random
import threading

from model.uds import Uds

app = Flask(__name__)

mqtt_host = "localhost"
mqtt_port = 1883
mqtt_username = "client"
mqtt_password = "password"

air_conditioners = {}
ambient_senzors = {}
lamps = {}
vehicle_gates = {}

topics = ["button", "dth", "dms", "pir", "uds", "buzzer", "diode"]
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")

        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)

    else:
        print(f"Connection failed with code {rc}")



def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print(f"Received message: {payload}")

    if msg.topic == "uds":
        print("AAAAAAAAAAAAAAAAAAAAa")
        timestamp = time.time()
        dus_sensor = Uds(timestamp, payload["pi"], payload["name"], payload["simulated"], payload["distance"])
        dus_sensor.save_to_influxdb()


def mqtt_subscribe():
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_username, password=mqtt_password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_host, mqtt_port, 60)
    client.loop_forever()

def publish_mqtt_message(message):
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_username, password=mqtt_password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_host, mqtt_port, 60)
    client.loop_start()
    client.publish("new_topic/Temperature", message)
    time.sleep(1)
    client.loop_stop()


@app.route("/")
def index():
    return "Flask MQTT Publisher"


mqtt_thread = threading.Thread(target=mqtt_subscribe)
mqtt_thread.start()

if __name__ == "__main__":
    app.run()
