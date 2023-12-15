from simulations.dht import run_dht_simulator
import threading
import time
from settings.settings import print_lock
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883


def dht_callback(humidity, temperature, code, settings):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

        message = {
            "pi": "PI1",
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.strftime('%H:%M:%S', t),
            "humidity": humidity,
            "temperature": temperature
        }

        mqtt_publish.single(f"dht", json.dumps(message), hostname=mqtt_host, port=mqtt_port)


def run_dht(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.dht import run_dht_loop, DHT
        print(f"Starting {settings['name']} loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f"{settings['name']} loop started")