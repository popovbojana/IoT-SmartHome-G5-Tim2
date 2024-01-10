import threading
import time
from settings.settings import print_lock2, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json


mqtt_config = load_mqtt_config()
rgb_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, rgb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rgb_batch = rgb_batch.copy()
            publish_data_counter = 0
            rgb_batch.clear()
        mqtt_publish.multiple(local_rgb_batch, hostname=mqtt_config['host'], port=mqtt_config['port'],
                              auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rgb_led_callback(state, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    # t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")
    # print(f"State: {state}")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "state": state,
    }

    with counter_lock:
        rgb_batch.append(('rgb_led', json.dumps(message), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rgb_led(settings, threads, stop_event, state):
    if settings['simulated']:
        buzzer_thread = threading.Thread(target=rgb_led_callback, args=(state, "RGB_" + state, settings, publish_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        from actuators.rgb_led import run_rgb_loop, RGB_LED
        rgb_led = RGB_LED(settings['name'], settings['red_pin'], settings['green_pin'], settings['blue_pin'])
        buzzer_thread = threading.Thread(target=run_rgb_loop, args=(rgb_led, 2, rgb_led_callback, stop_event, settings,
                                                                    publish_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
