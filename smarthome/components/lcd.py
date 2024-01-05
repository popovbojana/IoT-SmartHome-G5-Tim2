from simulations.lcd import run_lcd_simulator
import threading
import time
from settings.settings import print_lock, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
batch_size = 5
lcd_batch = []


def lcd_callback(display, code, settings):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Display: {display}%")

        message = {
            "pi": "PI2",
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.time(),
            "display": display
        }
        lcd_batch.append(message)

        if len(lcd_batch) == batch_size:
            msgs = [{"topic": "lcd", "payload": json.dumps(msg)} for msg in lcd_batch]
            mqtt_config = load_mqtt_config()
            mqtt_publish.multiple(msgs, hostname=mqtt_config['host'], port=mqtt_config['port'],
                                  auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
            lcd_batch.clear()


def run_lcd(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        lcd_thread = threading.Thread(target=run_lcd_simulator, args=(2, lcd_callback, stop_event, settings))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"{settings['name']} simulator started")
    else:
        pass
        # todo: funkcije za gyro senzor
        # from sensors.gyro import run_gyro_loop, Gyro
        # print(f"Starting {settings['name']} loop")
        # gyro = Gyro(settings['pin'])
        # gyro_thread = threading.Thread(target=run_gyro_loop, args=(gyro, 2, gyro_callback, stop_event))
        # gyro_thread.start()
        # threads.append(gyro_thread)
        # print(f"{settings['name']} loop started")