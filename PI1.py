import threading
from settings.settings import load_settings_pi1
from components.dht import run_dht
from components.uds import run_uds
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('Starting PI1...')
    settings_pi1 = load_settings_pi1()
    threads = []
    stop_event = threading.Event()
    try:
        # rdh1_settings = settings_pi1['RDH1']
        # rdh2_settings = settings_pi1['RDH2']
        dus1_settings = settings_pi1['DUS1']
        # run_dht(rdh1_settings, threads, stop_event)
        # run_dht(rdh2_settings, threads, stop_event)
        run_uds(dus1_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app...')
        for t in threads:
            stop_event.set()