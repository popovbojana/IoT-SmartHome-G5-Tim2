import threading
import time
from settings.settings import print_lock2, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json

mqtt_host = "localhost"
mqtt_port = 1883
batch_size = 5
rgb_led_batch = []


def rgb_led_callback(comment, on, code, settings):
    with print_lock2:
        t = time.localtime()
        print()
        print("*" * 5 + settings['name'] + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Comment: {comment}")
        print(f"On: {on} sec")

        message = {
            "pi": "PI1",
            "name": settings['name'],
            "simulated": settings['simulated'],
            "timestamp": time.time(),
            "comment": comment,
            "on": on
        }
        rgb_led_batch.append(message)

        if len(rgb_led_batch) == batch_size:
            msgs = [{"topic": "rgb_led", "payload": json.dumps(msg)} for msg in rgb_led_batch]
            mqtt_config = load_mqtt_config()
            mqtt_publish.multiple(msgs, hostname=mqtt_config['host'], port=mqtt_config['port'],
                                  auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
            rgb_led_batch.clear()


def run_rgb_led(settings, threads, stop_event, duration):
    if settings['simulated']:
        buzzer_thread = threading.Thread(target=rgb_led_callback, args=(duration, "BUZZER_OK", settings))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        from actuators.rgb_led import run_rgb_led_loop, RGB_LED
        rgb_led = RGB_LED(settings['name'], settings['red_pin'], settings['green_pin'], settings['blue_pin'])
        buzzer_thread = threading.Thread(target=run_rgb_led_loop, args=(rgb_led, 2, rgb_led_callback, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
