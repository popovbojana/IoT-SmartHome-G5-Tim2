from simulations.diode import run_diode_simulator
import threading
import time
from settings.settings import print_lock


def diode_callback(on, code, name):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + name + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"{on}")


def run_diode(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} loop")
        diode_thread = threading.Thread(target=run_diode_simulator, args=(2, diode_callback, stop_event, settings['name']))
        diode_thread.start()
        threads.append(diode_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.diode import run_diode_loop, DIODE
        print(f"Starting {settings['name']} loop")
        diode = DIODE(settings['name'], settings['pin'])
        diode_thread = threading.Thread(target=run_diode_loop, args=(diode, 2, diode_callback, stop_event))
        diode_thread.start()
        threads.append(diode_thread)
        print(f"{settings['name']} loop started")
