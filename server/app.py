from flask import Flask
import json
import paho.mqtt.client as mqtt
import time
from influxdb_client import InfluxDBClient
import threading

from model.uds import Uds
from model.button import Button
from model.buzzer import Buzzer
from model.dht import Dht
from model.diode import Diode
from model.dms import Dms
from model.pir import Pir


app = Flask(__name__)

mqtt_host = "localhost"
mqtt_port = 1883
mqtt_username = "client"
mqtt_password = "password"

air_conditioners = {}
ambient_senzors = {}
lamps = {}
vehicle_gates = {}

topics = ["button", "dht", "dms", "pir", "uds", "buzzer", "diode"]
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
    print(payload)
    if msg.topic == "uds":
        dus_sensor = Uds(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["distance"])
        dus_sensor.save_to_influxdb(client_influx)
    elif msg.topic == "button":
        button = Button(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["door_unlocked"])
        button.save_to_influxdb(client_influx)
    elif msg.topic == "buzzer":
        buzzer = Buzzer(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["pitch"], payload["duration"])
        buzzer.save_to_influxdb(client_influx)
    elif msg.topic == "dht":
        dht = Dht(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["humidity"], payload["temperature"])
        dht.save_to_influxdb(client_influx)
    elif msg.topic == "diode":
        diode = Diode(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["light_on"])
        diode.save_to_influxdb(client_influx)
    elif msg.topic == "dms":
        dms = Dms(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["key"])
        dms.save_to_influxdb(client_influx)
    elif msg.topic == "pir":
        pir = Pir(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["motion_detected"])
        pir.save_to_influxdb(client_influx)


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


config = {
    "influxdb": {
        "host": "localhost",
        "port": 8086,
        "organization": "nwt",
        "bucket": "measurements",
        "token": "RvNuFi6feoqRplXfeScO8c8UJeA366xepg9RinlRH-sKIBBsqacrFEeuQ6jD2Ai4XBZ-VmSDqYX2usL2yIRf3g=="
    }
}

influxdb_config = config.get("influxdb", {})

client_influx = InfluxDBClient(url=f"http://{influxdb_config['host']}:{influxdb_config['port']}", token=influxdb_config['token'], org=influxdb_config['organization'])


mqtt_thread = threading.Thread(target=mqtt_subscribe)
mqtt_thread.start()

if __name__ == "__main__":
    app.run()
