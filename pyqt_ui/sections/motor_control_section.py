# sections/motor_control_section.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QMessageBox
from PyQt6.QtCore import Qt, pyqtSlot
from core.motor_controller import MotorController

class MotorControlSection(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.init_ui()
        self.init_motor_controller()

    def init_ui(self):
        """Initialize the Motor Control Section."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Motor Control")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        # Sliders for four motors
        self.sliders = []
        for i in range(4):
            motor_label = QLabel(f"Motor {i+1} Torque")
            layout.addWidget(motor_label)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(50)
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.setTickInterval(10)
            slider.valueChanged.connect(lambda value, idx=i: self.slider_moved(idx, value))
            layout.addWidget(slider)
            self.sliders.append(slider)

    def init_motor_controller(self):
        """Initialize the motor controller."""
        sync_mode = self.config.get('motor_slider_synchronization', 'sync_mode', default='independent')
        self.motor_controller = MotorController(sync_mode=sync_mode)
        self.motor_controller.motor_updated.connect(self.update_motor_display)

    def slider_moved(self, motor_index, value):
        """Handle slider movements to adjust motor torque."""
        try:
            torque = value / 100.0  # Normalize torque value
            self.motor_controller.set_torque(motor_index, torque)
        except Exception as e:
            QMessageBox.critical(self, "Motor Control Error", f"Failed to set motor torque: {e}")

    @pyqtSlot(int, float)
    def update_motor_display(self, motor_index, torque):
        """Update the motor display based on torque changes."""
        try:
            # In a real application, update the motor status display here
            print(f"Motor {motor_index + 1} torque set to {torque}")
        except Exception as e:
            QMessageBox.critical(self, "Motor Display Error", f"Failed to update motor display: {e}")
