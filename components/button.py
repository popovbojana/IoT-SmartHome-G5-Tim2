from simulations.button import run_button_simulator
import threading
import time
from settings.settings import print_lock
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883


def button_callback(pushed, unlocked, code, settings):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"{pushed}")

        message = {
            "pi": "PI1",
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.strftime('%H:%M:%S', t),
            "door_unlocked": unlocked
        }

        mqtt_publish.single(f"button", json.dumps(message), hostname=mqtt_host, port=mqtt_port)


def run_button(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} loop")
        button_thread = threading.Thread(target=run_button_simulator, args=(2, button_callback, stop_event, settings))
        button_thread.start()
        threads.append(button_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.button import run_button_loop, Button
        print(f"Starting {settings['name']} loop")
        button = Button(settings['name'], settings['pin'])
        button_thread = threading.Thread(target=run_button_loop, args=(button, 2, button_callback, stop_event))
        button_thread.start()
        threads.append(button_thread)
        print(f"{settings['name']} loop started")
