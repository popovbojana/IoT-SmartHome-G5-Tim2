from simulations.dms import run_dms_simulator
import threading
import time


def dms_callback(key, code, name):
    t = time.localtime()
    print("*"*5 + name + "*"*5)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Key: {key}")


def run_dms(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} loop")
        dms_thread = threading.Thread(target=run_dms_simulator, args=(2, dms_callback, stop_event, settings['name']))
        dms_thread.start()
        threads.append(dms_thread)
        print(f"{settings['name']} simulator started")
    else:
        from sensors.dms import run_dms_loop, DMS
        print(f"Starting {settings['name']} loop")
        dms = DMS(settings['name'], settings['row_pins'], settings['col_pins'])
        dms_thread = threading.Thread(target=run_dms_loop, args=(dms, 2, dms_callback, stop_event))
        dms_thread.start()
        threads.append(dms_thread)
        print(f"{settings['name']} loop started")
