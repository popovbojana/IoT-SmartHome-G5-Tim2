import RPi.GPIO as GPIO
import time
import random


class BUZZER:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.pitch = 440
        GPIO.setup(self.pin, GPIO.OUT)

    # def buzz(self, pitch, duration)
    def buzz(self):
        period = 1.0 / self.pitch
        delay = period / 2
        GPIO.output(self.pin, True)
        time.sleep(delay)
        GPIO.output(self.pin, False)
        time.sleep(delay)


def run_buzzer_loop(buzzer, callback, stop_event, settings, publish_event, alarm_event, system_event):
    while True:
        alarm_event.wait()
        start = time.time()
        buzzer.buzz()

        while system_event.is_set():
            buzzer.buzz()

        end = time.time()
        duration = end - start
        print("Duration:", str(duration))
        callback(duration, "CODE", settings, publish_event)
        alarm_event.clear()

        if stop_event.is_set():
            break
