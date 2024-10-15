# views/main_window.py

import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSlot
from .simulation_view import SimulationView
from .real_data_view import RealDataView
from .detailed_view import DetailedView

class MainWindow(QMainWindow):
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.init_ui()
        self.setStyleSheet("background-color: lightgray;")
        # Initialize data simulator
        from core.data_simulator import DataSimulator
        self.data_simulator = DataSimulator()
        self.data_simulator.data_updated.connect(self.update_real_data_view)
        self.data_simulator.start()

    def init_ui(self):
        """Initialize the main window UI."""
        # Set window size from config
        width = self.config.get('window_settings', 'width', default=1200)
        height = self.config.get('window_settings', 'height', default=800)
        background_color = self.config.get('window_settings', 'background_color', default='lightgray')
        self.setWindowTitle("Magnet Placement Machine Control")
        self.setGeometry(100, 100, width, height)


        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Simulation View (Left Half)
        self.simulation_view = SimulationView(self.config)
        self.simulation_view.clicked.connect(self.open_detailed_view_simulated)

        # Real Data View (Right Half)
        self.real_data_view = RealDataView(self.config)
        self.real_data_view.clicked.connect(self.open_detailed_view_real)

        # Add to main layout
        main_layout.addWidget(self.simulation_view)
        main_layout.addWidget(self.real_data_view)

    @pyqtSlot(dict)
    def update_real_data_view(self, data):
        """Update the real data view with sensor data."""
        self.real_data_view.update_overlay(data)

    def open_detailed_view_simulated(self):
        """Transition to the detailed view."""
        self.detailed_view = DetailedView(self.config, real_data=False)
        self.detailed_view.show()
        self.close()
    def open_detailed_view_real(self):
        """Transition to the detailed view."""
        self.detailed_view = DetailedView(self.config, real_data=True)
        self.detailed_view.show()
        self.close()


    def closeEvent(self, event):
        """Handle the window close event."""
        self.data_simulator.stop()
        event.accept()
