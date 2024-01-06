from simulations.uds import run_uds_simulator
import threading
import time
from settings.settings import print_lock, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
batch_size = 5
uds_batch = []


def uds_callback(distance, code, settings):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Distance: {distance}")

        message = {
            "pi": settings['pi'],
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.time(),
            "distance": float(distance)
        }
        uds_batch.append(message)

        if len(uds_batch) == batch_size:
            msgs = [{"topic": "uds", "payload": json.dumps(msg)} for msg in uds_batch]
            mqtt_config = load_mqtt_config()
            mqtt_publish.multiple(msgs, hostname=mqtt_config['host'], port=mqtt_config['port'],
                                  auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
            uds_batch.clear()


def run_uds(settings, threads, stop_event):
        if settings['simulated']:
            print(f"Starting {settings['name']} simulator")
            uds1_thread = threading.Thread(target = run_uds_simulator, args=(2, uds_callback, stop_event, settings))
            uds1_thread.start()
            threads.append(uds1_thread)
            print(f"{settings['name']} simulator started")
        else:
            from sensors.uds import run_uds_loop, UDS
            print(f"Starting {settings['name']} loop")
            uds = UDS(settings['name'], settings['trig_pin'], settings['echo_pin'])
            uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event))
            uds_thread.start()
            threads.append(uds_thread)
            print(f"{settings['name']} loop started")