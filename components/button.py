from simulations.button import run_button_simulator
import threading
import time
from settings.settings import print_lock


def button_callback(pushed, code, name):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + name + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"{pushed}")


def run_button(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} loop")
        button_thread = threading.Thread(target=run_button_simulator, args=(2, button_callback, stop_event, settings['name']))
        button_thread.start()
        threads.append(button_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.button import run_button_loop, Button
        print(f"Starting {settings['name']} loop")
        button = Button(settings['name'], settings['pin'])
        button_thread = threading.Thread(target=run_button_loop, args=(button, 2, button_callback, stop_event))
        button_thread.start()
        threads.append(button_thread)
        print(f"{settings['name']} loop started")
