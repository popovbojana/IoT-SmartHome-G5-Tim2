import threading
import paho.mqtt.client as mqtt

from settings.settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
from components.button import run_button
from components.gyro import run_gyro
from components.lcd import run_lcd
from settings.settings import load_mqtt_config

import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_sensors(settings, threads, stop_event):
    ds2_settings = settings['Door Sensor'][0]
    dus2_settings = settings['Door Ultrasonic Sensor'][0]
    dpir2_settings = settings['Door Motion Sensor'][0]
    gdht_settings = settings['Garage DHT'][0]
    gsg_settings = settings['Gun Safe Gyro'][0]
    rpir3_settings = settings['Room PIR'][0]
    rdh3_settings = settings['Room DHT'][0]

    run_button(ds2_settings, threads, stop_event)
    run_uds(dus2_settings, threads, stop_event)
    run_pir(dpir2_settings, threads, stop_event)
    run_dht(gdht_settings, threads, stop_event)
    run_pir(rpir3_settings, threads, stop_event)
    run_dht(rdh3_settings, threads, stop_event)
    run_gyro(gsg_settings, threads, stop_event)


def run_displays(settings, threads, stop_event):
    glcd_settings = settings['Garage LCD'][0]

    run_lcd(glcd_settings, threads, stop_event)


topics = ['lcd-display', 'system-on', 'system-off']
all_topics_subscribed = threading.Event()

system_event = threading.Event()


def on_message(client, userdata, msg):
    if msg.topic == 'lcd-display':
        print("ASD")
    elif msg.topic == 'system-on':
        pass
    elif msg.topic == 'system-off':
        pass


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected PI2 to MQTT broker\n")

        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)
        all_topics_subscribed.set()


    else:
        print(f"Connection failed with code {rc}")


def mqtt_subscribe():
    mqtt_config = load_mqtt_config()
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_config['username'], password=mqtt_config['password'])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_config['host'], mqtt_config['port'], 60)
    client.loop_forever()


if __name__ == "__main__":
    print('Starting PI2...')
    settings_pi2 = load_settings('settings/settings_pi2.json')
    threads_pi2 = []
    stop_event_pi2 = threading.Event()

    mqtt_thread = threading.Thread(target=mqtt_subscribe)
    mqtt_thread.start()
    all_topics_subscribed.wait()

    print()
    try:
        run_sensors(settings_pi2, threads_pi2, stop_event_pi2)
        run_displays(settings_pi2, threads_pi2, stop_event_pi2)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app...')
        for t in threads_pi2:
            stop_event_pi2.set()
