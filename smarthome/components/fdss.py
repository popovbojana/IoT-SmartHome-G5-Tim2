from simulations.fdss import run_fdss_simulator
import threading
import time
import paho.mqtt.publish as mqtt_publish
import json
from settings.broker_settings import HOST, PORT

fdss_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, fdss_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_fdss_batch = fdss_batch.copy()
            publish_data_counter = 0
            fdss_batch.clear()
        mqtt_publish.multiple(local_fdss_batch, hostname=HOST, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, fdss_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def fdss_callback(alarm_time, binary, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    # t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")
    # print(f"Alarm time: {alarm_time}")
    # print(f"Binary: {binary}")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "alarm_time": alarm_time,
        "binary": binary
    }

    with counter_lock:
        fdss_batch.append(('fdss', json.dumps(message), 0, False))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_fdss(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        lcd_thread = threading.Thread(target=run_fdss_simulator, args=(2, fdss_callback, stop_event, settings,
                                                                       publish_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"{settings['name']} simulator started")
    else:
        from displays.fdss import run_fdss_loop, FDSS
        print(f"Starting {settings['name']} loop")
        fdss = FDSS(settings['name'], settings['segment_pins'], settings['digit_pins'])
        fdss_thread = threading.Thread(target=run_fdss_loop, args=(fdss, 2, fdss_callback, stop_event, settings,
                                                                   publish_event))
        fdss_thread.start()
        threads.append(fdss_thread)
        print(f"{settings['name']} loop started")
