import time
import random


def generate_values():
    while True:
        acceleration = random.uniform(-10, 10)
        rotation = random.uniform(-180, 180)

        yield acceleration, rotation


def run_gyro_simulator(delay, callback, stop_event, settings, publish_event):
    for a, r in generate_values():
        time.sleep(delay)
        callback(r, a, "GYROLIB_OK", settings, publish_event)
        if stop_event.is_set():
            break
