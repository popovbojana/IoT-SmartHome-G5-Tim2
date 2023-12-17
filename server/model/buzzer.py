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
        point.field("pi", self.pi)
        point.field("name", self.name)
        point.field("simulated", self.simulated)
        point.field("pitch", self.pitch)
        point.field("duration", self.duration)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket="iot", org="nwt", record=point)
