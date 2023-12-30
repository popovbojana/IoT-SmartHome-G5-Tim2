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
            callback("Door is unlocked", True, "BUTTON_OK", button.name)
        else:
            callback("Door is locked", False, "BUTTON_OK", button.name)
        if stop_event.is_set():
            break
        time.sleep(delay)
