# config.py
import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file='app_config.json'):
        self.portable = Path('portable.txt').exists()
        if self.portable:
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            self.config_file = data_dir / config_file
        else:
            self.config_file = config_file
        self.data = self.load()

    def load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

config = ConfigManager()