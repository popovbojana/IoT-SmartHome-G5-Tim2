from flask import Flask
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as mqtt_publish
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
from model.gyro import Gyro
from model.lcd import Lcd
from model.rgb_led import Rgb_led
from model.fdss import Fdss

app = Flask(__name__)

mqtt_host = "localhost"
mqtt_port = 1883
mqtt_username = "client"
mqtt_password = "password"

topics = ["button", "dht", "dms", "pir", "uds", "buzzer", "diode", "gyro", "lcd", "rgb_led", "fdss"]


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
    elif msg.topic == "gyro":
        gyro = Gyro(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["rotation"], payload["acceleration"])
        gyro.save_to_influxdb(client_influx)
    elif msg.topic == "lcd":
        lcd = Lcd(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["display"])
        lcd.save_to_influxdb(client_influx)
    elif msg.topic == "rgb_led":
        rgb_led = Rgb_led(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["state"])
        rgb_led.save_to_influxdb(client_influx)
    elif msg.topic == "fdss":
        fdss = Fdss(payload["timestamp"], payload["pi"], payload["name"], payload["simulated"], payload["alarm_time"])
        fdss.save_to_influxdb(client_influx)


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
        #FILIP TOKEN:
        "token": "2y_saeDWgOVQrh3S7QVarIImp-W---5lc_0giPs8xn1tzQjOGXxNT9tuF8YrovtLMNxQsdyQvSOCtP61h0d2UQ=="
        #BOJANA TOKEN:
    }
}

influxdb_config = config.get("influxdb", {})

client_influx = InfluxDBClient(url=f"http://{influxdb_config['host']}:{influxdb_config['port']}", token=influxdb_config['token'], org=influxdb_config['organization'])


mqtt_thread = threading.Thread(target=mqtt_subscribe)
mqtt_thread.start()

if __name__ == "__main__":
    dht_batch = ['asd', 'asd']
    msgs = [{"topic": "dpir1-light-on", "payload": json.dumps(msg)} for msg in dht_batch]
    mqtt_publish.multiple(msgs, hostname='localhost', port=1883,
                          auth={"username": 'client', "password": 'password'})
    # app.run()
