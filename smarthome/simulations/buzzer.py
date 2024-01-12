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
    # start_time = None
    #
    # while True:
    #     if alarm_event.is_set() and start_time is None:
    #         start_time = time.time()
    #         print("ALARM IS ON!!!.")
    #
    #     if not alarm_event.is_set() and start_time is not None:
    #         end_time = time.time()
    #         elapsed_time = end_time - start_time
    #         start_time = None
    #         callback(elapsed_time, "CODE", settings, publish_event)
    #         print("ALARM IS OFF!!!")
    #
    #     if stop_event.is_set():
    #         break