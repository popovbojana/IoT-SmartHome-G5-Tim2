import json
import threading


def load_mqtt_config(filePath='settings/mqtt_configuration.json'):
    with open(filePath, 'r') as f:
        return json.load(f)
