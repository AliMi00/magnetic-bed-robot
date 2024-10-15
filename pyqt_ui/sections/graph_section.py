# sections/graph_section.py

import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PyQt6.QtCore import Qt
import time

class GraphSection(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.init_ui()

    def init_ui(self):
        """Initialize the Graph Data Section."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Graph Data")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        # Drop-down to select data type
        self.data_selector = QComboBox()
        self.data_selector.addItems(['Temperature', 'Pressure', 'Humidity', 'Vibration'])
        self.data_selector.currentIndexChanged.connect(self.change_graph)
        layout.addWidget(self.data_selector)

        # PyQtGraph Plot Widget
        self.plot_widget = pg.PlotWidget()
        self.plot = self.plot_widget.plot([], [])
        layout.addWidget(self.plot_widget)

        # Data storage
        self.x = []
        self.y = []
        self.max_points = 100
        self.current_data = self.data_selector.currentText().lower()

    def change_graph(self, index):
        """Change the graph based on selected data type."""
        self.current_data = self.data_selector.currentText().lower()
        self.x = []
        self.y = []
        self.plot.clear()
        self.plot = self.plot_widget.plot([], [])

    def update_graph_data(self, data):
        """Update the graph with new data."""
        self.x.append(time.time())
        self.y.append(data.get(self.current_data, 0))
        if len(self.x) > self.max_points:
            self.x = self.x[-self.max_points:]
            self.y = self.y[-self.max_points:]
        # Convert timestamps to relative time for better visualization
        relative_x = [x - self.x[0] for x in self.x]
        self.plot.setData(relative_x, self.y)
        self.plot_widget.setLabel('left', self.current_data.capitalize())
        self.plot_widget.setLabel('bottom', 'Time', units='s')
