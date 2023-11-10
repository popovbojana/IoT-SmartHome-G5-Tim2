import RPi.GPIO as GPIO
import time
import threading


class DIODE:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def turnOn(self):
        GPIO.setup(self.pin, GPIO.HIGH)

    def turnOff(self):
        GPIO.setup(self.pin, GPIO.LOW)


def run_diode_loop(diode, delay, callback, stop_event):
    on_off = ''
    while on_off != 'cancel':
        on_off = input("Enter on/off to turn on/off the diode or cancel to exit: ")
        if on_off == 'on':
            diode.turnOn()
            callback("Light are on", "DIODE_OK", diode.name)
        elif on_off == 'off':
            diode.turnOff()
            callback("Light are off", "DIODE_OK", diode.name)
        if stop_event.is_set():
            break
        time.sleep(delay)
