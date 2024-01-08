import RPi.GPIO as GPIO
import time


class RGB_LED:
    def __init__(self, name, red_pin, green_pin, blue_pin):
        self.name = name
        self.RED_PIN = red_pin
        self.GREEN_PIN = green_pin
        self.BLUE_PIN = blue_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.BLUE_PIN, GPIO.OUT)

    def turnOff(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)

    def white(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)

    def red(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)

    def green(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)

    def blue(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)

    def yellow(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)

    def purple(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)

    def lightBlue(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)


def run_rgb_loop(rgb_led, delay, callback, stop_event, settings, publish_event):
    command = ''
    while command != 'cancel':
        command = input(
            "Enter (white, red, green, blue, yellow, purple or light_blue) to select light,\n off to turn off or "
            "cancel to exit: ")
        if command == 'white':
            rgb_led.white()
            callback("WHITE", "RGB_LED_WHITE", settings, publish_event)
        elif command == 'red':
            rgb_led.red()
            callback("RED", "RGB_LED_RED", settings, publish_event)
        elif command == 'green':
            rgb_led.green()
            callback("GREEN", "RGB_LED_GREEN", settings, publish_event)
        elif command == 'blue':
            rgb_led.blue()
            callback("BLUE", "RGB_LED_BLUE", settings, publish_event)
        elif command == 'yellow':
            rgb_led.yellow()
            callback("YELLOW", "RGB_LED_YELLOW", settings, publish_event)
        elif command == 'purple':
            rgb_led.purple()
            callback("PURPLE", "RGB_LED_PURPLE", settings, publish_event)
        elif command == 'light_blue':
            rgb_led.lightBlue()
            callback("BLUE", "RGB_LED_LIGHT_BLUE", settings, publish_event)
        elif command == 'off':
            rgb_led.turnOff()
            callback("OFF", "RGB_LED_OFF", settings, publish_event)
        if stop_event.is_set():
            break
        time.sleep(delay)
