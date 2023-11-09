import RPi.GPIO as GPIO
import time


class PIR:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.detected_motion = False
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.motion_detected)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.no_motion)

    def motion_detected(self, channel):
        self.detected_motion = True

    def no_motion(self, channel):
        self.detected_motion = False

    def read_pir(self):
        return self.detected_motion


def run_pir_loop(pir, delay, callback, stop_event):
    while True:
        if pir.read_pir():
            callback("Motion detected", "PIR_OK", pir.name)
        else:
            callback("No motion", "PIR_OK", pir.name)
        if stop_event.is_set():
            break
        time.sleep(delay)
