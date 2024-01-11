import threading
import time
import paho.mqtt.client as mqtt

from settings.settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.buzzer import run_buzzer
from components.fdss import run_fdss
from components.rgb_led import run_rgb_led
from settings.settings import print_lock
from settings.broker_settings import HOST, PORT


try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)
except:
    pass


def run_sensors(settings, threads, stop_event):
    rpir4_settings = settings['Room PIR'][0]
    rdh4_settings = settings['Room DHT'][0]
    bir_settings = settings['Bedroom Infrared'][0]

    run_pir(rpir4_settings, threads, stop_event)
    run_dht(rdh4_settings, threads, stop_event)
    run_pir(bir_settings, threads, stop_event)


def run_actuators(settings, threads, stop_event):
    thread = threading.Thread(target=menu_actuators, args=(settings, threads, stop_event,))
    thread.start()
    threads.append(thread)


def menu_actuators(settings, threads, stop_event):
    while not stop_event.is_set():
        print()
        option = input("Enter X/x to start actuator menu: ")
        if option.capitalize() == "X":
            while True:
                with print_lock:
                    print()
                    print("**** ACTUATOR MENU ****")
                    print("1) Enter 1 to buzz\n"
                          "2) Enter 2 for RGB\n"
                          "3) Enter 3 to exit\n")
                    option = input("Enter: ")
                    if option == "1":
                        bb_settings = settings['Bedroom Buzzer'][0]
                        duration = input("Enter duration: ")
                        run_buzzer(bb_settings, threads, stop_event, duration)
                        time.sleep(int(duration))
                    elif option == "2":
                        brgb_settings = settings['Bedroom RGB'][0]
                        color = input("Enter (white, red, green, blue, yellow, purple or light_blue) to select light,\n off to turn off:")
                        if color.upper() not in ["WHITE", "RED", "GREEN", "BLUE", "YELLOW", "PURPLE", "LIGHT_BLUE", "OFF"]:
                            break
                        else:
                            run_rgb_led(brgb_settings, threads, stop_event, color)
                            time.sleep(1)
                    elif option == "3":
                        print("Exiting the menu. Printing is resumed.")
                        break

                    else:
                        print("Entered wrong number, try again :)")
        else:
            pass


def run_displays(settings, threads, stop_event):
    b4sd_settings = settings['Bedroom 4 Digit 7 Segment Display'][0]

    run_fdss(b4sd_settings, threads, stop_event)


alarm_event = threading.Event()
system_event = threading.Event()


def on_connect(client, userdata, flags, rc):
    topics = ['rgb_commands', 'alarm-on', 'alarm-off', 'system-on', 'system-off']

    if rc == 0:
        print("Connected to MQTT broker")

        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)

    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    if msg.topic == 'rgb_commands':
        pass
    elif msg.topic == 'alarm-on':
        pass
    elif msg.topic == 'alarm-off':
        pass
    elif msg.topic == 'system-on':
        pass
    elif msg.topic == 'system-off':
        pass


if __name__ == "__main__":
    print('Starting PI3...')
    settings_pi3 = load_settings('settings/settings_pi3.json')
    threads_pi3 = []
    stop_event_pi3 = threading.Event()

    # MQTT Config
    mqtt_client = mqtt.Client()
    # mqtt_client.username_pw_set(username="client", password="password")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg)
    mqtt_client.connect(HOST, PORT, 60)
    mqtt_client.loop_start()

    try:
        run_sensors(settings_pi3, threads_pi3, stop_event_pi3)
        run_actuators(settings_pi3, threads_pi3, stop_event_pi3)
        run_displays(settings_pi3, threads_pi3, stop_event_pi3)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app...')
        for t in threads_pi3:
            stop_event_pi3.set()
