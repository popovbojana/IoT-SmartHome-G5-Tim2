import time

num = {' ': (0, 0, 0, 0, 0, 0, 0),
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


# def generate_values():
#     binary = []
#     while True:
#         a = time.ctime()[11:13] + time.ctime()[14:16]
#         s = str(a).rjust(4)
#
#         for digit in range(4):
#             b = ""
#             for loop in range(0, 7):
#                 n = num[s[digit]][loop]
#                 b = b + str(n)
#             binary.append(b)
#
#         yield a, binary
#         binary = []
#
#
# def run_fdss_simulator(delay, callback, stop_event, settings, publish_event):
#     for a, b in generate_values():
#         time.sleep(delay)
#         callback(a, b, "FDSS_OK", settings, publish_event)
#         if stop_event.is_set():
#             break


def generate_values():
    a = time.ctime()[11:13] + time.ctime()[14:16]


def run_fdss_simulator(delay, callback, stop_event, settings, publish_event, alarm_clock_event):
    while True:
        a = time.ctime()[11:13] + time.ctime()[14:16]
        callback(a, "a", "FDSS_ON", settings, publish_event)

        if alarm_clock_event.is_set():
            while alarm_clock_event.is_set():
                a = time.ctime()[11:13] + time.ctime()[14:16]
                callback(a, "a", "FDSS_ON", settings, publish_event)
                print("FDSS_ON")
                time.sleep(5)
                a = time.ctime()[11:13] + time.ctime()[14:16]
                callback(a, "a", "FDSS_OFF", settings, publish_event)
                print("FDSS_OFF")
                time.sleep(5)
        if stop_event.is_set():
            break