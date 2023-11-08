import json


def load_settings_pi1(filePath='C:/Users/filip/Documents/GitHub/IoT-SmartHome-G5-Tim2/settings/settings_pi1.json'):
    with open(filePath, 'r') as f:
        return json.load(f)
