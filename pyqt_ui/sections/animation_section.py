# sections/animation_section.py

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer

class AnimationSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_animation()

    def init_ui(self):
        """Initialize the Animation Data Section."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("3D Simulation")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        # Animation Label
        self.animation_label = QLabel()
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.animation_label.setText("Initializing Animation...")
        layout.addWidget(self.animation_label)

    def init_animation(self):
        """Initialize animation using a QTimer."""
        self.states = ["Animating...", "Placing Magnet...", "Calibrating...", "Idle..."]
        self.current_state = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(1000)  # Update every second

    def update_animation(self):
        """Update the animation state."""
        self.animation_label.setText(self.states[self.current_state])
        self.current_state = (self.current_state + 1) % len(self.states)

    def stop_animation(self):
        """Stop the animation timer."""
        self.timer.stop()
