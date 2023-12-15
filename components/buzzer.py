import threading
import time
from settings.settings import print_lock2
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
batch_size = 5
buzzer_batch = []


def buzzer_callback(duration, code, settings):
    with print_lock2:
        pitch = 440
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Pitch: {pitch}")
        print(f"Duration: {duration} sec")

        message = {
            "pi": "PI1",
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.strftime('%H:%M:%S', t),
            "pitch": pitch,
            "duration": duration
        }
        buzzer_batch.append(message)

        if len(buzzer_batch) == batch_size:
            msgs = [{"topic": "buzzer", "payload": json.dumps(msg)} for msg in buzzer_batch]
            mqtt_publish.multiple(msgs, hostname=mqtt_host, port=mqtt_port)
            buzzer_batch.clear()


def run_buzzer(settings, threads, stop_event, duration):
    if settings['simulated']:
        buzzer_thread = threading.Thread(target=buzzer_callback, args=(duration, "BUZZER_OK", settings))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        from actuators.buzzer import run_buzzer_loop, BUZZER
        buzzer = BUZZER(settings['pin'])
        buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer, 2, buzzer_callback, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
