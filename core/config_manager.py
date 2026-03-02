import json
import os
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG = {
    "template_files": [],
    "excel_output": "placeholders.xlsx",
    "data_file": "",
    "output_dir": "output",
    "folder_column": "ID",
    "filename_pattern": "{ID}_{template_name}",
    "theme": "dark",
    "multiprocessing": True,
    "num_workers": 4,
    "pdf_gen": False,
    "zip_gen": False
}

class ConfigManager:
    def __init__(self, config_path: str = "app_config.json"):
        self.config_path = config_path
        self.config = self.load()

    def load(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()

    def save(self):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save()
