from simulations.dms import run_dms_simulator
import threading
import time
from settings.settings import print_lock, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_config = load_mqtt_config()
dms_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()


def publisher_task(event, dms_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dms_batch = dms_batch.copy()
            publish_data_counter = 0
            dms_batch.clear()
        mqtt_publish.multiple(local_dms_batch, hostname=mqtt_config['host'], port=mqtt_config['port'],
                              auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dms_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dms_callback(key, settings, publish_event, system_event):
    global publish_data_counter, publish_data_limit

    # t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")
    # print(f"Key: {key}")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "key": key
    }

    with counter_lock:
        dms_batch.append(('dms', json.dumps(message), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dms(key, settings, threads, stop_event, system_event):
    if settings['simulated']:
        dms_thread = threading.Thread(target=dms_callback, args=(key, settings, publish_event, system_event))
        dms_thread.start()
        threads.append(dms_thread)
    else:
        from sensors.dms import run_dms_loop, DMS
        dms = DMS(settings['name'], settings['row_pins'], settings['col_pins'])
        dms_thread = threading.Thread(target=run_dms_loop, args=(dms, 2, dms_callback, stop_event, settings,
                                                                 publish_event))
        dms_thread.start()
        threads.append(dms_thread)
