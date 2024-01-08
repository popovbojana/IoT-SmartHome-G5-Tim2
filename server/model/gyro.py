from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Gyro:
    def __init__(self, timestamp, pi, name, simulated, rotation, acceleration):
        self.timestamp = timestamp
        self.pi = pi
        self.name = name
        self.simulated = simulated
        self.rotation = rotation
        self.acceleration = acceleration

    def save_to_influxdb(self, client):
        point = Point("gyro_data").time(int(self.timestamp), WritePrecision.S)
        point.tag("pi", self.pi)
        point.tag("name", self.name)
        point.tag("simulated", self.simulated)
        point.field("rotation", self.rotation)
        point.field("acceleration", self.acceleration)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket="iot", org="nwt", record=point)
