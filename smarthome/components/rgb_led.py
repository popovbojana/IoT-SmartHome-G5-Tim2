import threading
import time
import paho.mqtt.publish as mqtt_publish
import json
from settings.broker_settings import HOST, PORT


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
        mqtt_publish.multiple(local_rgb_batch, hostname=HOST, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def rgb_led_callback(state, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    print("RGB: " + state)

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
        rgb_batch.append(('rgb_led', json.dumps(message), 0, False))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_rgb_led(command, settings, threads, stop_event):
    if settings['simulated']:
        rgb_led_thread = threading.Thread(target=rgb_led_callback, args=(command, "RGB_" + command, settings, publish_event))
        rgb_led_thread.start()
        threads.append(rgb_led_thread)
    else:
        from actuators.rgb_led import run_rgb_loop, RGB_LED
        rgb_led = RGB_LED(settings['name'], settings['red_pin'], settings['green_pin'], settings['blue_pin'])
        rgb_led_thread = threading.Thread(target=run_rgb_loop, args=(command, rgb_led, 2, rgb_led_callback, stop_event, settings,
                                                                    publish_event))
        rgb_led_thread.start()
        threads.append(rgb_led_thread)
