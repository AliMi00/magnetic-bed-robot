from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from core.config_manager import ConfigManager
from core.data_simulator import DataSimulator
from core.motor_controller import MotorController
from core.camera_stream import CameraStreamHandler

from sections.graph_section import GraphSection
from sections.animation_section import AnimationSection
from sections.camera_section import CameraSection
from sections.motor_control_section import MotorControlSection

class DetailedView(QWidget):
    # Define a custom signal to notify MainWindow to switch back to the main view
    back_to_main = pyqtSignal()

    def __init__(self, config_manager, real_data=False):
        super().__init__()
        self.config = config_manager
        self.real_data = real_data
        self.init_ui()

        # Set background color based on data type
        background_color = self.config.get(
            'real_data' if real_data else 'simulated', 
            'background_color', 
            default='lightgray'
        )
        self.setStyleSheet(f"background-color: {background_color};")

        # Initialize components
        self.graph_section = GraphSection(self.config)
        self.animation_section = AnimationSection()
        self.camera_section = CameraSection(self.config)
        self.motor_control_section = MotorControlSection(self.config)

        # Layout setup
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        self.setLayout(main_layout)

        # Add button to move to main window
        self.main_window_button = QPushButton("Home")
        self.main_window_button.clicked.connect(self.move_to_main_window)
        main_layout.addWidget(self.main_window_button)

        # Add sections to grid
        main_layout.addLayout(grid_layout)
        grid_layout.addWidget(self.graph_section, 0, 0)
        grid_layout.addWidget(self.animation_section, 0, 1)
        grid_layout.addWidget(self.camera_section, 1, 0)
        grid_layout.addWidget(self.motor_control_section, 1, 1)

        # Configure grid layout ratios
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

        # Initialize data simulator if using simulated data
        if not self.real_data:
            self.data_simulator = DataSimulator()
            self.data_simulator.data_updated.connect(self.graph_section.update_graph_data)
            self.data_simulator.start()
        else:
            # Initialize real data handlers here if necessary
            pass

    def init_ui(self):
        """Initialize the detailed view UI."""
        width = self.config.get('window_settings', 'width', default=1200)
        height = self.config.get('window_settings', 'height', default=800)
        self.setFixedSize(width, height)
        self.setWindowTitle("Detailed View - Magnet Placement Machine")

    @pyqtSlot()
    def move_to_main_window(self):
        """Handle the button click to move to the main window."""
        # Emit the signal to notify MainWindow to switch views
        self.back_to_main.emit()
        print("Home button clicked. Emitting back_to_main signal...")

    def set_real_data(self, real_data):
        """Update the view to use real or simulated data."""
        if self.real_data != real_data:
            self.real_data = real_data
            background_color = self.config.get(
                'real_data' if real_data else 'simulated', 
                'background_color', 
                default='lightgray'
            )
            self.setStyleSheet(f"background-color: {background_color};")
            
            # Start or stop data simulators accordingly
            if real_data:
                # Initialize real data handlers
                self.cleanup_simulated_data()
                # Initialize real data simulators if necessary
            else:
                # Initialize simulated data simulators
                self.init_simulated_data()

    def init_simulated_data(self):
        """Initialize simulated data components."""
        if not hasattr(self, 'data_simulator'):
            self.data_simulator = DataSimulator()
            self.data_simulator.data_updated.connect(self.graph_section.update_graph_data)
            self.data_simulator.start()

    def cleanup_simulated_data(self):
        """Cleanup simulated data components."""
        if hasattr(self, 'data_simulator'):
            self.data_simulator.stop()
            del self.data_simulator

    def cleanup(self):
        """Cleanup resources when switching views."""
        if not self.real_data and hasattr(self, 'data_simulator'):
            self.data_simulator.stop()
        self.camera_section.stop_camera()
        self.animation_section.stop_animation()
        # Add any other cleanup tasks here
