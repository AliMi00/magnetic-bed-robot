from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton
)
from PySide6.QtCore import Qt
from scenario_base import ScenarioBase

import pyqtgraph as pg

class Scenario1(ScenarioBase):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
         # Main layout using QGridLayout for precise positioning
        main_layout = QGridLayout(self)

        # Remove layout margins and spacing for precise control
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)


        ### Left container 3D simulation
        # create a vertical layout to hold the 3D simulation title
        self.simulation_layout = QVBoxLayout()
        self.simulation_layout.setSpacing(0)

        # 3D simulation container title
        simulation_label = QLabel("3D simulation placing technique")
        simulation_label.setAlignment(Qt.AlignCenter)
        simulation_label.setStyleSheet("font-size: 16px; font-weight: bold; padding-bottom: 0px;")
        self.simulation_layout.addWidget(simulation_label)

        # Left side: Container for 3D simulation (placed in the top-left corner)
        self.simulation_container = QWidget()
        self.simulation_container.setStyleSheet("background-color: lightgray;")
        self.simulation_container.setFixedSize(650, 650)

        # Add the 3D simulation container to the layout (below the title)
        self.simulation_layout.addWidget(self.simulation_container)

        # Place the simulation container in the top-left corner (row 0, column 0)
        main_layout.addLayout(self.simulation_layout, 0, 0)

        ### Middle container for Real-time Force data ###
        self.force_container = QWidget()
        self.force_layout = QVBoxLayout(self.force_container)
        self.force_layout.setSpacing(0)

        # Title for Force Graph
        force_label = QLabel("Real-Time Force Data")
        force_label.setAlignment(Qt.AlignCenter)
        force_label.setStyleSheet("font-size: 16px; font-weight: bold; padding-bottom: 10px;")
        self.force_layout.addWidget(force_label)

        # PyQtGraph plot for Force data
        self.force_graph = pg.PlotWidget()
        self.force_graph.setBackground('w')  # Set background to white
        self.force_graph.setLabel('left', 'Force (N)')
        self.force_graph.setLabel('bottom', 'Time (s)')
        self.force_graph.addLegend()

        # sample static data for Force
        force_time = [ 0, 1, 2, 3 ,4 , 5]
        force_values = [ 0, 2, 4, 3, 5, 6]

        self.force_plot = self.force_graph.plot(force_time, force_values, pen=pg.mkPen(color="b", width=2), name="Force Data")
        self.force_layout.addWidget(self.force_graph)

        # Add the force container to the main layout 
        main_layout.addWidget(self.force_container, 0, 1)

        ### Right: Container for Real-Time Torque Data ###
        self.torque_container = QWidget()
        self.torque_layout = QVBoxLayout(self.torque_container)
        self.torque_layout.setSpacing(0)


        # Title for Torque Data
        torque_label = QLabel("Real-Time Torque Data")
        torque_label.setAlignment(Qt.AlignCenter)
        torque_label.setStyleSheet("font-size: 16px; font-weight: bold; padding-bottom: 10px;")
        self.torque_layout.addWidget(torque_label)

        # PyQtGraph plot for Torque data
        self.torque_graph = pg.PlotWidget()
        self.torque_graph.setBackground('w')  # Set background to white
        self.torque_graph.setLabel('left', 'Torque (Nm)')
        self.torque_graph.setLabel('bottom', 'Time (s)')
        self.torque_graph.addLegend()

        # Sample static data for Torque
        torque_time = [0, 1, 2, 3, 4, 5]
        torque_values = [0, 1, 2, 1, 3, 4]

        self.torque_plot = self.torque_graph.plot(torque_time, torque_values, pen=pg.mkPen(color="r", width=2), name="Torque Data")
        self.torque_layout.addWidget(self.torque_graph)

        # Add the torque container to the main layout beside the force container
        main_layout.addWidget(self.torque_container, 0, 2)

        # Add stretch to force elements to adjust correctly
        main_layout.setColumnStretch(0, 1)  # Allow the simulation container to stretch
        main_layout.setColumnStretch(1, 1)  # Allow the force container to stretch
        main_layout.setColumnStretch(2, 1)  # Allow the torque container to stretch
        main_layout.setColumnStretch(0, 0)  # No stretch on the left column



        #Bottom right container for robotic arm controls (QGridLayout)
        self.control_container = QWidget()
        control_layout = QVBoxLayout(self.control_container)
        

         # Title/label for the control buttons
        title_label = QLabel("Buttons to Move the Robotic Arm")
        title_label.setAlignment(Qt.AlignCenter)  # Center the title label
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; padding-bottom: 10px;")

        control_layout.addWidget(title_label)

        button_grid = QGridLayout()

           # X-axis control buttons
        x_positive_button = QPushButton("→")
        x_negative_button = QPushButton("←")

        # Y-axis control buttons
        y_positive_button = QPushButton("↑")
        y_negative_button = QPushButton("↓")

        # Z-axis control buttons
        z_up_button = QPushButton("Z+")
        z_down_button = QPushButton("Z-")

        # Styling buttons for visibility and user-friendliness
        buttons = [x_positive_button, x_negative_button, y_positive_button, y_negative_button, z_up_button, z_down_button]

        for button in buttons:
             button.setFixedSize(50, 50)  # Set a fixed size for all buttons
             button.setStyleSheet("font-size: 20px;")  # Increase font size for visibility

         # Place buttons in a grid layout
        button_grid.addWidget(x_negative_button, 1, 0)  # X-
        button_grid.addWidget(x_positive_button, 1, 2)  # X+
        button_grid.addWidget(y_positive_button, 0, 1)  # Y+
        button_grid.addWidget(y_negative_button, 2, 1)  # Y-
        button_grid.addWidget(z_up_button, 0, 3)        # Z+
        button_grid.addWidget(z_down_button, 2, 3)      # Z-


        control_layout.addLayout(button_grid)

         # Add the control container to the main layout in the bottom-right corner
        main_layout.addWidget(self.control_container, 1, 1, alignment=Qt.AlignBottom | Qt.AlignRight)
