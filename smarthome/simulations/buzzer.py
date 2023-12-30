import time
import random


def generate_values():
    while True:
        pitch = random.randint(400, 800)
        duration = random.uniform(0.1, 0.5)
        yield pitch, duration


def run_buzzer_simulator(delay, callback, stop_event, name):
    for p, d in generate_values():
        time.sleep(delay)
        callback("BUZZZzz", p, d, "BUZZER_OK", name)
        if stop_event.is_set():
            break

