from simulations.lcd import run_lcd_simulator
import threading
import time
import paho.mqtt.publish as mqtt_publish
import json
from settings.broker_settings import HOST, PORT

lcd_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, lcd_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_lcd_batch = lcd_batch.copy()
            publish_data_counter = 0
            lcd_batch.clear()
        mqtt_publish.multiple(local_lcd_batch, hostname=HOST, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, lcd_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def lcd_callback(display, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    # t = time.localtime()
    # print()
    # print("*" * 5 + settings['name'] + "*" * 5)
    # print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    # print(f"Code: {code}")
    # print(f"Display: {display}")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "display": display
    }

    with counter_lock:
        lcd_batch.append(('lcd', json.dumps(message), 0, False))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_lcd(settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {settings['name']} simulator")
        lcd_thread = threading.Thread(target=run_lcd_simulator, args=(2, lcd_callback, stop_event, settings,
                                                                      publish_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"{settings['name']} simulator started")
    else:
        from displays.lcd.Adafruit_LCD1602 import run_lcd_loop, Adafruit_CharLCD
        print(f"Starting {settings['name']} loop")
        lcd = Adafruit_CharLCD(settings['name'], settings['pin_rs'], settings['pin_e'], settings['pins_db'])
        lcd_thread = threading.Thread(target=run_lcd_loop, args=(lcd, 2, lcd_callback, stop_event, settings,
                                                                 publish_event))
        lcd_thread.start()
        threads.append(lcd_thread)
        print(f"{settings['name']} loop started")
