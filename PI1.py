import threading
from settings.settings import load_settings_pi1
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
from components.button import run_button
from components.dms import run_dms
from components.diode import run_diode

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
        # rdh1_settings = settings_pi1['Room DHT'][0]
        # rdh2_settings = settings_pi1['Room DHT'][1]
        # dus1_settings = settings_pi1['Door Ultrasonic Sensor']
        # dpir1_settings = settings_pi1['Door Motion Sensor']
        # rpir1_settings = settings_pi1['Room PIR'][0]
        # rpir2_settings = settings_pi1['Room PIR'][1]
        # ds1_settings = settings_pi1["Door Sensor"]
        # dms_settings = settings_pi1["Door Membrane Switch"]
        dl_settings = settings_pi1["Door Light"]

        # run_dht(rdh1_settings, threads, stop_event)
        # run_dht(rdh2_settings, threads, stop_event)
        # run_uds(dus1_settings, threads, stop_event)
        # run_pir(dpir1_settings, threads, stop_event)
        # run_pir(rpir1_settings, threads, stop_event)
        # run_pir(rpir2_settings, threads, stop_event)
        # run_button(ds1_settings, threads, stop_event)
        # run_dms(dms_settings, threads, stop_event)
        run_diode(dl_settings, threads, stop_event)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app...')
        for t in threads:
            stop_event.set()