import json
import threading
import time
import paho.mqtt.client as mqtt
import re

from settings.settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.buzzer import run_buzzer
from components.fdss import run_fdss
from components.rgb_led import run_rgb_led
from components.ir import run_ir
from settings.settings import print_lock
from settings.broker_settings import HOST, PORT


try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_sensors(settings, threads, stop_event):
    rpir4_settings = settings['Room PIR'][0]
    rdh4_settings = settings['Room DHT'][0]
    bir_settings = settings['Bedroom Infrared'][0]
    bb_settings = settings['Bedroom Buzzer'][0]

    run_pir(rpir4_settings, threads, stop_event)
    run_dht(rdh4_settings, threads, stop_event)
    run_pir(bir_settings, threads, stop_event)
    run_buzzer(bb_settings, threads, stop_event, alarm_event, system_event, alarm_clock_event)


def run_actuators(settings, threads, stop_event):
    ir_settings = settings['Bedroom Infrared'][0]

    run_ir(ir_settings, threads, stop_event, "0")


def validate_time_format(time_str):
    time_regex = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')

    if time_regex.match(time_str):
        return True
    else:
        return False


def run_displays(settings, threads, stop_event):
    b4sd_settings = settings['Bedroom 4 Digit 7 Segment Display'][0]

    run_fdss(b4sd_settings, threads, stop_event, alarm_clock_event)


alarm_event = threading.Event()
system_event = threading.Event()
alarm_clock_event = threading.Event()


def on_connect(client, userdata, flags, rc):
    topics = ['rgb_commands', 'alarm-on', 'alarm-off', 'system-on', 'system-off', 'alarm-clock-on', 'alarm-clock-server']

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
        # print(payload)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Invalid payload: {msg.payload}")
        return

    if msg.topic == 'rgb_commands':
        command = payload['command']
        brgb_settings = settings_pi3['Bedroom RGB'][0]
        run_rgb_led(command, brgb_settings, threads_pi3, stop_event_pi3)

    elif msg.topic == 'alarm-on':
        alarm_event.set()
        print(payload)
    elif msg.topic == 'alarm-off':
        alarm_event.clear()
        print("ALARM OFF")
    elif msg.topic == 'system-on':
        system_event.set()
        print("SYSTEM ON")
    elif msg.topic == 'system-off':
        system_event.clear()
        print("SYSTEM OFF")
    elif msg.topic == 'alarm-clock-server':
        if payload["event"] == "alarm-on":
            print("UKLJUCIO budilnik")
            alarm_clock_event.set()
        elif payload["event"] == "alarm-off":
            alarm_clock_event.clear()
            print("iskljucen budilnik")


if __name__ == "__main__":
    print('Starting PI3...')
    settings_pi3 = load_settings('settings/settings_pi3.json')
    threads_pi3 = []
    stop_event_pi3 = threading.Event()

    # MQTT Config
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg)
    mqtt_client.connect(HOST, PORT, 60)
    mqtt_client.loop_start()

    try:
        run_sensors(settings_pi3, threads_pi3, stop_event_pi3)
        run_actuators(settings_pi3, threads_pi3, stop_event_pi3)
        run_displays(settings_pi3, threads_pi3, stop_event_pi3)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app...')
        for t in threads_pi3:
            stop_event_pi3.set()
