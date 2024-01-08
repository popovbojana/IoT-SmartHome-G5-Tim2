from simulations.gyro import run_gyro_simulator
import threading
import time
from settings.settings import print_lock, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_config = load_mqtt_config()
gyro_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, gyro_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_gyro_batch = gyro_batch.copy()
            publish_data_counter = 0
            gyro_batch.clear()
        mqtt_publish.multiple(local_gyro_batch, hostname=mqtt_config['host'], port=mqtt_config['port'],
                              auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gyro_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def gyro_callback(rotation, acceleration, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print()
    print("*" * 5 + settings['name'] + "*" * 5)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Rotation: {rotation}")
    print(f"Acceleration: {acceleration}")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "rotation": float(rotation),
        "acceleration": float(acceleration)
    }

    with counter_lock:
        gyro_batch.append(('gyro', json.dumps(message), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_gyro(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        gyro_thread = threading.Thread(target=run_gyro_simulator, args=(2, gyro_callback, stop_event, settings,
                                                                        publish_event))
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