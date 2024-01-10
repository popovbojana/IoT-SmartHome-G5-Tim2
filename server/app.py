from flask import Flask, jsonify
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
from settings.broker_settings import HOST, PORT
from settings.influx_settings import TOKEN, ORG, URL
from save_to_influx import *

app = Flask(__name__)

# InfluxDB Config
influxdb_client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)

# MQTT Config
mqtt_client = mqtt.Client()
mqtt_client.connect(HOST, PORT, 60)
mqtt_client.loop_start()


def on_connect(client, userdata, flags, rc):
    topics = ["button", "dht", "dms", "pir", "uds", "buzzer", "diode", "gyro", "lcd", "rgb_led", "fdss"]

    if rc == 0:
        print("Connected to MQTT broker")

        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)

    else:
        print(f"Connection failed with code {rc}")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(payload)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Invalid payload: {msg.payload}")
        return
    if msg.topic == "uds":
        save_uds_data(payload, influxdb_client)
    elif msg.topic == "button":
        save_button_data(payload, influxdb_client)
    elif msg.topic == "buzzer":
        save_buzzer_data(payload, influxdb_client)
    elif msg.topic == "dht":
        save_dht_data(payload, influxdb_client)
    elif msg.topic == "diode":
        save_diode_data(payload, influxdb_client)
    elif msg.topic == "dms":
        save_dms_data(payload, influxdb_client)
    elif msg.topic == "pir":
        save_pir_data(payload, influxdb_client)
        # pir.turn_on_light()

        # if payload["name"] == "DPIR1":
        #     msg = json.dumps({"event": "turn-on"})
        #     mqtt_publish.single("dpir1-light-on", payload=msg, hostname=mqtt_config['host'], port=mqtt_config['port'],
        #                         auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
        #     query = """
        #     from(bucket: "iot")
        #       |> range(start: -1m, stop: now())
        #       |> filter(fn: (r) => r["_measurement"] == "uds_data")
        #       |> filter(fn: (r) => r["_field"] == "distance")
        #       |> filter(fn: (r) => r["name"] == "DUS1")
        #     """
        #     last_dus1_data = handle_influx_query(query)
        #     print(last_dus1_data['data'])

    elif msg.topic == "gyro":
        save_gyro_data(payload, influxdb_client)
    elif msg.topic == "lcd":
        save_lcd_data(payload, influxdb_client)
    elif msg.topic == "rgb_led":
        save_rgb_data(payload, influxdb_client)
    elif msg.topic == "fdss":
        save_fdss_data(payload, influxdb_client)


def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/")
def index():
    return "Flask MQTT Publisher"


if __name__ == "__main__":
    app.run()
