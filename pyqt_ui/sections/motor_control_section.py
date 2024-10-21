# sections/motor_control_section.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QMessageBox
from PyQt6.QtCore import Qt, pyqtSlot

from core.motor_controller import MotorController
import yaml
class MotorControlSection(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.motor_torque_mapping = self.load_motor_mapping("config/param_motors_control.yaml")  
        self.init_ui()
        self.init_motor_controller()
     
    def load_motor_mapping(self, filename):
        """Load motor mapping from a .yaml file"""
        with open(filename, "r") as file:
            return yaml.safe_load(file)
    

    def init_ui(self):
        """Initialize the Motor Control Section."""
        layout = QVBoxLayout()
        self.setLayout(layout)

         # Title
        title = QLabel("Torque Motor Control")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px; padding-bottom: 10px;")
        layout.addWidget(title)

       
        # Slider 1 (controls two motors)
        self.slider1 = QSlider(Qt.Orientation.Horizontal)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(187)
        self.slider1.setValue(93)
        self.slider1.valueChanged.connect(lambda: self.slider_moved(1))
        layout.addWidget(QLabel(f"Slider 1 (Motors {self.motor_torque_mapping['slider1'][0]}, {self.motor_torque_mapping['slider1'][1]})"))
        layout.addWidget(self.slider1)

        # Add QLabel to show the torque value for slider 1
        self.slider1_value_label = QLabel(f"Torque value: {self.slider1.value()} Ncm")
        layout.addWidget(self.slider1_value_label)

        # Slider 2 (controls two motors)
        self.slider2 = QSlider(Qt.Orientation.Horizontal)
        self.slider2.setMinimum(0)
        self.slider2.setMaximum(187)
        self.slider2.setValue(93)
        self.slider2.valueChanged.connect(lambda: self.slider_moved(2))
        layout.addWidget(QLabel(f"Slider 2 (Motors {self.motor_torque_mapping['slider2'][0]}, {self.motor_torque_mapping['slider2'][1]})"))
        layout.addWidget(self.slider2)

        # Add QLabel to show the torque value for slider 2
        self.slider2_value_label = QLabel(f"Torque value: {self.slider2.value()} Ncm")
        layout.addWidget(self.slider2_value_label)

   
    def init_motor_controller(self):
        """Initialize the motor controller."""
        sync_mode = self.config.get('motor_slider_synchronization', 'sync_mode', default='independent')
        self.motor_controller = MotorController(sync_mode=sync_mode)
        self.motor_controller.motor_updated.connect(self.update_motor_display)

    def slider_moved(self, slider_number):
        """Handle slider movements to adjust motor torque"""
        if slider_number == 1:
            motor1, motor2 = self.motor_torque_mapping['slider1']
            torque_value = self.slider1.value()
            self.slider1_value_label.setText(f"Torque value: {torque_value} Ncm")
        elif slider_number == 2:
            motor1, motor2 = self.motor_torque_mapping['slider2']
            torque_value = self.slider2.value()
            self.slider2_value_label.setText(f"Torque value: {torque_value} Ncm")
        


    @pyqtSlot(int, float)
    def update_motor_display(self, motor_index, torque):
        """Update the motor display based on torque changes."""
        try:
            # In a real application, update the motor status display here
            print(f"Motor {motor_index + 1} torque set to {torque}")
        except Exception as e:
            QMessageBox.critical(self, "Motor Display Error", f"Failed to update motor display: {e}")
