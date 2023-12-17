from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from influxdb_client import Point, WritePrecision

class Uds:
    def __init__(self, timestamp, pi, name, simulated, distance):
        self.timestamp = timestamp
        self.pi = pi
        self.name = name
        self.simulated = simulated
        self.distance = distance

    def save_to_influxdb(self):

        # Konvertujte timestamp u sekunde (int)
        timestamp_seconds = int(self.timestamp)

        point = Point(self.name).time(timestamp_seconds, WritePrecision.S)
        point.field("pi", self.pi)
        point.field("name", self.name)
        point.field("simulated", self.simulated)
        point.field("distance", float(self.distance))

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket="iot", org="nwt", record=point)


# Konfiguracija InfluxDB klijenta
config = {
    "influxdb": {
        "host": "localhost",
        "port": 8086,
        "organization": "nwt",
        "bucket": "measurements",
        "token": "Y_NxGg8VlXocoZDLP7Z0UiXnWI-eHr8dNbcbRWK3PvPlfwXlPHkmWEuY5CFbvMrMLZ2lq8Juv98w-TNRY6BqaA=="
    }
}

influxdb_config = config.get("influxdb", {})

# Klijent za InfluxDB
client = InfluxDBClient(url=f"http://{influxdb_config['host']}:{influxdb_config['port']}", token=influxdb_config['token'], org=influxdb_config['organization'])