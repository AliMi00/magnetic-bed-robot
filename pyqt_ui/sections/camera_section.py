# sections/camera_section.py

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSlot
from core.camera_stream import CameraStreamHandler

class CameraSection(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.init_ui()
        self.init_camera()

    def init_ui(self):
        """Initialize the Camera Stream Section."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Camera Stream")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        # Camera Label
        self.camera_label = QLabel("Initializing Camera...")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.camera_label)

    def init_camera(self):
        """Initialize the camera stream handler."""
        self.camera_handler = CameraStreamHandler()
        self.camera_handler.frame_updated.connect(self.update_camera_stream)
        self.camera_handler.start()

    # @pyqtSlot(QImage)
    def update_camera_stream(self, qt_image):
        """Update the camera stream with new frames."""
        pixmap = QPixmap.fromImage(qt_image)
        self.camera_label.setPixmap(pixmap.scaled(
            self.camera_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def stop_camera(self):
        """Stop the camera stream."""
        self.camera_handler.stop()
