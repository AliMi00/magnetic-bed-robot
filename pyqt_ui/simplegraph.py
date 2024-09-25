import sys
import numpy as np
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel
)
from PyQt6.QtCore import QTimer
import pyqtgraph as pg

os.environ["QT_QPA_PLATFORM"] = "xcb"

class SensorDataUI(QWidget):
    def __init__(self, update_interval=1000):
        super().__init__()

        # Layout setup
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # PyQtGraph settings for real-time updates
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        # Create sensor graphs and labels
        self.graphs = []
        self.lines = []
        self.data_buffers = []

        self.num_sensors = 3  # Three graphs for three sensors
        self.num_lines_per_sensor = 2  # Two lines per graph (each sensor)
        self.data_buffer_size = 100  # Buffer size for the graph (rolling window)

        # Add graphs to the layout in a 2x2 grid
        for i in range(self.num_sensors):
            graph_widget = pg.PlotWidget()
            graph_widget.setYRange(-10, 10)  # Adjust based on sensor range
            self.graphs.append(graph_widget)

            sensor_lines = []
            sensor_data_buffers = []

            # Add multiple lines per sensor graph
            for j in range(self.num_lines_per_sensor):
                line = graph_widget.plot(pen=pg.mkPen(color=(j * 85, 255 - j * 85, 150), width=2))
                sensor_lines.append(line)

                # Initialize data buffers for each line
                sensor_data_buffers.append(np.zeros(self.data_buffer_size))

            self.lines.append(sensor_lines)
            self.data_buffers.append(sensor_data_buffers)

            # Add graph to the grid layout (row-major order)
            row, col = divmod(i, 2)
            self.layout.addWidget(graph_widget, row, col)

        # Add a data reading box in the fourth position (bottom-right)
        self.data_label_box = QLabel("Sensor Data Reading: ")
        self.layout.addWidget(self.data_label_box, 1, 1)

        # Create a timer for real-time updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(update_interval)

    def update_data(self):
        sensor_data_readout = "Sensor Data:\n"
        for i in range(self.num_sensors):
            for j in range(self.num_lines_per_sensor):
                # Simulating new sensor data (replace this with actual sensor data fetching)
                new_data = np.random.normal(0, 1)
                self.data_buffers[i][j] = np.roll(self.data_buffers[i][j], -1)
                self.data_buffers[i][j][-1] = new_data

                # Update the line graph
                self.lines[i][j].setData(self.data_buffers[i][j])

                # Update the sensor data readout
                sensor_data_readout += f"Sensor {i+1}, Line {j+1}: {new_data:.2f}\n"

        # Update the data reading box
        self.data_label_box.setText(sensor_data_readout)

# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SensorDataUI(update_interval=1000)  # Update interval set to 1 second
    window.setWindowTitle("Real-Time Sensor Data with Multiple Lines")
    window.show()
    sys.exit(app.exec())
