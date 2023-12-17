from simulations.dms import run_dms_simulator
import threading
import time
from settings.settings import print_lock, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
batch_size = 5
dms_batch = []


def dms_callback(key, code, settings):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Key: {key}")

        message = {
            "pi": "PI1",
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.strftime('%H:%M:%S', t),
            "key": key
        }
        dms_batch.append(message)

        if len(dms_batch) == batch_size:
            msgs = [{"topic": "dms", "payload": json.dumps(msg)} for msg in dms_batch]
            mqtt_config = load_mqtt_config()
            mqtt_publish.multiple(msgs, hostname=mqtt_config['host'], port=mqtt_config['port'],
                                  auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
            dms_batch.clear()


def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} loop")
        dms_thread = threading.Thread(target=run_dms_simulator, args=(2, dms_callback, stop_event, settings))
        dms_thread.start()
        threads.append(dms_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.dms import run_dms_loop, DMS
        print(f"Starting {settings['name']} loop")
        dms = DMS(settings['name'], settings['row_pins'], settings['col_pins'])
        dms_thread = threading.Thread(target=run_dms_loop, args=(dms, 2, dms_callback, stop_event))
        dms_thread.start()
        threads.append(dms_thread)
        print(f"{settings['name']} loop started")
