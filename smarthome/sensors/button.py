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


def run_button_loop(button, delay, callback, stop_event, settings, publish_event, switch_event):
    while True:
        switch_event.wait()

        if button.read_state():
            callback("Door is unlocked", True, "BUTTON_OK", settings, publish_event)
            start_time = time.time()

            while button.read_state():
                time.sleep(0.1)
                elapsed_time = time.time() - start_time

                if elapsed_time > 5:
                    callback("Door is unlocked", True, "BUTTON_5_SEC", settings, publish_event)

        time.sleep(delay)
        switch_event.clear()

        if stop_event.is_set():
            GPIO.cleanup()
            break
