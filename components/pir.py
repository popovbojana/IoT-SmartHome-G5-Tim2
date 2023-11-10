from simulations.pir import run_pir_simulator
import threading
import time
from settings.settings import print_lock


def pir_callback(motion, code, name):
    with print_lock:
        t = time.localtime()
        print()
        print("*" * 5 + name + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"{motion}")


def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} loop")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, pir_callback, stop_event, settings['name']))
        pir_thread.start()
        threads.append(pir_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.pir import run_pir_loop, PIR
        print(f"Starting {settings['name']} loop")
        pir = PIR(settings['name'], settings['pin'])
        pir_thread = threading.Thread(target=run_pir_loop, args=(pir, 2, pir_callback, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
        print(f"{settings['name']} loop started")
