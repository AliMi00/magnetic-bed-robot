# core/data_simulator.py

import time
import threading
import pandas as pd
from PyQt6.QtCore import QObject, pyqtSignal

class DataSimulator(QObject):
    data_updated = pyqtSignal(dict)

    def __init__(self, file_path=None, parent=None):
        super().__init__(parent)
        self.running = False
        self.file_path = file_path
        self.data = pd.read_csv('config/HBsteel-M22-F.csv')  # Load the data from the file
        self.index = 0  # Start reading from the first row

    def start(self):
        """Start the data simulation in a separate thread."""
        self.running = True
        self.data = pd.read_csv('config/HBsteel-M22-F.csv')  # Reload the data
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        """Stop the data simulation."""
        self.running = False
        self.index = 0
        

    def run(self):
        """Simulate sensor data updates by reading from the CSV file."""
        while self.running and self.index < len(self.data):
            # Extract data from the current row
            row = self.data.iloc[self.index]
            data = {
                'Force_x': row["Force_M1.Force_x [newton]"],
                'Force_y': row["Force_M1.Force_y [newton]"],
                'Force_z': row["Force_M1.Force_z [newton]"],
                'Distance': row["$dist_1 [mm]"]
            }
            self.data_updated.emit(data)
            self.index += 1  # Move to the next row
            time.sleep(0.1)  # Update every second
