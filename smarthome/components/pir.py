from simulations.pir import run_pir_simulator
import threading
import time
from settings.settings import print_lock, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
batch_size = 5
pir_batch = []


def pir_callback(motion, detected, code, settings):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"{motion}")

        message = {
            "pi": settings['pi'],
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.time(),
            "motion_detected": detected
        }
        pir_batch.append(message)

        if len(pir_batch) == batch_size:
            msgs = [{"topic": "pir", "payload": json.dumps(msg)} for msg in pir_batch]
            mqtt_config = load_mqtt_config()
            mqtt_publish.multiple(msgs, hostname=mqtt_config['host'], port=mqtt_config['port'],
                                  auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
            pir_batch.clear()


def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} loop")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, pir_callback, stop_event, settings))
        pir_thread.start()
        threads.append(pir_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.pir import run_pir_loop, PIR
        print(f"Starting {settings['name']} loop")
        pir = PIR(settings['name'], settings['pin'])
        pir_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, pir_callback, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
        print(f"{settings['name']} loop started")
