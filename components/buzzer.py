from simulations.buzzer import run_buzzer_simulator
import threading
import time
from settings.settings import print_lock


def buzzer_callback(buzz, pitch, duration, code, name):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + name + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Pitch: {pitch}")
        print(f"Duration: {duration} sec")
        print(f"{buzz}")


def run_buzzer(settings, threads, stop_event):
        if settings['simulated']:
            print(f"Starting {settings['name']} simulator")
            buzzer_thread = threading.Thread(target = run_buzzer_simulator, args=(2, buzzer_callback, stop_event, settings['name']))
            buzzer_thread.start()
            threads.append(buzzer_thread)
            print(f"{settings['name']} simulator started")
        else:
            from sensors.buzzer import run_buzzer_loop, BUZZER
            print(f"Starting {settings['name']} loop")
            buzzer = BUZZER(settings['pin'])
            buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer, 2, buzzer_callback, stop_event))
            buzzer_thread.start()
            threads.append(buzzer_thread)
            print(f"{settings['name']} loop started")