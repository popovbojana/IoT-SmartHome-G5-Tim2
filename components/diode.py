import threading
import time
from settings.settings import print_lock2

state = False
def diode_callback(code, name):
    global state
    with print_lock2:
        t = time.localtime()
        print()
        print("*" * 5 + name + "*" * 5)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        if state:
            state = False
            print("Light is on\n")
        else:
            state = True
            print("Light is off\n")


def run_diode(settings, threads, stop_event):
    if settings['simulated']:
        diode_thread = threading.Thread(target=diode_callback, args=('DIODE_OK', settings['name']))
        diode_thread.start()
        threads.append(diode_thread)
    else:
        from actuators.diode import run_diode_loop, DIODE
        diode = DIODE(settings['name'], settings['pin'])
        diode_thread = threading.Thread(target=run_diode_loop, args=(diode, 2, diode_callback, stop_event))
        diode_thread.start()
        threads.append(diode_thread)
