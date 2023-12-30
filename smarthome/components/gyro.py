from simulations.gyro import run_gyro_simulator
import threading
import time
from settings.settings import print_lock, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
batch_size = 5
gyro_batch = []


def gyro_callback(rotation, acceleration, code, settings):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Rotation: {rotation}%")
        print(f"Acceleration: {acceleration}°C")

        message = {
            "pi": "PI1",
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.time(),
            "rotation": float(rotation),
            "acceleration": float(acceleration)
        }
        gyro_batch.append(message)

        if len(gyro_batch) == batch_size:
            msgs = [{"topic": "gyro", "payload": json.dumps(msg)} for msg in gyro_batch]
            mqtt_config = load_mqtt_config()
            mqtt_publish.multiple(msgs, hostname=mqtt_config['host'], port=mqtt_config['port'],
                                  auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
            gyro_batch.clear()


def run_gyro(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        gyro_thread = threading.Thread(target=run_gyro_simulator, args=(2, gyro_callback, stop_event, settings))
        gyro_thread.start()
        threads.append(gyro_thread)
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