import RPi.GPIO as GPIO
import time
import threading


class Button:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.pushed = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self.button_changed)

    def button_changed(self, channel):
        self.pushed = GPIO.input(self.pin) == GPIO.LOW

    def read_state(self):
        return self.pushed


def run_button_loop(button, delay, callback, stop_event):
    while True:
        if button.read_state():
            callback("Door is unlocked", "BUTTON_OK", button.name)
        else:
            callback("Door is locked", "BUTTON_OK", button.name)
        if stop_event.is_set():
            break
        time.sleep(delay)

# Primjer korištenja klase DoorSensor
if __name__ == "__main__":
    door_sensor = DoorSensor("DS1", 4)  # Inicijalizacija Door Sensora s pinom 4

    def door_callback(status, code, name):
        print(f"Door Status: {status} - {name}")

    stop_event = threading.Event()  # Event za zaustavljanje petlje
    door_sensor_thread = threading.Thread(target=run_door_sensor_loop, args=(door_sensor, 1, door_callback, stop_event))
    door_sensor_thread.start()

    # Ovdje može biti ostatak vašeg programa ili petlja koja završava petlju samo ako je potrebno

    stop_event.set()  # Postavljanje eventa za zaustavljanje petlje
    door_sensor_thread.join()  # Čekanje da se petlja završi
