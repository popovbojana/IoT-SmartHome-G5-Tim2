from simulations.uds import run_uds_simulator
import threading
import time
from settings.settings import print_lock, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_config = load_mqtt_config()
uds_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, uds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_uds_batch = uds_batch.copy()
            publish_data_counter = 0
            uds_batch.clear()
        mqtt_publish.multiple(local_uds_batch, hostname=mqtt_config['host'], port=mqtt_config['port'],
                              auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, uds_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def uds_callback(distance, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    # t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")
    # print(f"Distance: {distance}")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "distance": float(distance)
    }

    with counter_lock:
        uds_batch.append(('uds', json.dumps(message), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_uds(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        uds1_thread = threading.Thread(target=run_uds_simulator, args=(2, uds_callback, stop_event, settings, publish_event))
        uds1_thread.start()
        threads.append(uds1_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.uds import run_uds_loop, UDS
        print(f"Starting {settings['name']} loop")
        uds = UDS(settings['name'], settings['trig_pin'], settings['echo_pin'])
        uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event, settings, publish_event))
        uds_thread.start()
        threads.append(uds_thread)
        print(f"{settings['name']} loop started")
