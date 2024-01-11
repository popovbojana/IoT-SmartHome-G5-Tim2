import time
import random


def run_pir_simulator(delay, callback, stop_event, settings, publish_event):
    while True:
        time.sleep(delay)
        motion_detected = random.random() < 0.3
        if motion_detected:
            callback("Motion detected", True, "PIR_OK", settings, publish_event)
        if stop_event.is_set():
            break
