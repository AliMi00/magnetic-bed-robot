import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import qdarkstyle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern PyQt6 UI")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply qdarkstyle stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())