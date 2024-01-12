import threading
import time


def run_buzzer_simulator(callback, stop_event, settings, publish_event, alarm_event, system_event, clock_event):
    # condition = threading.Condition()

    while True:
        if alarm_event.is_set():
            start = time.time()

            while alarm_event.is_set():
                print("alarm")
                time.sleep(5)

            end = time.time()
            duration = end - start
            print("Duration:", str(duration))
            callback(duration, "CODE", settings, publish_event)
            alarm_event.clear()

        elif clock_event.is_set():
            start = time.time()

            while clock_event.is_set():
                print("clock")
                time.sleep(5)

            end = time.time()
            duration = end - start
            print("Duration:", str(duration))
            callback(duration, "CODE", settings, publish_event)
            clock_event.clear()

        if stop_event.is_set():
            break
