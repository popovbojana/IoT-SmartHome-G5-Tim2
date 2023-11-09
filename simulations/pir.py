import time
import random


def generate_values():
    while True:
        yield random.choice([True, False])


def run_pir_simulator(delay, callback, stop_event, name):
    for motion in generate_values():
        time.sleep(delay)
        if motion:
            callback("Motion detected", "PIR_OK", name)
        else:
            callback("No motion", "PIR_OK", name)
        if stop_event.is_set():
            break
