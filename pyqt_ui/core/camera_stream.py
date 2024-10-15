# core/camera_stream.py

import cv2
import threading
import time
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QMessageBox


class CameraStreamHandler(QObject):
    frame_updated = pyqtSignal(QImage)

    def __init__(self, camera_index=0, parent=None):
        super().__init__(parent)
        self.running = False
        self.cap = None
        self.camera_index = camera_index

    def start(self):
        """Start the camera stream in a separate thread."""
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            QMessageBox.warning(None, "Camera Error", "Unable to access the camera.")
            return
        self.running = True
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        """Stop the camera stream."""
        self.running = False
        if self.cap:
            self.cap.release()

    def run(self):
        """Capture frames from the camera and emit them."""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to RGB format
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.frame_updated.emit(qt_image)
            time.sleep(0.03)  # Approximately 30 FPS
