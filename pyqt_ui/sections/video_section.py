# sections/animation_section.py

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QMovie

class AnimationSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_animation()

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
        self.gif = QMovie("assets/science-field.gif")  # Replace with the actual path to your GIF
        self.animation_label.setMovie(self.gif)
        self.gif.start()

    def update_gif_size(self, new_size):
        """Adjust the GIF size based on the given size."""
        if self.gif is not None:
            self.gif.setScaledSize(QSize(new_size.width(), new_size.height()))

    def stop_animation(self):
        """Stop the GIF animation."""
        if self.gif is not None:
            self.gif.stop()
