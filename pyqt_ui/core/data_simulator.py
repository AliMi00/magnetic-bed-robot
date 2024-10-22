# core/data_simulator.py

import random
import time
import threading
from PyQt6.QtCore import QObject, pyqtSignal

class DataSimulator(QObject):
    data_updated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = False

    def start(self):
        """Start the data simulation in a separate thread."""
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        """Stop the data simulation."""
        self.running = False

    def run(self):
        """Simulate sensor data updates."""
        while self.running:
            # Simulate some sensor data
            data = {
                'Force': random.uniform(1.0, 30.0),
                'Torque': random.uniform(0.1, 20.0)
            }
            self.data_updated.emit(data)
            time.sleep(1)  # Update every second
