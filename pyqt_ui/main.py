import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow


if __name__ == "__main__":

    app = QApplication(sys.argv)

    # create main window and show it

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
    