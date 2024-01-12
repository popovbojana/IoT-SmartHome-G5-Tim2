import time


def run_buzzer_simulator(callback, stop_event, settings, publish_event, alarm_event, system_event):
    while True:
        alarm_event.wait()
        start = time.time()

        while system_event.is_set():
            time.sleep(0.5)

        end = time.time()
        duration = end - start
        print("Duration:", str(duration))
        callback(duration, "CODE", settings, publish_event)
        alarm_event.clear()

        if stop_event.is_set():
            break