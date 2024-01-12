from simulations.button import run_button_simulator
import threading
import time
import paho.mqtt.publish as mqtt_publish
import json
from settings.settings import load_mqtt_config

mqtt_config = load_mqtt_config()
button_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, button_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_button_batch = button_batch.copy()
            publish_data_counter = 0
            button_batch.clear()
        mqtt_publish.multiple(local_button_batch, hostname=mqtt_config['host'], port=mqtt_config['port'],
                              auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, button_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def button_callback(pushed, unlocked, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    # t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")
    # print(f"{pushed}")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "door_unlocked": unlocked,
        "code": code
    }

    with counter_lock:
        button_batch.append(('button', json.dumps(message), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_button(settings, threads, stop_event, alarm_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} loop")
        button_thread = threading.Thread(target=run_button_simulator, args=(2, button_callback, stop_event, settings,
                                                                            publish_event, alarm_event))
        button_thread.start()
        threads.append(button_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.button import run_button_loop, Button
        print(f"Starting {settings['name']} loop")
        button = Button(settings['name'], settings['pin'])
        button_thread = threading.Thread(target=run_button_loop, args=(button, 2, button_callback, stop_event, settings,
                                                                       publish_event, alarm_event))
        button_thread.start()
        threads.append(button_thread)
        print(f"{settings['name']} loop started")
