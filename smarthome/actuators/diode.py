import RPi.GPIO as GPIO
import time


class DIODE:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def turnOn(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turnOff(self):
        GPIO.output(self.pin, GPIO.LOW)


def run_diode_loop(diode, callback, stop_event, settings, publish_event):
    diode.turnOn()
    callback(True, "DIODE_OK", settings, publish_event)
    time.sleep(10)
    diode.turnOff()
    callback(False, "DIODE_OK", settings, publish_event)
