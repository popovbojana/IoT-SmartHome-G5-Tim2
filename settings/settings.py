import json


def load_settings_pi1(filePath='settings/settings_pi1.json'):
    with open(filePath, 'r') as f:
        return json.load(f)
