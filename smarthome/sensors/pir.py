import RPi.GPIO as GPIO
import time


class PIR:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.detected_motion = False
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.motion_detected)

    def motion_detected(self, channel):
        self.detected_motion = True

    def read_pir(self):
        return self.detected_motion

    def reset(self):
        self.detected_motion = False


def run_pir_loop(pir, delay, callback, stop_event, settings, publish_event):
    while True:
        if pir.read_pir():
            callback("Motion detected", True, "PIR_OK", settings, publish_event)
            pir.reset()
        else:
            callback("No motion detected", False, "PIR_OK", settings, publish_event)
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)
