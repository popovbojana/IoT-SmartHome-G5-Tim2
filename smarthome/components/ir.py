import threading
import time
from settings.settings import print_lock2, load_mqtt_config
import paho.mqtt.publish as mqtt_publish
import json


mqtt_config = load_mqtt_config()
ir_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, ir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ir_batch = ir_batch.copy()
            publish_data_counter = 0
            ir_batch.clear()
        mqtt_publish.multiple(local_ir_batch, hostname=mqtt_config['host'], port=mqtt_config['port'],
                              auth={"username": mqtt_config['username'], "password": mqtt_config['password']})
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def ir_callback(button, code, settings, publish_event):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    print()
    print("*" * 5 + settings['name'] + "*" * 5)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    print(f"Code: {code}")
    print(f"Button: {button.upper()}")

    message = {
        "pi": settings['pi'],
        "name": settings['name'],
        "simulated": settings['simulated'],
        "timestamp": time.time(),
        "button": button.upper(),
    }

    with counter_lock:
        ir_batch.append(('ir', json.dumps(message), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_ir(settings, threads, stop_event, button):
    if settings['simulated']:
        ir_thread = threading.Thread(target=ir_callback, args=(button, "IR_BUTTON_" + button.upper(), settings, publish_event))
        ir_thread.start()
        threads.append(ir_thread)
    else:
        from actuators.ir import run_ir_loop, IR
        ir = IR(settings['name'], settings['pin'])
        ir_thread = threading.Thread(target=run_ir_loop, args=(ir, 2, ir_callback, stop_event, settings,
                                                                    publish_event))
        ir_thread.start()
        threads.append(ir_thread)
