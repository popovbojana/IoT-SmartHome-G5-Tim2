from simulations.pir import run_pir_simulator
import threading
import time
import paho.mqtt.publish as mqtt_publish
import json
from settings.broker_settings import HOST, PORT

pir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        mqtt_publish.multiple(local_pir_batch, hostname=HOST, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def pir_callback(motion, detected, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    # t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")
    # print(f"{motion}")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "motion_detected": detected
    }

    with counter_lock:
        pir_batch.append(('pir', json.dumps(message), 0, False))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} loop")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, pir_callback, stop_event, settings,
                                                                      publish_event))
        pir_thread.start()
        threads.append(pir_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.pir import run_pir_loop, PIR
        print(f"Starting {settings['name']} loop")
        pir = PIR(settings['name'], settings['pin'])
        pir_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, pir_callback, stop_event, settings,
                                                                 publish_event))
        pir_thread.start()
        threads.append(pir_thread)
        print(f"{settings['name']} loop started")
