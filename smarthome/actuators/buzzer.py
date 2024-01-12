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


def run_buzzer_loop(buzzer, callback, stop_event, settings, publish_event, alarm_event):
    while not stop_event.is_set():
        start_time = time.time()  # Record the start time before waiting for the event
        alarm_event.wait()
        end_time = time.time()  # Record the end time when the event is set
        alarm_duration = end_time - start_time
        print("ALARM DURATIONNNNN", str(alarm_duration))
        callback(alarm_duration, "CODE", settings, publish_event)


    #     if stop_event.is_set():
    #         break
    #     time.sleep(int(duration))
