# sections/motor_control_section.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QSlider, QLabel, QMessageBox, QPushButton, QComboBox, QStackedWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtGui import QFont
import yaml
import re
from core.motor_controller import MotorController


class MotorControlSection(QWidget):

    next_video = pyqtSignal()
    previous_video = pyqtSignal()
    

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.motor_torque_mapping = self.load_motor_mapping("config/param_motors_control.yaml")
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


    def load_motor_mapping(self, filename):
        """Load motor mapping from a .yaml file"""
        with open(filename, "r") as file:
            return yaml.safe_load(file)

    def parse_torque_value(self, value):
        """Parse the torque value and return numeric value and unit"""
        match = re.match(r"(\d+(?:\.\d+)?)\s*(N.*)", value)
        if not match:
            raise ValueError(f"Invalid torque value format: {value}. Torque unit must start with 'N' as newton meter unit.")
        numeric_value = float(match.group(1))
        unit = match.group(2)

        return numeric_value, unit

    def init_ui(self):
        """Initialize the Motor Control Section."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Control Panel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 18px; padding-bottom: 10px;")
        layout.addWidget(title)

        # Combo Box to switch between Robotic Arm and Motor Torque Control
        self.control_selector = QComboBox()
        self.control_selector.addItems(['Robotic Arm Control', 'Motor Torque Control'])
        self.control_selector.currentIndexChanged.connect(self.change_control_mode)
        layout.addWidget(self.control_selector)

        # Stacked Widget to hold both control UIs
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Initialize both UI sections
        self.init_robotic_arm_control_ui()
        self.init_motor_torque_control_ui()

        # Add sections to the stacked widget
        self.stacked_widget.addWidget(self.robotic_arm_control_widget)
        self.stacked_widget.addWidget(self.motor_torque_control_widget)

        # Set default to Robotic Arm Control
        self.stacked_widget.setCurrentIndex(0)

    def init_robotic_arm_control_ui(self):
        """Initialize the UI for Robotic Arm Control."""
        self.robotic_arm_control_widget = QWidget()
        arm_layout = QVBoxLayout(self.robotic_arm_control_widget)

        # Create movement buttons with styling
        button_font = QFont('Arial', 12, QFont.Weight.Bold)

        # Up Button (↑)
        self.up_button = QPushButton("↑")
        self.up_button.setFont(button_font)
        self.up_button.setStyleSheet(self.get_arrow_button_style())
        arm_layout.addWidget(self.up_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Left, Right, and Down buttons in an HBox
        left_right_layout = QHBoxLayout()
        
        # Left Button (←)
        self.left_button = QPushButton("←")
        self.left_button.setFont(button_font)
        self.left_button.setStyleSheet(self.get_arrow_button_style())
        left_right_layout.addWidget(self.left_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.left_button.clicked.connect(self.on_left_button_clicked)

        # Right Button (→)
        self.right_button = QPushButton("→")
        self.right_button.setFont(button_font)
        self.right_button.setStyleSheet(self.get_arrow_button_style())
        left_right_layout.addWidget(self.right_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.right_button.clicked.connect(self.on_right_button_clicked)



        arm_layout.addLayout(left_right_layout)

        # Down Button (↓)
        self.down_button = QPushButton("↓")
        self.down_button.setFont(button_font)
        self.down_button.setStyleSheet(self.get_arrow_button_style())
        arm_layout.addWidget(self.down_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Check if there are 3 axes, and add Z+ and Z- buttons if so
        if self.num_axes == 3:
            z_button_layout = QHBoxLayout()
            
            # Z+ Button (Z+)
            self.z_plus_button = QPushButton("Z+")
            self.z_plus_button.setFont(button_font)
            self.z_plus_button.setStyleSheet(self.get_arrow_button_style())
            z_button_layout.addWidget(self.z_plus_button, alignment=Qt.AlignmentFlag.AlignCenter)

            # Z- Button (Z-)
            self.z_minus_button = QPushButton("Z-")
            self.z_minus_button.setFont(button_font)
            self.z_minus_button.setStyleSheet(self.get_arrow_button_style())
            z_button_layout.addWidget(self.z_minus_button, alignment=Qt.AlignmentFlag.AlignCenter)

            arm_layout.addLayout(z_button_layout)

    def init_motor_torque_control_ui(self):
        """Initialize the UI for Motor Torque Control."""
        self.motor_torque_control_widget = QWidget()
        motor_layout = QVBoxLayout(self.motor_torque_control_widget)

        # Extract and parse maximum torque values
        slider1_max_value, slider1_unit = self.parse_torque_value(self.motor_torque_mapping['slider1_max'])
        slider2_max_value, slider2_unit = self.parse_torque_value(self.motor_torque_mapping['slider2_max'])

        # Store units for use in displaying torque values later
        self.slider1_unit = slider1_unit
        self.slider2_unit = slider2_unit

        # Slider 1 (controls motors)
        self.slider1 = QSlider(Qt.Orientation.Horizontal)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(int(slider1_max_value))  # Use the max value as is
        self.slider1.setValue(int(slider1_max_value / 2))  # Start at half the maximum value
        self.slider1.valueChanged.connect(lambda: self.slider_moved(1))
        motors_text_1 = ", ".join(map(str, self.motor_torque_mapping['slider1']))
        motor_label_1 = "Motor" if len(self.motor_torque_mapping['slider1']) == 1 else "Motors"
        motor_layout.addWidget(QLabel(f"Slider 1 ({motor_label_1} {motors_text_1})"))
        motor_layout.addWidget(self.slider1)
        # Add QLabel to show the torque value for slider 1
        self.slider1_value_label = QLabel(f"Torque value: {self.slider1.value()} {self.slider1_unit}")
        motor_layout.addWidget(self.slider1_value_label)

        # Slider 2 (controls motors)
        self.slider2 = QSlider(Qt.Orientation.Horizontal)
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(int(slider2_max_value))  # Use the max value as is
        self.slider2.setValue(int(slider2_max_value / 2))  # Start at half the maximum value
        self.slider2.valueChanged.connect(lambda: self.slider_moved(2))
        motors_text_2 = ", ".join(map(str, self.motor_torque_mapping['slider2']))
        motor_label_2 = "Motor" if len(self.motor_torque_mapping['slider2']) == 1 else "Motors"
        motor_layout.addWidget(QLabel(f"Slider 2 ({motor_label_2} {motors_text_2})"))
        motor_layout.addWidget(self.slider2)

        # Add QLabel to show the torque value for slider 2
        self.slider2_value_label = QLabel(f"Torque value: {self.slider2.value()} {self.slider2_unit}")
        motor_layout.addWidget(self.slider2_value_label)


    def change_control_mode(self, index):
        """Change between Robotic Arm Control and Motor Torque Control."""
        self.stacked_widget.setCurrentIndex(index)

    def slider_moved(self, slider_number):
        """Handle slider movements to adjust motor torque"""
        if slider_number == 1:
            torque_value = self.slider1.value()
            self.slider1_value_label.setText(f"Torque value: {torque_value} {self.slider1_unit}")
        elif slider_number == 2:
            torque_value = self.slider2.value()
            self.slider2_value_label.setText(f"Torque value: {torque_value} {self.slider2_unit}")

    def get_arrow_button_style(self):
        """Get the consistent style for the arrow buttons."""
        return """
            QPushButton {
                border: 1px solid #ccc;  /* Light gray border */
                border-radius: 5px;      /* Rounded corners */
                padding: 10px;           /* Padding for size */
                background-color: white; /* White background */
                font-size: 18px;         /* Bigger font */
                font-weight: bold;       /* Bold font */
            }
            QPushButton:hover {
                border: 1px solid #888;  /* Darker border on hover */
            }
            QPushButton:pressed {
                background-color: #f0f0f0;  /* Slightly darker when pressed */
            }
        """
    #left button clicked
    @pyqtSlot()
    def on_left_button_clicked(self):
        """Handle the left button click event."""
        try:
            # In a real application, move the robotic arm left here
            print("Moving the robotic arm left")
            self.next_video.emit()

        except Exception as e:
            QMessageBox.critical(self, "Left Button Error", f"Failed to move the robotic arm left: {e}")

    #right button clicked
    @pyqtSlot()
    def on_right_button_clicked(self):
        """Handle the right button click event."""
        try:
            # In a real application, move the robotic arm right here
            print("Moving the robotic arm right")
            self.previous_video.emit()
        except Exception as e:
            QMessageBox.critical(self, "Right Button Error", f"Failed to move the robotic arm right: {e}")


    @pyqtSlot(int, float)
    def update_motor_display(self, motor_index, torque):
        """Update the motor display based on torque changes."""
        try:
            # In a real application, update the motor status display here
            print(f"Motor {motor_index + 1} torque set to {torque}")
        except Exception as e:
            QMessageBox.critical(self, "Motor Display Error", f"Failed to update motor display: {e}")
