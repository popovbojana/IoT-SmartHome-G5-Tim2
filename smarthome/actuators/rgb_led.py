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


def run_rgb_loop(command, rgb_led, delay, callback, stop_event, settings, publish_event):
# def run_rgb_loop(command, rgb_led, delay, callback, stop_event, settings, publish_event,
#                  state_off_event, state_white_event, state_red_event, state_green_event, state_blue_event, state_yellow_event, state_purple_event, state_lightblue_event):
#     while True:
#         if state_off_event.is_set():
#             rgb_led.turnOff()
#             callback("OFF", "RGB_LED_OFF", settings, publish_event)
#
#         elif state_white_event.is_set():
#             rgb_led.white()
#             callback("WHITE", "RGB_LED_WHITE", settings, publish_event)
#
#         elif state_red_event.is_set():
#             rgb_led.red()
#             callback("RED", "RGB_LED_RED", settings, publish_event)
#
#         elif state_green_event.is_set():
#             rgb_led.green()
#             callback("GREEN", "RGB_LED_GREEN", settings, publish_event)
#
#         elif state_blue_event.is_set():
#             rgb_led.blue()
#             callback("BLUE", "RGB_LED_BLUE", settings, publish_event)
#
#         elif state_yellow_event.is_set():
#             rgb_led.yellow()
#             callback("YELLOW", "RGB_LED_YELLOW", settings, publish_event)
#
#         elif state_purple_event.is_set():
#             rgb_led.purple()
#             callback("PURPLE", "RGB_LED_PURPLE", settings, publish_event)
#
#         elif state_lightblue_event.is_set():
#             rgb_led.lightBlue()
#             callback("LIGHT_BLUE", "RGB_LED_LIGHT_BLUE", settings, publish_event)

    while True:
        if command == 'WHITE':
            rgb_led.white()
            callback("WHITE", "RGB_LED_WHITE", settings, publish_event)

        elif command == 'RED':
            rgb_led.red()
            callback("RED", "RGB_LED_RED", settings, publish_event)

        elif command == 'GREEN':
            rgb_led.green()
            callback("GREEN", "RGB_LED_GREEN", settings, publish_event)

        elif command == 'BLUE':
            rgb_led.blue()
            callback("BLUE", "RGB_LED_BLUE", settings, publish_event)

        elif command == 'YELLOW':
            rgb_led.yellow()
            callback("YELLOW", "RGB_LED_YELLOW", settings, publish_event)

        elif command == 'PURPLE':
            rgb_led.purple()
            callback("PURPLE", "RGB_LED_PURPLE", settings, publish_event)

        elif command == 'BLUE':
            rgb_led.lightBlue()
            callback("BLUE", "RGB_LED_LIGHT_BLUE", settings, publish_event)

        elif command == 'OFF':
            rgb_led.turnOff()
            callback("OFF", "RGB_LED_OFF", settings, publish_event)
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)
