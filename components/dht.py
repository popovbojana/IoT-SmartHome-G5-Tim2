from simulations.dht import run_dht_simulator
import threading
import time

def dht_callback(humidity, temperature, code, name):
    t = time.localtime()
    print("*"*5 + name + "*"*5)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Humidity: {humidity}%")
    print(f"Temperature: {temperature}°C")


def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            print(f"Starting {settings['name']} simulator")
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, stop_event, settings['name']))
            dht1_thread.start()
            threads.append(dht1_thread)
            print(f"{settings['name']} simulator started")
        else:
            from sensors.dht import run_dht_loop, DHT
            print(f"Starting {settings['name']} loop")
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
            dht1_thread.start()
            threads.append(dht1_thread)
            print(f"{settings['name']} loop started")