import time
import random


def generate_values():
    while True:
        yield random.choice([True, False])


def run_diode_simulator(delay, callback, stop_event, name):
    for on in generate_values():
        time.sleep(delay)
        if on:
            callback("Lights are on", "DIODE_ON", name)
        else:
            callback("Lights are off", "DIODE_OFF", name)
        if stop_event.is_set():
            break
