import time
import random


def generate_values():
    while True:
        yield random.choice([True, False])


def run_pir_simulator(delay, callback, stop_event, settings, publish_event):
    for motion in generate_values():
        time.sleep(delay)
        if motion:
            callback("Motion detected", True, "PIR_OK", settings, publish_event)
        else:
            callback("No motion", False, "PIR_OK", settings, publish_event)
        if stop_event.is_set():
            break
