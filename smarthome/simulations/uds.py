import time
import random


def generate_values():
    while True:
        decreasing = random.choice([True, False])
        distance = 10 if decreasing else 0

        while True:
            yield distance

            if decreasing:
                distance -= 1
                if distance == 0:
                    break
            else:
                distance += 1
                if distance == 10:
                    break


def run_uds_simulator(delay, callback, stop_event, settings, publish_event):
    for d in generate_values():
        time.sleep(delay)
        callback(d, "UDSLIB_OK", settings, publish_event)
        if stop_event.is_set():
            break
