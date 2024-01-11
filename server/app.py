from datetime import datetime, timedelta

from flask import Flask, jsonify
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
import paho.mqtt.publish as mqtt_publish
from settings.broker_settings import HOST, PORT
from settings.influx_settings import TOKEN, ORG, URL
from save_to_influx import *
from threading import Lock

people_inside_lock = Lock()

app = Flask(__name__)

people_inside = 0

# InfluxDB Config
influxdb_client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)


def on_connect(client, userdata, flags, rc):
    topics = ["button", "dht", "dms", "pir", "uds", "buzzer", "diode", "gyro", "lcd", "rgb_led", "fdss"]

    if rc == 0:
        print("Connected to MQTT broker")

        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)

    else:
        print(f"Connection failed with code {rc}")


mqtt_client = mqtt.Client()
# mqtt_client.username_pw_set(username="client", password="password")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg)
mqtt_client.connect(HOST, PORT, 60)
mqtt_client.loop_start()


def on_message(client, userdata, msg):
    global people_inside

    try:
        payload = json.loads(msg.payload.decode())
        # print(payload)
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

        if payload["name"] == "DPIR1":
            msg = json.dumps({"event": "turn-on"})
            mqtt_publish.single("dpir1-light-on", payload=msg, hostname=HOST, port=PORT)

            event_timestamp = payload["timestamp"]
            if not isinstance(event_timestamp, datetime):
                event_timestamp = datetime.fromtimestamp(event_timestamp)
            start_time = int((event_timestamp - timedelta(seconds=60)).timestamp())
            end_time = int(event_timestamp.timestamp())

            query = f"""
                from(bucket: "iot")
                  |> range(start: {start_time}, stop: {end_time})
                  |> filter(fn: (r) => r["_measurement"] == "uds_data")
                  |> filter(fn: (r) => r["_field"] == "distance")
                  |> filter(fn: (r) => r["name"] == "DUS1")
                """
            last_dus1_data = handle_influx_query(query)
            if last_dus1_data['status'] == "success":
                sorted_data = sorted(last_dus1_data['data'], key=lambda x: x['_time'])
                if len(sorted_data) >= 1:
                    first_distance = sorted_data[0]['_value']
                    last_distance = sorted_data[-1]['_value']

                    with people_inside_lock:
                        if last_distance > first_distance:
                            people_inside += 1
                        elif last_distance < first_distance:
                            people_inside -= 1
                            if people_inside < 0:
                                people_inside = 0
                        else:
                            pass

                print("People inside: ", people_inside)

        if payload["name"] == "DPIR2":
            event_timestamp = payload["timestamp"]
            if not isinstance(event_timestamp, datetime):
                event_timestamp = datetime.fromtimestamp(event_timestamp)
            start_time = int((event_timestamp - timedelta(seconds=60)).timestamp())
            end_time = int(event_timestamp.timestamp())

            query = f"""
                from(bucket: "iot")
                  |> range(start: {start_time}, stop: {end_time})
                  |> filter(fn: (r) => r["_measurement"] == "uds_data")
                  |> filter(fn: (r) => r["_field"] == "distance")
                  |> filter(fn: (r) => r["name"] == "DUS2")
                """
            last_dus2_data = handle_influx_query(query)
            if last_dus2_data['status'] == "success":
                sorted_data = sorted(last_dus2_data['data'], key=lambda x: x['_time'])
                if len(sorted_data) >= 1:
                    first_distance = sorted_data[0]['_value']
                    last_distance = sorted_data[-1]['_value']

                    with people_inside_lock:
                        if last_distance > first_distance:
                            people_inside += 1
                        elif last_distance < first_distance:
                            people_inside -= 1
                            if people_inside < 0:
                                people_inside = 0
                        else:
                            pass

                print("People inside: ", people_inside)

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

        return {"status": "success", "data": container}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.route("/")
def index():
    return "Flask MQTT Publisher"


if __name__ == "__main__":
    app.run()
