# views/detailed_view.py

from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout
from PyQt6.QtCore import pyqtSlot
from core.config_manager import ConfigManager
from core.data_simulator import DataSimulator
from core.motor_controller import MotorController
from core.camera_stream import CameraStreamHandler

from sections.graph_section import GraphSection
from sections.animation_section import AnimationSection
from sections.camera_section import CameraSection
from sections.motor_control_section import MotorControlSection

class DetailedView(QMainWindow):
    def __init__(self, config_manager, real_data=False):
        super().__init__()
        self.config = config_manager
        self.init_ui()

        # set for real data or simulated
        if real_data:
            background_color = self.config.get('simulated', 'background_color', default='lightgray')
            self.setStyleSheet("background-color: " + background_color + ";")
        else:
            background_color = self.config.get('real_data', 'background_color', default='lightgray')
            self.setStyleSheet("background-color: " + background_color + ";")

        # Initialize components
        self.graph_section = GraphSection(self.config)
        self.animation_section = AnimationSection()
        self.camera_section = CameraSection(self.config)
        self.motor_control_section = MotorControlSection(self.config)

        # Layout setup
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Add button to move to main window
        self.main_window_button = QPushButton("Main Window")
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

        # Initialize data simulator
        self.data_simulator = DataSimulator()
        self.data_simulator.data_updated.connect(self.graph_section.update_graph_data)
        self.data_simulator.start()

    def init_ui(self):
        """Initialize the detailed view UI."""
        self.setWindowTitle("Detailed View - Magnet Placement Machine")
        width = self.config.get('window_settings', 'width', default=1200)
        height = self.config.get('window_settings', 'height', default=800)
        self.setGeometry(150, 150, width, height)

    @pyqtSlot()
    def move_to_main_window(self):
        """Handle the button click to move to the main window."""
        # Logic to switch to the main window goes here
        from views.main_window import MainWindow
        self.main_window = MainWindow(self.config)
        self.main_window.show()
        self.close()
        print("Moving to main window...")

    def closeEvent(self, event):
        """Handle the window close event."""
        self.data_simulator.stop()
        self.camera_section.stop_camera()
        self.animation_section.stop_animation()
        event.accept()
