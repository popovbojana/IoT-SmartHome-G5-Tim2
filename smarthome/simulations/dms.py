import time
import random


def generate_values():
    while True:
        yield random.choice(["1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"])


def run_dms_simulator(delay, callback, stop_event, settings, publish_event):
    for key in generate_values():
        time.sleep(delay)
        callback(key, "DMS_OK", settings, publish_event)
        if stop_event.is_set():
            break
