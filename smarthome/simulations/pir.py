import time


def generate_values():
    interval = 11  # interval u sekundama
    next_motion_time = time.time() + interval
    while True:
        current_time = time.time()
        if current_time >= next_motion_time:
            yield True
            next_motion_time = current_time + interval
        else:
            time.sleep(0.1)  # Čekanje kratko vrijeme kako biste izbjegli nepotrebno opterećenje CPU-a


def run_pir_simulator(delay, callback, stop_event, settings, publish_event):
    for motion in generate_values():
        time.sleep(delay)
        callback("Motion detected", True, "PIR_OK", settings, publish_event)
        if stop_event.is_set():
            break
