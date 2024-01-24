import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS from Flask-CORS
from flask_socketio import SocketIO
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
from settings.broker_settings import HOST, PORT
from settings.influx_settings import TOKEN, ORG, URL
from save_to_influx import *
from threading import Lock

people_inside_lock = Lock()

app = Flask(__name__)

people_inside = 0
pin_code = ['0', '0', '0', '0']
system_on = False
alarm_on = False

alarm_clock_time = ''
alarm_clock_on = False

# InfluxDB Config
influxdb_client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
scheduler = BackgroundScheduler()

# Web sockets config
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def send_message_ws(topic, payload):
    try:
        socketio.emit(topic, payload)
    except Exception as e:
        print(e)


def handle_button(payload):
    global alarm_on, system_on
    if (payload["code"] == "BUTTON_5_SEC") and (alarm_on is not True) and (system_on is True):
        msg = json.dumps({"event": "alarm-on-button", "time": payload["timestamp"]})
        mqtt_client.publish("alarm-on", payload=msg)
        save_alarm_data(True, time.time(), influxdb_client)
        alarm_on = True
        send_message_ws("alarm", True)


def handle_dht(payload):
    message = {
        "display": ("Humidity: " + str(payload['humidity']) + "\n" +
                    "Temperature: " + str(payload['temperature']))
    }

    msg = json.dumps(message)
    mqtt_client.publish("lcd-display", payload=msg)


def handle_dms(payload):
    global alarm_on, system_on
    key_list = [str(p) for p in pin_code]
    key = payload['key']
    if ',' in key:
        list = key.split(',')
        check_key_list = [l.strip() for l in list]
        if key_list == check_key_list:
            if system_on:
                msg = json.dumps({"event": "system-off"})
                mqtt_client.publish("system-off", payload=msg)
                system_on = False
                send_message_ws("system", False)

                if alarm_on:
                    msg = json.dumps({"event": "alarm-off"})
                    mqtt_client.publish("alarm-off", payload=msg)
                    save_alarm_data(False, time.time(), influxdb_client)
                    alarm_on = False
                    send_message_ws("alarm", False)

            else:
                time.sleep(10)
                msg = json.dumps({"event": "system-on"})
                mqtt_client.publish("system-on", payload=msg)
                system_on = True
                send_message_ws("system", True)
            return True
        else:
            return False


def handle_ir(payload):
    if payload['button'] == "0":
        msg = json.dumps({"command": "OFF"})
        mqtt_client.publish("rgb_commands", payload=msg)

    elif payload['button'] == "1":
        msg = json.dumps({"command": "WHITE"})
        mqtt_client.publish("rgb_commands", payload=msg)

    elif payload['button'] == "2":
        msg = json.dumps({"command": "RED"})
        mqtt_client.publish("rgb_commands", payload=msg)

    elif payload['button'] == "3":
        msg = json.dumps({"command": "GREEN"})
        mqtt_client.publish("rgb_commands", payload=msg)

    elif payload['button'] == "4":
        msg = json.dumps({"command": "BLUE"})
        mqtt_client.publish("rgb_commands", payload=msg)

    elif payload['button'] == "5":
        msg = json.dumps({"command": "YELLOW"})
        mqtt_client.publish("rgb_commands", payload=msg)

    elif payload['button'] == "6":
        msg = json.dumps({"command": "PURPLE"})
        mqtt_client.publish("rgb_commands", payload=msg)

    elif payload['button'] == "7":
        msg = json.dumps({"command": "LIGHT_BLUE"})
        mqtt_client.publish("rgb_commands", payload=msg)


def handle_pir(payload):
    global system_on, alarm_on, people_inside
    if payload["name"] == "DPIR1":
        msg = json.dumps({"event": "turn-on"})
        mqtt_client.publish("dpir1-light-on", payload=msg)

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
                        send_message_ws("people_inside", people_inside)
                    elif last_distance < first_distance:
                        people_inside -= 1
                        if people_inside < 0:
                            people_inside = 0
                    else:
                        pass

            print("People inside: ", people_inside)
            save_people_data(people_inside, time.time(), influxdb_client)
            send_message_ws("people_inside", people_inside)

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
            save_people_data(people_inside, time.time(), influxdb_client)
            send_message_ws("people_inside", people_inside)

    if payload['name'] == 'RPIR1' or payload['name'] == 'RPIR2' or payload['name'] == 'RPIR3' or payload[
        'name'] == 'RPIR4':
        if people_inside == 0 and (alarm_on is not True) and (system_on is True):
            msg = json.dumps({"event": "alarm-on-" + payload['name']})
            mqtt_client.publish("alarm-on", payload=msg)
            save_alarm_data(True, time.time(), influxdb_client)
            print("ALARM ", payload['name'])
            alarm_on = True
            send_message_ws("alarm", True)


def handle_gyro(payload):
    global alarm_on, system_on
    acceleration = float(payload['acceleration'])
    rotation = float(payload['rotation'])

    if acceleration < -9.5 or acceleration > 9.5:
        if (alarm_on is not True) and (system_on is True):
            msg = json.dumps({"event": "alarm-on-gyro"})
            mqtt_client.publish("alarm-on", payload=msg)
            alarm_on = True
            save_alarm_data(True, time.time(), influxdb_client)
            send_message_ws("alarm", True)

    if rotation < -175 or rotation > 175:
        if (alarm_on is not True) and (system_on is True):
            msg = json.dumps({"event": "alarm-on-gyro"})
            mqtt_client.publish("alarm-on", payload=msg)
            alarm_on = True
            save_alarm_data(True, time.time(), influxdb_client)
            send_message_ws("alarm", True)


def handle_alarm_clock_pi(payload):
    global alarm_clock_on, alarm_clock_time
    if payload["action"] == "add":
        alarm_clock_time = payload["time"]
    elif payload["action"] == "turn-off":
        alarm_clock_on = False
        alarm_clock_time = ''
        msg = json.dumps({"event": "alarm-off"})
        mqtt_client.publish("alarm-clock-server", payload=msg)
        send_message_ws("alarm_clock", False)


@app.route('/dms', methods=['POST'])
def dms_endpoint():
    try:
        payload = request.get_json()

        if payload:
            print("Received JSON data: ", payload)
            try:
                save_dms_data(payload, influxdb_client)
                result = handle_dms(payload)

                if not result:
                    raise Exception("wrong password")

            except Exception as e:
                return jsonify({"response": "error - " + str(e)})

            return jsonify({"response": "Correct passcode. Dms processed successfully"})
        else:
            return jsonify({"response": "error - No JSON data received"})
    except Exception as e:
        return jsonify({"response": "error - " + str(e)})


@app.route('/ir', methods=['POST'])
def ir_endpoint():
    try:
        payload = request.get_json()

        if payload:
            print("Received JSON data: ", payload)
            try:
                save_ir_data(payload, influxdb_client)
                handle_ir(payload)
            except Exception as e:
                print(e)

            return jsonify({"response": "Ir processed successfully"})
        else:
            return jsonify({"response": "error - No JSON data received"})
    except Exception as e:
        return jsonify({"response": "error - " + str(e)})


@app.route('/alarm-clock-pi', methods=['POST'])
def alarm_clock_pi_endpoint():
    try:
        payload = request.get_json()

        if payload:
            print("Received JSON data: ", payload)
            try:
                handle_alarm_clock_pi(payload)
            except Exception as e:
                print(e)

            return jsonify({"response": "Alarm clock pi processed successfully"})
        else:
            return jsonify({"response": "error - No JSON data received"})
    except Exception as e:
        return jsonify({"response": "error - " + str(e)})


def check_and_trigger_alarms():
    global alarm_clock_time, alarm_clock_on

    current_time = time.strftime('%H:%M')
    if current_time == alarm_clock_time and not alarm_clock_on:
        print("ALARM CLOCK")
        msg = json.dumps({"event": "alarm-on"})
        mqtt_client.publish("alarm-clock-server", payload=msg)
        alarm_clock_on = True
        send_message_ws("alarm_clock", True)

def on_connect(client, userdata, flags, rc):
    topics = ["button", "dht", "dms", "pir", "uds", "buzzer", "diode", "gyro", "lcd", "rgb_led", "fdss", "ir",
              "alarm-clock-pi"]

    if rc == 0:
        print("Connected to MQTT broker")

        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)

        scheduler.add_job(check_and_trigger_alarms, 'interval', seconds=10)
        scheduler.start()

    else:
        print(f"Connection failed with code {rc}")


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg)
mqtt_client.connect(HOST, PORT, 60)
mqtt_client.loop_start()


def on_message(client, userdata, msg):
    global people_inside, system_on, alarm_on, alarm_clock_on

    try:
        payload = json.loads(msg.payload.decode())
        # print(payload)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Invalid payload: {msg.payload}")
        return

    if msg.topic == "uds":
        save_uds_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)

    elif msg.topic == "button":
        save_button_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)
        handle_button(payload)

    elif msg.topic == "buzzer":
        save_buzzer_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)

    elif msg.topic == "dht":
        save_dht_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)
        handle_dht(payload)

    elif msg.topic == "diode":
        save_diode_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)

    elif msg.topic == "pir":
        save_pir_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)
        handle_pir(payload)

    elif msg.topic == "gyro":
        save_gyro_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)
        handle_gyro(payload)

    elif msg.topic == "lcd":
        save_lcd_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)

    elif msg.topic == "rgb_led":
        save_rgb_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)

    elif msg.topic == "fdss":
        save_fdss_data(payload, influxdb_client)
        send_message_ws(payload["name"], payload)


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
    # socketio.run(app, debug=True, port=5000)
    app.run()
