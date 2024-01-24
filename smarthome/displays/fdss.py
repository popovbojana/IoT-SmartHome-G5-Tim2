import RPi.GPIO as GPIO
import time


class FDSS:
    def __init__(self, name, segment_pins, digit_pins):
        self.segment_pins = segment_pins
        self.digit_pins = digit_pins
        self.name = name
        self.num = {' ': (0, 0, 0, 0, 0, 0, 0),
                    '0': (1, 1, 1, 1, 1, 1, 0),
                    '1': (0, 1, 1, 0, 0, 0, 0),
                    '2': (1, 1, 0, 1, 1, 0, 1),
                    '3': (1, 1, 1, 1, 0, 0, 1),
                    '4': (0, 1, 1, 0, 0, 1, 1),
                    '5': (1, 0, 1, 1, 0, 1, 1),
                    '6': (1, 0, 1, 1, 1, 1, 1),
                    '7': (1, 1, 1, 0, 0, 0, 0),
                    '8': (1, 1, 1, 1, 1, 1, 1),
                    '9': (1, 1, 1, 1, 0, 1, 1)}

        GPIO.setmode(GPIO.BCM)
        for segment in segment_pins:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

        for digit in digit_pins:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)

    def show_time(self):
        binary = []
        n = time.ctime()[11:13] + time.ctime()[14:16]
        s = str(n).rjust(4)
        for digit in range(4):
            b = ""
            for loop in range(0, 7):
                GPIO.output(self.segment_pins[loop], self.num[s[digit]][loop])
                if (int(time.ctime()[18:19]) % 2 == 0) and (digit == 1):
                    GPIO.output(25, 1)
                else:
                    GPIO.output(25, 0)
                b = b + str(n)
            GPIO.output(self.digit_pins[digit], 0)
            time.sleep(0.001)
            GPIO.output(self.digit_pins[digit], 1)
            binary.append(b)
        return n, binary


def run_fdss_loop(fdss, delay, callback, stop_event, settings, publish_event):
    while True:
        a, b = fdss.show_time()
        callback(a, b, "FDSS_OK", settings, publish_event)
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)
