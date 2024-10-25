#views.main_window.py
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import pyqtSlot
from .simulation_view import SimulationView
from .real_data_view import RealDataView
from .detailed_view import DetailedView

class MainWindow(QMainWindow):
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.init_ui()
        self.setStyleSheet("background-color: white;")
        
        # Initialize data simulator
        # from core.data_simulator import DataSimulator
        # self.data_simulator = DataSimulator()
        # self.data_simulator.data_updated.connect(self.update_real_data_view)
        # self.data_simulator.start()

    def init_ui(self):
        """Initialize the main window UI."""
        # Set window size from config
        width = self.config.get('window_settings', 'width', default=1200)
        height = self.config.get('window_settings', 'height', default=800)
        background_color = self.config.get('window_settings', 'background_color', default='lightgray')
        self.setWindowTitle("Magnet Placement Machine Control")
        self.setGeometry(100, 100, width, height)

        # Central widget with QStackedWidget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize different views
        self.main_view = QWidget()
        self.detailed_view = DetailedView(self.config, real_data=False)

        # Setup main view layout
        main_layout = QHBoxLayout()
        self.main_view.setLayout(main_layout)

        # Simulation View (Left Half)
        self.simulation_view = SimulationView(self.config)
        self.simulation_view.clicked.connect(self.open_detailed_view_simulated)

        # Real Data View (Right Half)
        self.real_data_view = RealDataView(self.config)
        self.real_data_view.clicked.connect(self.open_detailed_view_real)

        # Add to main layout
        main_layout.addWidget(self.simulation_view)
        main_layout.addWidget(self.real_data_view)

        # Add views to stacked widget
        self.stacked_widget.addWidget(self.main_view)       # Index 0
        self.stacked_widget.addWidget(self.detailed_view)   # Index 1

        # Connect the back_to_main signal from DetailedView to the slot
        self.detailed_view.back_to_main.connect(self.show_main_view)

    @pyqtSlot(dict)
    def update_real_data_view(self, data):
        """Update the real data view with sensor data."""
        self.real_data_view.update_overlay(data)

    def open_detailed_view_simulated(self):
        """Switch to the detailed view with simulated data."""
        self.detailed_view.set_real_data(False)
        self.stacked_widget.setCurrentWidget(self.detailed_view)

    def open_detailed_view_real(self):
        """Switch to the detailed view with real data."""
        self.detailed_view.set_real_data(True)
        self.stacked_widget.setCurrentWidget(self.detailed_view)

    @pyqtSlot()
    def show_main_view(self):
        """Switch back to the main view."""
        self.stacked_widget.setCurrentWidget(self.main_view)
        print("Switched back to main view.")

    def closeEvent(self, event):
        """Handle the window close event."""
        self.data_simulator.stop()
        self.detailed_view.cleanup()
        event.accept()
