import threading
import time
from settings.settings import load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json


state = False

mqtt_config = load_mqtt_config()
diode_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, diode_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_diode_batch = diode_batch.copy()
            publish_data_counter = 0
            diode_batch.clear()
        mqtt_publish.multiple(local_diode_batch, hostname=mqtt_config['host'], port=mqtt_config['port'],
                              auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, diode_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def diode_callback(on, code, settings, publish_event):
    global state, publish_data_counter, publish_data_limit

    # t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")

    on = on
    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "light_state": on,
    }
    with counter_lock:
        diode_batch.append(('diode', json.dumps(message), 0, True))
        publish_data_counter += 1

    if settings['simulated']:
        # print("Light is on")
        time.sleep(10)
        on = False
        # print("Light is off")

        message = {
            "pi": settings['pi'],
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.time(),
            "light_state": on,
        }
        with counter_lock:
            diode_batch.append(('diode', json.dumps(message), 0, True))
            publish_data_counter += 1


        # if not state:
        #     state = True
        #     on = True
        #     print("Light is on\n")
        # else:
        #     state = False
        #     on = False
        #     print("Light is off\n")
    # else:
    #     if not on:
    #         print("Light is on\n")
    #     else:
    #         print("Light is off\n")
    #
    # message = {
    #     "pi": settings['pi'],
    #     "name": settings['name'],
    #     "simulated": settings['simulated'],
    #     "timestamp": time.time(),
    #     "light_state": on,
    # }

    with counter_lock:
        diode_batch.append(('diode', json.dumps(message), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_diode(settings, threads, stop_event):
    if settings['simulated']:
        diode_thread = threading.Thread(target=diode_callback, args=(True, 'DIODE_OK', settings, publish_event))
        diode_thread.start()
        threads.append(diode_thread)
    else:
        from actuators.diode import run_diode_loop, DIODE
        diode = DIODE(settings['name'], settings['pin'])
        diode_thread = threading.Thread(target=run_diode_loop, args=(diode, diode_callback, stop_event, settings,
                                                                     publish_event))
        diode_thread.start()
        threads.append(diode_thread)
