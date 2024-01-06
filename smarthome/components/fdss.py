from simulations.fdss import run_fdss_simulator
import threading
import time
from settings.settings import print_lock, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
batch_size = 5
lcd_batch = []


def fdss_callback(alarm_time, binary, code, settings):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Alarm time: {alarm_time}")
        print(f"Binary: {binary}")

        message = {
            "pi": settings['pi'],
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.time(),
            "alarm_time": alarm_time,
            "binary": binary
        }
        lcd_batch.append(message)

        if len(lcd_batch) == batch_size:
            msgs = [{"topic": "fdss", "payload": json.dumps(msg)} for msg in lcd_batch]
            mqtt_config = load_mqtt_config()
            mqtt_publish.multiple(msgs, hostname=mqtt_config['host'], port=mqtt_config['port'],
                                  auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
            lcd_batch.clear()


def run_fdss(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        lcd_thread = threading.Thread(target=run_fdss_simulator, args=(2, fdss_callback, stop_event, settings))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.fdss import run_fdss_loop, FDSS
        print(f"Starting {settings['name']} loop")
        fdss = FDSS(settings['name'], settings['segment_pins'], settings['digit_pins'])
        fdss_thread = threading.Thread(target=run_fdss_loop, args=(fdss, 2, fdss_callback, stop_event))
        fdss_thread.start()
        threads.append(fdss_thread)
        print(f"{settings['name']} loop started")