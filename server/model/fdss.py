from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Fdss:
    def __init__(self, timestamp, pi, name, simulated, alarm_time):
        self.timestamp = timestamp
        self.pi = pi
        self.name = name
        self.simulated = simulated
        self.alarm_time = alarm_time

    def save_to_influxdb(self, client):
        point = Point("fdss_data").time(int(self.timestamp), WritePrecision.S)
        point.tag("pi", self.pi)
        point.tag("name", self.name)
        point.tag("simulated", self.simulated)
        point.field("alarm_time", self.alarm_time)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket="iot", org="nwt", record=point)
