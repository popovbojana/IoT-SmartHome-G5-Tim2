from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Dht:
    def __init__(self, timestamp, pi, name, simulated, humidity, temperature):
        self.timestamp = timestamp
        self.pi = pi
        self.name = name
        self.simulated = simulated
        self.humidity = humidity
        self.temperature = temperature

    def save_to_influxdb(self, client):
        point = Point("dht_data").time(int(self.timestamp), WritePrecision.S)
        point.field("pi", self.pi)
        point.field("name", self.name)
        point.field("simulated", self.simulated)
        point.field("humidity", self.humidity)
        point.field("temperature", self.temperature)

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket="iot", org="nwt", record=point)
