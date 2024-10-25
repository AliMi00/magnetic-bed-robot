# views/simulation_view.py

from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal

import os

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

class SimulationView(ClickableLabel):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.init_ui()

    def init_ui(self):
        """Initialize the simulation view UI."""
        sim_bg_path = self.config.get('window_settings', 'simulation_background', default='')
        if sim_bg_path and os.path.exists(sim_bg_path):
            sim_pixmap = QPixmap(sim_bg_path)
        else:
            sim_pixmap = QPixmap(600, 800)
            sim_pixmap.fill(Qt.GlobalColor.lightGray)

        # Set the background image for the SimulationView
        window_width = self.config.get('window_settings', 'width', default=1200)
        window_height = self.config.get('window_settings', 'height', default=800)
        self.setPixmap(sim_pixmap.scaled(window_width//2, window_height, Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        self.setScaledContents(True)
        self.setFixedSize(window_width//2, window_height)

        # Add "Simulation" text overlay
        self.overlay_label = QLabel("Simulation", self)
        self.overlay_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.overlay_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); padding: 10px;")
        self.overlay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set overlay position (centered)
        self.overlay_label.setGeometry(0, 0, window_width//2, 50)  # Set the label width to match the view width and position at the top
