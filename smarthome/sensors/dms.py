import RPi.GPIO as GPIO
import time


class DMS:
    def __init__(self, name, row_pins, col_pins):
        self.name = name
        self.row_pins = row_pins
        self.col_pins = col_pins
        self.keys = [
            ["1", "2", "3", "A"],
            ["4", "5", "6", "B"],
            ["7", "8", "9", "C"],
            ["*", "0", "#", "D"]
        ]
        for row_pin in self.row_pins:
            GPIO.setup(row_pin, GPIO.OUT)
            GPIO.output(row_pin, GPIO.LOW)
        for col_pin in self.col_pins:
            GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_key(self):
        for i, row_pin in enumerate(self.row_pins):
            GPIO.output(row_pin, GPIO.HIGH)
            for j, col_pin in enumerate(self.col_pins):
                if not GPIO.input(col_pin):
                    GPIO.output(row_pin, GPIO.LOW)
                    return self.keys[i][j]
            GPIO.output(row_pin, GPIO.LOW)
        return None


def run_dms_loop(dms, delay, callback, stop_event, settings, publish_event):
    while True:
        key = dms.read_key()
        callback(key, "DMS_OK", settings, publish_event)
        if stop_event.is_set():
            break
        time.sleep(delay)

