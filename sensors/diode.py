import RPi.GPIO as GPIO
import time
import threading


class DIODE:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.bright = False
        GPIO.setup(self.pin, GPIO.OUT)

    def turnOn(self):
        GPIO.setup(self.pin, GPIO.HIGH)

    def turnOff(self):
        GPIO.setup(self.pin, GPIO.LOW)


def run_diode_loop(diode, delay, callback, stop_event, cancel):
    while cancel != 'cancel':
        on_off = input("Turn on or off the diode")
        if on_off == 'on':
            diode.turnOn()
            callback("Lights are on", "DIODE_ON", diode.name)
        elif on_off == 'off':
            diode.turnOff()
            callback("Lights are off", "DIODE_OFF", diode.name)
        if stop_event.is_set():
            break
        time.sleep(delay)
