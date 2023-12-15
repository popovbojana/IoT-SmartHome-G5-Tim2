from simulations.dht import run_dht_simulator
import threading
import time
from settings.settings import print_lock
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
batch_size = 5
dht_batch = []


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
        dht_batch.append(message)

        if len(dht_batch) == batch_size:
            msgs = [{"topic": "dht", "payload": json.dumps(msg)} for msg in dht_batch]
            mqtt_publish.multiple(msgs, hostname=mqtt_host, port=mqtt_port)
            dht_batch.clear()


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