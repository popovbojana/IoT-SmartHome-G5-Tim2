import json
import threading
import time
import paho.mqtt.client as mqtt
import re

from settings.settings import load_settings
from components.dht import run_dht
from components.pir import run_pir
from components.buzzer import run_buzzer
from components.fdss import run_fdss
from components.rgb_led import run_rgb_led
from components.ir import run_ir
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
    bb_settings = settings['Bedroom Buzzer'][0]

    run_pir(rpir4_settings, threads, stop_event)
    run_dht(rdh4_settings, threads, stop_event)
    run_pir(bir_settings, threads, stop_event)
    run_buzzer(bb_settings, threads, stop_event, alarm_event, system_event, alarm_clock_event)

    ir_settings = settings['Bedroom Infrared'][0]
    run_ir(ir_settings, threads, stop_event, "0")


# def run_actuators(settings, threads, stop_event):
#     thread = threading.Thread(target=menu_actuators, args=(settings, threads, stop_event,))
#     thread.start()
#     threads.append(thread)


def validate_time_format(time_str):
    time_regex = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')

    if time_regex.match(time_str):
        return True
    else:
        return False


# def menu_actuators(settings, threads, stop_event):
#     while not stop_event.is_set():
#         print()
#         option = input("Enter X/x to start actuator menu: ")
#         if option.capitalize() == "X":
#             while True:
#                 with print_lock:
#                     print()
#                     print("**** ACTUATOR MENU ****")
#                     print("1) Enter 1 to buzz\n"
#                           "2) Enter 2 for RGB\n"
#                           "3) Enter 3 for IR Receiver\n"
#                           "4) Enter 4 for setting an alarm\n"
#                           "5) Enter 5 for setting off an alarm\n"
#                           "6) Enter 6 for removing an alarm\n"
#                           "7) Enter 7 to exit\n")
#                     option = input("Enter: ")
#                     if option == "1":
#                         bb_settings = settings['Bedroom Buzzer'][0]
#                         duration = input("Enter duration: ")
#                         run_buzzer(bb_settings, threads, stop_event, duration)
#                         time.sleep(int(duration))
#                     elif option == "2":
#                         ir_settings = settings['Bedroom Infrared'][0]
#                         ir_button = input("Enter (LEFT, RIGHT, UP, DOWN, 2, 3, 1, OK, 4, 5, 6, 7, 8, 9, *, 0, #) to select command: ")
#                         if ir_button.upper() not in ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0", "#"]:
#                             break
#                         else:
#                             run_ir(ir_settings, threads, stop_event, ir_button)
#                             time.sleep(1)
#                     elif option == "4":
#                         alarm_time = input("Enter what time you want your alarm to turn on with format HH:MM: ")
#                         if validate_time_format(alarm_time):
#                             msg = json.dumps({"time": alarm_time, "action": "add"})
#                             mqtt_client.publish("alarm-clock-pi", payload=msg)
#                         else:
#                             print("Invalid time format. Please enter the time in HH:MM format.")
#                     elif option == "5":
#                         msg = json.dumps({"time": "empty", "action": "turn-off"})
#                         mqtt_client.publish("alarm-clock-pi", payload=msg)
#                     elif option == "6":
#                         alarm_time = input("Enter what alarm you want to remove with format HH:MM: ")
#                         if validate_time_format(alarm_time):
#                             msg = json.dumps({"time": alarm_time, "action": "remove"})
#                             mqtt_client.publish("alarm-clock-pi", payload=msg)
#                         else:
#                             print("Invalid time format. Please enter the time in HH:MM format.")
#                     elif option == "7":
#                         print("Exiting the menu. Printing is resumed.")
#                         break
#
#                     else:
#                         print("Entered wrong number, try again :)")
#         else:
#             pass


def run_displays(settings, threads, stop_event):
    b4sd_settings = settings['Bedroom 4 Digit 7 Segment Display'][0]

    run_fdss(b4sd_settings, threads, stop_event)


alarm_event = threading.Event()
system_event = threading.Event()
alarm_clock_event = threading.Event()

# state_off_event = threading.Event()
# state_white_event = threading.Event()
# state_red_event = threading.Event()
# state_green_event = threading.Event()
# state_blue_event = threading.Event()
# state_yellow_event = threading.Event()
# state_purple_event = threading.Event()
# state_lightblue_event = threading.Event()
#
#
# def set_rgb_states(state_to_set, *other_states):
#     state_to_set.set()
#
#     for state in other_states:
#         state.clear()

def on_connect(client, userdata, flags, rc):
    topics = ['rgb_commands', 'alarm-on', 'alarm-off', 'system-on', 'system-off', 'alarm-clock-on', 'alarm-clock-server']

    if rc == 0:
        print("Connected to MQTT broker")

        for topic in topics:
            client.subscribe(topic)
            print("Subscribed to: " + topic)

    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        # print(payload)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Invalid payload: {msg.payload}")
        return

    if msg.topic == 'rgb_commands':
        command = payload['command']
        brgb_settings = settings_pi3['Bedroom RGB'][0]
        run_rgb_led(command, brgb_settings, threads_pi3, stop_event_pi3)

        # if command == "OFF":
        #     set_rgb_states(state_off_event, state_white_event, state_red_event, state_green_event, state_blue_event, state_yellow_event, state_purple_event, state_lightblue_event)
        # elif command == "WHITE":
        #     set_rgb_states(state_white_event, state_off_event, state_red_event, state_green_event, state_blue_event, state_yellow_event, state_purple_event, state_lightblue_event)
        # elif command == "RED":
        #     set_rgb_states(state_red_event, state_off_event, state_white_event, state_green_event, state_blue_event, state_yellow_event, state_purple_event, state_lightblue_event)
        # elif command == "GREEN":
        #     set_rgb_states(state_green_event, state_off_event, state_white_event, state_red_event, state_green_event, state_blue_event, state_yellow_event, state_purple_event, state_lightblue_event)
        # elif command == "BLUE":
        #     set_rgb_states(state_blue_event, state_off_event, state_white_event, state_red_event, state_green_event, state_blue_event, state_yellow_event, state_purple_event, state_lightblue_event)
        # elif command == "YELLOW":
        #     set_rgb_states(state_yellow_event, state_off_event, state_white_event, state_red_event, state_green_event, state_blue_event, state_yellow_event, state_purple_event, state_lightblue_event)
        # elif command == "PURPLE":
        #     set_rgb_states(state_purple_event, state_off_event, state_white_event, state_red_event, state_green_event, state_blue_event, state_yellow_event, state_purple_event, state_lightblue_event)
        # elif command == "LIGHT_BLUE":
        #     set_rgb_states(state_lightblue_event, state_white_event, state_red_event, state_green_event, state_blue_event, state_yellow_event, state_purple_event, state_lightblue_event)

    elif msg.topic == 'alarm-on':
        alarm_event.set()
        print(payload)
    elif msg.topic == 'alarm-off':
        alarm_event.clear()
        print("ALARM OFF")
    elif msg.topic == 'system-on':
        system_event.set()
        print("SYSTEM ON")
    elif msg.topic == 'system-off':
        system_event.clear()
        print("SYSTEM OFF")
    elif msg.topic == 'alarm-clock-server':
        if payload["event"] == "alarm-on":
            print("UKLJUCIO budilnik")
            alarm_clock_event.set()
        elif payload["event"] == "alarm-off":
            alarm_clock_event.clear()
            print("iskljucen budilnik")


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
        # run_actuators(settings_pi3, threads_pi3, stop_event_pi3)
        run_displays(settings_pi3, threads_pi3, stop_event_pi3)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app...')
        for t in threads_pi3:
            stop_event_pi3.set()
