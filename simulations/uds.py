import time
import random


# def generate_values(initial_distance=100):
#     distance = initial_distance
#     TRIG_PIN = False
#     ECHO_PIN = False
#
#     while True:
#         if not TRIG_PIN:
#             TRIG_PIN = True
#             ECHO_PIN = False
#             distance += random.uniform(-5, 5)  # Adjust the range here
#             if distance < 0:
#                 distance = 0
#             if distance > 100:
#                 distance = 100
#
#         if TRIG_PIN and not ECHO_PIN:
#             ECHO_PIN = True
#
#         if TRIG_PIN and ECHO_PIN:
#             TRIG_PIN = False
#             ECHO_PIN = False
#
#         yield distance

def generate_values(initial_distance=100):
    distance = initial_distance
    TRIG_PIN = False
    ECHO_PIN = False
    decreasing = True

    while True:
        if not TRIG_PIN:
            TRIG_PIN = True
            ECHO_PIN = False

            if decreasing:
                distance -= random.uniform(5, 15)
            else:
                distance += random.uniform(5, 15)

            if distance <= 0:
                decreasing = False
                distance = 0
            if distance >= 100:
                decreasing = True
                distance = 100

        if TRIG_PIN and not ECHO_PIN:
            ECHO_PIN = True

        if TRIG_PIN and ECHO_PIN:
            TRIG_PIN = False
            ECHO_PIN = False

        yield distance

def run_uds_simulator(delay, callback, stop_event, name):
    for d in generate_values():
        time.sleep(delay)
        callback(d, "UDSLIB_OK", name)
        if stop_event.is_set():
            break