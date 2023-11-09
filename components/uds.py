from simulations.uds import run_uds_simulator
import threading
import time

def uds_callback(distance, code, name):
    t = time.localtime()
    print("*"*5 + name + "*"*5)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Distance: {distance}")


def run_uds(settings, threads, stop_event):
        if settings['simulated']:
            print(f"Starting {settings['name']} simulator")
            uds1_thread = threading.Thread(target = run_uds_simulator, args=(2, uds_callback, stop_event, settings['name']))
            uds1_thread.start()
            threads.append(uds1_thread)
            print(f"{settings['name']} simulator started")
        else:
            from sensors.uds import run_uds_loop, UDS
            print(f"Starting {settings['name']} loop")
            uds = UDS(settings['name'], settings['trig_pin'], settings['echo_pin'])
            uds_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event))
            uds_thread.start()
            threads.append(uds_thread)
            print(f"{settings['name']} loop started")