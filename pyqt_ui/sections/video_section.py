# sections/animation_section.py

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QSize, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QMovie

class AnimationSection(QWidget):
    next_video_signal = pyqtSignal()
    video_number = 0
    frame_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_animation()
        self.video_list = ["assets/m2.gif", "assets/m3.gif", "assets/m4.gif", "assets/m5.gif", "assets/m6.gif"]
        self.gif.frameChanged.connect(self.on_frame_changed)

    def init_ui(self):
        """Initialize the Animation Data Section."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Animation Label with resizable GIF
        self.animation_label = QLabel()
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.animation_label)

    def init_animation(self):
        """Initialize animation using a GIF."""
        # Load GIF
        self.gif = QMovie("assets/m2.gif")  # Replace with the actual path to your GIF
        self.animation_label.setMovie(self.gif)
        self.gif.start()

    @pyqtSlot()
    def update_gif(self, gif_path):
        """Update the GIF with the given path."""
        self.gif = QMovie(gif_path)
        self.gif.frameChanged.connect(self.on_frame_changed)
        self.animation_label.setMovie(self.gif)
        self.update_gif_size(self.animation_label.size())
        self.gif.start()

    @pyqtSlot()
    def next_video(self):
        """Update the GIF with the next video in the list."""
        self.video_number = (self.video_number + 1) % len(self.video_list)
        self.update_gif(self.video_list[self.video_number])

    @pyqtSlot()
    def previous_video(self):
        """Update the GIF with the previous video in the list."""
        self.video_number = (self.video_number - 1) % len(self.video_list)
        self.update_gif(self.video_list[self.video_number])

    def update_gif_size(self, new_size):
        """Adjust the GIF size based on the given size."""
        if self.gif is not None:
            self.gif.setScaledSize(QSize(new_size.width(), new_size.height()))

    def stop_animation(self):
        """Stop the GIF animation."""
        if self.gif is not None:
            self.gif.stop()

    @pyqtSlot(int)
    def on_frame_changed(self, frame_number):
        """Emit the frame_changed signal when the frame of the GIF changes."""
        self.frame_changed.emit(frame_number)