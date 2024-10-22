from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QFrame, QLabel
)
from PyQt6.QtCore import Qt
import sys


class SimpleGridLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the UI with QGridLayout, four containers, and separator lines."""
        # Set up the main layout as QVBoxLayout
        main_layout = QVBoxLayout(self)

        # Set up the grid layout
        grid_layout = QGridLayout()

        # Container 1
        container_1 = QLabel("Container 1")
        container_1.setStyleSheet("background-color: lightblue; border: 1px solid black;")
        container_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(container_1, 0, 0)

        # Vertical Separator between Container 1 and Container 2
        vertical_line_1 = QFrame()
        vertical_line_1.setFrameShape(QFrame.Shape.VLine)
        vertical_line_1.setFrameShadow(QFrame.Shadow.Sunken)
        grid_layout.addWidget(vertical_line_1, 0, 1)

        # Container 2
        container_2 = QLabel("Container 2")
        container_2.setStyleSheet("background-color: lightgreen; border: 1px solid black;")
        container_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(container_2, 0, 2)

        # Horizontal Separator between the first and second row
        horizontal_line_1 = QFrame()
        horizontal_line_1.setFrameShape(QFrame.Shape.HLine)
        horizontal_line_1.setFrameShadow(QFrame.Shadow.Sunken)
        grid_layout.addWidget(horizontal_line_1, 1, 0, 1, 3)

        # Container 3
        container_3 = QLabel("Container 3")
        container_3.setStyleSheet("background-color: lightyellow; border: 1px solid black;")
        container_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(container_3, 2, 0)

        # Vertical Separator between Container 3 and Container 4
        vertical_line_2 = QFrame()
        vertical_line_2.setFrameShape(QFrame.Shape.VLine)
        vertical_line_2.setFrameShadow(QFrame.Shadow.Sunken)
        grid_layout.addWidget(vertical_line_2, 2, 1)

        # Container 4
        container_4 = QLabel("Container 4")
        container_4.setStyleSheet("background-color: lightcoral; border: 1px solid black;")
        container_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(container_4, 2, 2)

        # Configure row and column stretch to make the layout more flexible
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(2, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(2, 1)

        # Add the grid layout to the main layout
        main_layout.addLayout(grid_layout)

        # Set window properties
        self.setWindowTitle("Simple QGridLayout with Separators")
        self.setGeometry(100, 100, 800, 600)


# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleGridLayout()
    window.show()
    sys.exit(app.exec())
