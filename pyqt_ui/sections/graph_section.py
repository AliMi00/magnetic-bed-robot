# sections/graph_section.py

import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel
from PyQt6.QtCore import Qt
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import pandas as pd
import yaml

class GraphSection(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.num_axes = self.load_axes("config/param_set_axes.yaml")
        self.init_ui()

    def load_axes(self, filename):
        """Load the number of axes to plot from .yaml file"""
        with open(filename, "r") as file:
            data = yaml.safe_load(file)
            num_axes = data.get('axes', 3)  # Default to 3 if  not specified
            if num_axes not in [2, 3]:
                raise ValueError("Axes value must be either 2 or 3.")
            return num_axes


    def init_ui(self):
        """Initialize the Graph Data Section."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Drop-down to select data type
        self.data_selector = QComboBox()
        self.data_selector.addItems(['Force', 'Torque'])
        self.data_selector.currentIndexChanged.connect(self.change_graph)
        layout.addWidget(self.data_selector)

        # Load the CSV data
        self.data = pd.read_csv("config/HBsteel-M22-F.csv")

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)

        # Plot the data initially
        self.change_graph(0)

    def change_graph(self, index):
        """Change the graph based on selected data type."""
        self.ax.clear()

        if self.data_selector.currentText().lower() == 'force':
            distance = self.data['$dist_1 [mm]']
            force_x = self.data['Force_M1.Force_x [newton]']
            force_y = self.data['Force_M1.Force_y [newton]']
            force_z = self.data['Force_M1.Force_z [newton]']

            # Plot data based on the number of axes data
            if self.num_axes == 2:
               self.ax.plot(distance, force_x, label='Force_x', color='r')
               self.ax.plot(distance, force_y, label='Force_y', color='g')
            elif self.num_axes == 3:
               self.ax.plot(distance, force_x, label='Force_x', color='r')
               self.ax.plot(distance, force_y, label='Force_y', color='g')
               self.ax.plot(distance, force_z, label='Force_z', color='b')

            # Add labels, title, and legend
            self.ax.set_xlabel('Distance to steel plate [mm]')
            self.ax.set_ylabel('Interaction Force [newton]')
            self.ax.set_title('Force Plot')
            self.ax.legend()
        #Refresh the canvas to display the new graph
        self.canvas.draw()



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

    # def on_mouse_click(self, event):
    #     """Handle mouse click events on the graph."""
    #     # Check if click was on an axis (i.e., data point)
    #     if event.xdata and event.ydata:
    #         # Find the closest data point to where the user clicked
    #         x_val = event.xdata
    #         distance = self.data['$dist_1 [mm]']
    #         index = (distance - x_val).abs().idxmin()  # Find index of closest x value
    #         closest_x = distance.iloc[index]
    #         force_x = self.data['Force_M1.Force_x [newton]'].iloc[index]
    #         force_y = self.data['Force_M1.Force_y [newton]'].iloc[index]
    #         force_z = self.data['Force_M1.Force_z [newton]'].iloc[index]

