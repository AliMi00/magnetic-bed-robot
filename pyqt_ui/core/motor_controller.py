# core/motor_controller.py

from PyQt6.QtCore import QObject, pyqtSignal

class MotorController(QObject):
    # Signal to indicate motor torque has been updated: motor_index, torque_value
    motor_updated = pyqtSignal(int, float)

    def __init__(self, sync_mode='independent', parent=None):
        super().__init__(parent)
        self.sync_mode = sync_mode
        self.motor_torques = [0.0, 0.0, 0.0, 0.0]

    def set_torque(self, motor_index, torque):
        """Set the torque for a specific motor."""
        if self.sync_mode == 'synchronized':
            # If synchronized, set all motors to the same torque
            for i in range(4):
                self.motor_torques[i] = torque
                self.motor_updated.emit(i, torque)
        else:
            # Independent mode
            self.motor_torques[motor_index] = torque
            self.motor_updated.emit(motor_index, torque)
        # TODO: Integrate actual motor control commands here
