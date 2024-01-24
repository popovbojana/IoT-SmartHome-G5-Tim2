from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from settings.influx_settings import ORG, BUCKET


def save_uds_data(payload, client):
    point = Point("uds_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.field("distance", payload["distance"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_button_data(payload, client):
    point = Point("button_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.tag("code", payload["code"])
    point.field("door_unlocked", payload["door_unlocked"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_buzzer_data(payload, client):
    point = Point("buzzer_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.tag("pitch", payload["pitch"])
    point.field("duration", payload["duration"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_dht_data(payload, client):
    point = Point("dht_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.field("humidity", payload["humidity"])
    point.field("temperature", payload["temperature"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_diode_data(payload, client):
    point = Point("diode_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.field("light_state", payload["light_state"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_dms_data(payload, client):
    point = Point("dms_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.field("key", payload["key"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_pir_data(payload, client):
    point = Point("pir_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.field("motion_detected", payload["motion_detected"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_gyro_data(payload, client):
    point = Point("gyro_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.field("rotation", payload["rotation"])
    point.field("acceleration", payload["acceleration"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_lcd_data(payload, client):
    point = Point("lcd_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.field("display", payload["display"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_rgb_data(payload, client):
    point = Point("rgb_led_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.field("state", payload["state"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_fdss_data(payload, client):
    point = Point("fdss_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    # point.tag("code", payload["code"])
    point.field("alarm_time", payload["alarm_time"])

    print("UPISAO")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_ir_data(payload, client):
    point = Point("ir_data").time(int(payload["timestamp"]), WritePrecision.S)
    point.tag("pi", payload["pi"])
    point.tag("name", payload["name"])
    point.tag("simulated", payload["simulated"])
    point.field("button", payload["button"])

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_alarm_data(state, timestamp, client):
    point = Point("alarm_data").time(int(timestamp), WritePrecision.S)
    point.field("on", state)

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)


def save_people_data(number, timestamp, client):
    point = Point("people_data").time(int(timestamp), WritePrecision.S)
    point.field("inside", number)

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=BUCKET, org=ORG, record=point)
