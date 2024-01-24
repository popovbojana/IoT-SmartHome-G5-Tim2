import json
import threading
import time
import paho.mqtt.client as mqtt

from settings.settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
from components.button import run_button
from components.dms import run_dms
from components.diode import run_diode
from components.buzzer import run_buzzer
from settings.broker_settings import HOST, PORT


try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_sensors(settings, threads, stop_event):
    rdh1_settings = settings['Room DHT'][0]
    rdh2_settings = settings['Room DHT'][1]
    dus1_settings = settings['Door Ultrasonic Sensor'][0]
    dpir1_settings = settings['Door Motion Sensor'][0]
    rpir1_settings = settings['Room PIR'][0]
    rpir2_settings = settings['Room PIR'][1]
    ds1_settings = settings['Door Sensor'][0]
    db_settings = settings['Door Buzzer'][0]

    run_dht(rdh1_settings, threads, stop_event)
    run_dht(rdh2_settings, threads, stop_event)
    run_uds(dus1_settings, threads, stop_event)
    run_pir(dpir1_settings, threads, stop_event)
    run_pir(rpir1_settings, threads, stop_event)
    run_pir(rpir2_settings, threads, stop_event)
    run_button(ds1_settings, threads, stop_event)
    run_buzzer(db_settings, threads, stop_event, alarm_event, system_event, alarm_clock_event)


def run_actuators(settings, threads, stop_event):
    dms_settings = settings['Door Membrane Switch'][0]

    run_dms('key', dms_settings, threads, stop_event, system_event)


alarm_event = threading.Event()
system_event = threading.Event()
alarm_clock_event = threading.Event()


def on_connect(client, userdata, flags, rc):
    topics = ['dpir1-light-on', 'alarm-on', 'alarm-off', 'system-on', 'system-off']

    if rc == 0:
        print("Connected to MQTT broker")

        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)

    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    if msg.topic == 'dpir1-light-on':
        dl_settings = settings_pi1['Door Light'][0]
        run_diode(dl_settings, threads_pi1, stop_event_pi1)
    elif msg.topic == 'alarm-on':
        alarm_event.set()
        print("Alarm: ON")
    elif msg.topic == 'alarm-off':
        alarm_event.clear()
        print("Alarm: OFF")
    elif msg.topic == 'system-on':
        system_event.set()
        print("System: ON")
    elif msg.topic == 'system-off':
        system_event.clear()
        print("System: OFF")


if __name__ == "__main__":
    print('Starting PI1...')
    settings_pi1 = load_settings('settings/settings_pi1.json')
    threads_pi1 = []
    stop_event_pi1 = threading.Event()

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg)
    mqtt_client.connect(HOST, PORT, 60)
    mqtt_client.loop_start()

    try:
        run_sensors(settings_pi1, threads_pi1, stop_event_pi1)
        run_actuators(settings_pi1, threads_pi1, stop_event_pi1)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app...')
        for t in threads_pi1:
            stop_event_pi1.set()
