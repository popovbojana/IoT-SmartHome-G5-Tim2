import time
import random


def generate_values():
    while True:
        yield random.randint(1, 6)


def run_button_simulator(delay, callback, stop_event, settings, publish_event, alarm_event):
    for pushed in generate_values():
        time.sleep(delay)

        if pushed > 5:
            callback("Door is unlocked", True, "BUTTON_5_SEC", settings, publish_event)
        else:
            callback("Door is unlocked", True, "BUTTON_OK", settings, publish_event)

        if stop_event.is_set():
            break
