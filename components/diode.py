import threading
import time
from settings.settings import print_lock2, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
state = False
batch_size = 5
diode_batch = []


def diode_callback(code, settings):
    global state
    with print_lock2:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")

        if state:
            state = True
            print("Light is on\n")
        else:
            state = False
            print("Light is off\n")

        message = {
            "pi": "PI1",
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.time(),
            "light_on": state,
        }
        diode_batch.append(message)

        if len(diode_batch) == batch_size:
            msgs = [{"topic": "diode", "payload": json.dumps(msg)} for msg in diode_batch]
            mqtt_config = load_mqtt_config()
            mqtt_publish.multiple(msgs, hostname=mqtt_config['host'], port=mqtt_config['port'],
                                  auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
            diode_batch.clear()


def run_diode(settings, threads, stop_event):
    if settings['simulated']:
        diode_thread = threading.Thread(target=diode_callback, args=('DIODE_OK', settings))
        diode_thread.start()
        threads.append(diode_thread)
    else:
        from actuators.diode import run_diode_loop, DIODE
        diode = DIODE(settings['name'], settings['pin'])
        diode_thread = threading.Thread(target=run_diode_loop, args=(diode, 2, diode_callback, stop_event))
        diode_thread.start()
        threads.append(diode_thread)
