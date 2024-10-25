# core/motor_controller.py

from PyQt6.QtCore import QObject, pyqtSignal

class MotorController(QObject):
    # Signal to indicate motor torque has been updated: motor_index, torque_value
    motor_updated = pyqtSignal(int, float)

    def __init__(self, motor_mapping=None, sync_mode='independent', parent=None):
        """
        Initialize the MotorController.

        :param motor_mapping: A dictionary where keys are slider numbers and values are lists of motor indices.
        :param sync_mode: 'synchronized' for setting all motors the same, 'independent' for individual control.
        :param parent: Parent object (default None)
        """
        super().__init__(parent)
        self.sync_mode = sync_mode
        self.motor_torques = [0.0, 0.0, 0.0, 0.0]  # Assuming 4 motors for now
        self.motor_mapping = motor_mapping if motor_mapping else {}

    def set_torque(self, slider_number, torque):
        """
        Set the torque for motors mapped to a given slider.

        :param slider_number: The slider number (e.g., 1 for slider 1)
        :param torque: The torque value to set for the motors
        """
        if slider_number in self.motor_mapping:
            motors_to_update = self.motor_mapping[slider_number]
            for motor_index in motors_to_update:
                self.motor_torques[motor_index - 1] = torque  # motor_index starts at 1, list starts at 0
                self.motor_updated.emit(motor_index - 1, torque)  # Emit the signal for each motor

        elif self.sync_mode == 'synchronized':
            # If synchronized, set all motors to the same torque
            for i in range(4):
                self.motor_torques[i] = torque
                self.motor_updated.emit(i, torque)
        else:
            raise ValueError(f"No motors mapped to slider {slider_number}")

        # TODO: Integrate actual motor control commands here
