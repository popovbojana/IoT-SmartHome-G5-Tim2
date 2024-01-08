import time


def run_buzzer_simulator(duration, callback, stop_event, settings, publish_event):
    time.sleep(int(duration))
    callback(duration, "BUZZER_OK", settings, publish_event)
