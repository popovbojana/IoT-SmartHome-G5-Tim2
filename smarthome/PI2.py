import threading
import time
import paho.mqtt.client as mqtt

from settings.settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
from components.button import run_button
from components.gyro import run_gyro
from components.lcd import run_lcd
from settings.broker_settings import HOST, PORT


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


system_event = threading.Event()


def on_connect(client, userdata, flags, rc):
    topics = ['lcd-display', 'system-on', 'system-off']

    if rc == 0:
        print("Connected to MQTT broker")

        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)

    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    if msg.topic == 'lcd-display':
        print("ASD")
    elif msg.topic == 'system-on':
        pass
    elif msg.topic == 'system-off':
        pass


if __name__ == "__main__":
    print('Starting PI2...')
    settings_pi2 = load_settings('settings/settings_pi2.json')
    threads_pi2 = []
    stop_event_pi2 = threading.Event()

    # MQTT Config
    mqtt_client = mqtt.Client()
    mqtt_client.connect(HOST, PORT, 60)
    mqtt_client.loop_start()

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg)

    try:
        run_sensors(settings_pi2, threads_pi2, stop_event_pi2)
        run_displays(settings_pi2, threads_pi2, stop_event_pi2)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app...')
        for t in threads_pi2:
            stop_event_pi2.set()
