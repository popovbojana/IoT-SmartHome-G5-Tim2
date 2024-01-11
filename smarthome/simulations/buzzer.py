import time


def run_buzzer_simulator(callback, stop_event, settings, publish_event, alarm_event):
    while True:
        if alarm_event.is_set():
            callback(5, "CODE", settings, publish_event)

        if stop_event.is_set():
            break

        time.sleep(int(2))