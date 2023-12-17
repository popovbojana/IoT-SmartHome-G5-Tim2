from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Diode:
    def __init__(self, timestamp, pi, name, simulated, light_on):
        self.timestamp = timestamp
        self.pi = pi
        self.name = name
        self.simulated = simulated
        self.light_on = light_on

    def save_to_influxdb(self, client):
        point = Point("diode_data").time(int(self.timestamp), WritePrecision.S)
        point.field("pi", self.pi)
        point.field("name", self.name)
        point.field("simulated", self.simulated)
        point.field("light_on", self.light_on)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket="iot", org="nwt", record=point)
