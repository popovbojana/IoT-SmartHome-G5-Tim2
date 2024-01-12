from simulations.dht import run_dht_simulator
import threading
import time
import paho.mqtt.publish as mqtt_publish
import json
from settings.broker_settings import HOST, PORT

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        mqtt_publish.multiple(local_dht_batch, hostname=HOST, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dht_callback(humidity, temperature, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    # t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")
    # print(f"Humidity: {humidity}%")
    # print(f"Temperature: {temperature}°C")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "humidity": float(humidity),
        "temperature": float(temperature)
    }

    with counter_lock:
        dht_batch.append(('dht', json.dumps(message), 0, False))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        dht1_thread = threading.Thread(target=run_dht_simulator, args=(2, dht_callback, stop_event, settings,
                                                                       publish_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.dht import run_dht_loop, DHT
        print(f"Starting {settings['name']} loop")
        dht = DHT(settings['pin'])
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, settings,
                                                                  publish_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        print(f"{settings['name']} loop started")
