import time


def run_diode_simulator(delay, callback, stop_event, settings, publish_event):
    time.sleep(int(delay))
    callback(None, "DIODE_OK", settings, publish_event)
