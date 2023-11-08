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
            from sensors.uds import get_distance
            print(f"Starting {settings['name']} loop")
            dht1_thread = threading.Thread(target=get_distance, args=())
            dht1_thread.start()
            threads.append(dht1_thread)
            print(f"{settings['name']} loop started")