from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Buzzer:
    def __init__(self, timestamp, pi, name, simulated, pitch, duration):
        self.timestamp = timestamp
        self.pi = pi
        self.name = name
        self.simulated = simulated
        self.pitch = pitch
        self.duration = duration

    def save_to_influxdb(self, client):
        point = Point("buzzer_data").time(int(self.timestamp), WritePrecision.S)
        point.tag("pi", self.pi)
        point.tag("name", self.name)
        point.tag("simulated", self.simulated)
        point.tag("pitch", self.pitch)
        point.field("duration", self.duration)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket="iot", org="nwt", record=point)
