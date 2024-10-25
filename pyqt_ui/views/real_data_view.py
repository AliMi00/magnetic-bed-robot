# views/real_data_view.py

from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal
import os

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

class RealDataView(ClickableLabel):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.init_ui()

    def init_ui(self):
        """Initialize the real data view UI."""
        real_bg_path = self.config.get('window_settings', 'real_data_background', default='')
        if real_bg_path and os.path.exists(real_bg_path):
            real_pixmap = QPixmap(real_bg_path)
        else:
            real_pixmap = QPixmap(600, 800)
            real_pixmap.fill(Qt.GlobalColor.darkGray)
        
        window_width = self.config.get('window_settings', 'width', default=1200)
        window_height = self.config.get('window_settings', 'height', default=800)
        self.setPixmap(real_pixmap.scaled(window_width//2, window_height, Qt.AspectRatioMode.KeepAspectRatioByExpanding))
        self.setScaledContents(True)
        self.setFixedSize(window_width//2, window_height)

        # Add "Real" text overlay
        self.overlay_label_title = QLabel("Real", self)
        self.overlay_label_title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.overlay_label_title.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 150); padding: 10px;")
        self.overlay_label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set position and size of the "Real" label
        self.overlay_label_title.setGeometry(0, 0, window_width//2, 50)  # Position at top-center

    def update_overlay(self, data):
        """Overlay sensor data as text."""
        overlay_text = "\n".join([f"{k.capitalize()}: {v:.2f}" for k, v in data.items()])
        # Create a semi-transparent label to display data
        if hasattr(self, 'overlay_label'):
            self.overlay_label.setText(overlay_text)
        else:
            self.overlay_label = QLabel(self)
            self.overlay_label.setText(overlay_text)
            self.overlay_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 128);")
            self.overlay_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self.overlay_label.setFixedSize(self.width(), 100)
            self.overlay_label.move(10, 60)  # Position slightly below the "Real" label
            self.overlay_label.show()

