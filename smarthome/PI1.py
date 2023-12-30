import threading
from settings.settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.pir import run_pir
from components.button import run_button
from components.dms import run_dms
from components.diode import run_diode
from components.buzzer import run_buzzer
from settings.settings import print_lock

import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_sensors(settings, threads, stop_event):
    rdh1_settings = settings['Room DHT'][0]
    rdh2_settings = settings['Room DHT'][1]
    dus1_settings = settings['Door Ultrasonic Sensor'][0]
    dpir1_settings = settings['Door Motion Sensor'][0]
    rpir1_settings = settings['Room PIR'][0]
    rpir2_settings = settings['Room PIR'][1]
    ds1_settings = settings['Door Sensor'][0]
    dms_settings = settings['Door Membrane Switch'][0]

    run_dht(rdh1_settings, threads, stop_event)
    run_dht(rdh2_settings, threads, stop_event)
    run_uds(dus1_settings, threads, stop_event)
    run_pir(dpir1_settings, threads, stop_event)
    run_pir(rpir1_settings, threads, stop_event)
    run_pir(rpir2_settings, threads, stop_event)
    run_button(ds1_settings, threads, stop_event)
    run_dms(dms_settings, threads, stop_event)


def run_actuators(settings_pi1, threads, stop_event):
    thread = threading.Thread(target = menu_actuators, args=(settings_pi1, threads, stop_event,))
    thread.start()
    threads.append(thread)


def menu_actuators(settings_pi1, threads, stop_event):
    while not stop_event.is_set():
        print()
        option = input("Enter X/x to start actuator menu: ")
        if option.capitalize() == "X":
            while True:
                with print_lock:
                    print()
                    print("**** ACTUATOR MENU ****")
                    print("1) Enter 1 to change light state \n"
                          "2) Enter 2 to buzz\n"
                          "3) Enter 3 to exit\n")
                    option = input("Enter: ")
                    if option == "1":
                        dl_settings = settings_pi1['Door Light'][0]
                        run_diode(dl_settings, threads, stop_event)
                        time.sleep(1)
                    elif option == "2":
                        db_settings = settings_pi1['Door Buzzer'][0]
                        duration = input("Enter duration: ")
                        run_buzzer(db_settings, threads, stop_event, duration)
                        time.sleep(int(duration))
                    elif option == "3":
                        print("Exiting the menu. Printing is resumed.")
                        break

                    else:
                        print("Entered wrong number, try again :)")
        else:
            pass


if __name__ == "__main__":
    print('Starting PI1...')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        run_sensors(settings, threads, stop_event)
        run_actuators(settings, threads, stop_event)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app...')
        for t in threads:
            stop_event.set()