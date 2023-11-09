import time
import random


def generate_values():
    while True:
        yield random.choice([True, False])


def run_button_simulator(delay, callback, stop_event, name):
    for pushed in generate_values():
        time.sleep(delay)
        if pushed:
            callback("Door is unlocked", "BUTTON_OK", name)
        else:
            callback("Door is locked", "BUTTON_OK", name)
        if stop_event.is_set():
            break
