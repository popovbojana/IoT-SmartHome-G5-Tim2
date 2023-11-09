import RPi.GPIO as GPIO
import time
import random


class BUZZER:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def buzz(self, pitch, duration):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)

        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)


def run_buzzer_loop(buzzer, delay, callback, stop_event):
    while True:
        pitch = 440
        duration = 0.1
        buzzer.buzz(pitch, duration)
        callback("BUZZZzz", pitch, duration, "BUZZER_OK", buzzer.name)

        if stop_event.is_set():
            break
        time.sleep(delay)
