import threading
import time
from simulations.buzzer import run_buzzer_simulator
import paho.mqtt.publish as mqtt_publish
import json
from settings.broker_settings import HOST, PORT

buzzer_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()


def publisher_task(event, buzzer_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_buzzer_batch = buzzer_batch.copy()
            publish_data_counter = 0
            buzzer_batch.clear()
        mqtt_publish.multiple(local_buzzer_batch, hostname=HOST, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, buzzer_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def buzzer_callback(duration, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    pitch = 440
    t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")
    # # print(f"Pitch: {pitch}")
    # print(f"Duration: {duration} sec")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "pitch": float(pitch),
        "duration": float(duration)
    }

    with counter_lock:
        buzzer_batch.append(('buzzer', json.dumps(message), 0, False))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_buzzer(settings, threads, stop_event, alarm_event, system_event, alarm_clock_event):
    if settings['simulated']:
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(buzzer_callback, stop_event, settings,
                                                                            publish_event, alarm_event, system_event,
                                                                            alarm_clock_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        from actuators.buzzer import run_buzzer_loop, BUZZER
        buzzer = BUZZER(settings['pin'])
        buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer, buzzer_callback, stop_event, settings,
                                                                       publish_event, alarm_event, system_event, alarm_clock_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
