from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout, QPushButton
)
from PySide6.QtCore import Qt
from scenario_base import ScenarioBase

class Scenario2(ScenarioBase):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
         # Main layout using QGridLayout for precise positioning
        main_layout = QGridLayout(self)

        # Remove layout margins and spacing for precise control
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side: Container for 3D simulation (placed in the top-left corner)
        self.simulation_container = QWidget()
        self.simulation_container.setStyleSheet("background-color: lightgray;")
        self.simulation_container.setFixedSize(650, 650)

        # Place the simulation container in the top-left corner (row 0, column 0)
        main_layout.addWidget(self.simulation_container, 0, 0)

        # Right side: Information and controls (placed in row 0, column 1)
        label = QLabel("Scenario 2: Magnet Placement Technique 2")
        label.setStyleSheet("background-color: lightblue;")  # Set background color to see the layout effect
        label.setMinimumWidth(200)  # Ensure the label does not shrink too much
        main_layout.addWidget(label, 0, 1)

        # Add stretch to force right-side elements to adjust correctly
        main_layout.setColumnStretch(0, 0)  # No stretch on the left column
        main_layout.setColumnStretch(1, 1)  # Stretch on the right column to expand
        main_layout.setRowStretch(0, 1)  # Ensure the row expands vertically as needed


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