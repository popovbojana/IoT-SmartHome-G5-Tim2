from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.publish as mqtt_publish
from settings.settings import load_mqtt_config
import json

mqtt_config = load_mqtt_config()


class Pir:
    def __init__(self, timestamp, pi, name, simulated, motion_detected):
        self.timestamp = timestamp
        self.pi = pi
        self.name = name
        self.simulated = simulated
        self.motion_detected = motion_detected

    def save_to_influxdb(self, client):
        point = Point("pir_data").time(int(self.timestamp), WritePrecision.S)
        point.tag("pi", self.pi)
        point.tag("name", self.name)
        point.tag("simulated", self.simulated)
        point.field("motion_detected", self.motion_detected)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket="iot", org="nwt", record=point)

    def turn_on_light(self):
        if self.name == "DPIR1" and self.motion_detected:
            msg = json.dumps({"event": "turn-on"})

            mqtt_publish.single("dpir1-light-on", payload=msg, hostname=mqtt_config['host'], port=mqtt_config['port'],
                                auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
