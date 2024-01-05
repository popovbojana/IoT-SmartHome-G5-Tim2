import json
import threading


def load_settings(filePath='settings/settings_pi1.json'):
    with open(filePath, 'r') as f:
        return json.load(f)


def load_mqtt_config(filePath='settings/mqtt_configuration.json'):
    with open(filePath, 'r') as f:
        return json.load(f)


print_lock = threading.Lock()
print_lock2 = threading.Lock()
print_lock3 = threading.Lock()
