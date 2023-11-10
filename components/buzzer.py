import threading
import time
from settings.settings import print_lock2


def buzzer_callback(duration, code, name):
    with print_lock2:
        pitch = 440
        t = time.localtime()
        print()
        print("*" * 5 + name + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Pitch: {pitch}")
        print(f"Duration: {duration} sec")


def run_buzzer(settings, threads, stop_event, duration):
    if settings['simulated']:
        buzzer_thread = threading.Thread(target=buzzer_callback, args=(duration, "BUZZER_OK", settings['name']))
        buzzer_thread.start()
        threads.append(buzzer_thread)
    else:
        from actuators.buzzer import run_buzzer_loop, BUZZER
        buzzer = BUZZER(settings['pin'])
        buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer, 2, buzzer_callback, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
