import time
import random


# todo: odraditi bolju simulaciju
def generate_values(initial_rotation=0, initial_acceleration=0):
    rotation = initial_rotation
    acceleration = initial_acceleration
    while True:
        rotation = rotation + random.uniform(-1, 1)
        acceleration = acceleration + random.uniform(-1, 1)
        yield rotation, acceleration


def run_gyro_simulator(delay, callback, stop_event, name):
    for r, a in generate_values():
        time.sleep(delay)
        callback(r, a, "GYRO_OK", name)

        if stop_event.is_set():
            break
