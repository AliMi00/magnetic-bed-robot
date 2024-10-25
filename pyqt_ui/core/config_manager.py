# core/config_manager.py

import json
import os
from PyQt6.QtWidgets import QMessageBox

class ConfigManager:
    def __init__(self, config_file='config/config.json'):
        self.config_file = config_file
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load and parse the configuration file."""
        if not os.path.exists(self.config_file):
            QMessageBox.critical(None, "Configuration Error",
                                 f"Configuration file {self.config_file} not found.")
            sys.exit(1)
        try:
            with open(self.config_file, 'r') as file:
                self.config = json.load(file)
        except json.JSONDecodeError as e:
            QMessageBox.critical(None, "Configuration Error",
                                 f"Error parsing the configuration file: {e}")
            sys.exit(1)

    def get(self, *keys, default=None):
        """Retrieve a configuration value with nested keys."""
        data = self.config
        for key in keys:
            if key in data:
                data = data[key]
            else:
                return default
        return data
