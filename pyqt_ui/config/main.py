# main.py

import sys
from PyQt6.QtWidgets import QApplication
from core.config_manager import ConfigManager
from views.main_window import MainWindow

def main():
    """Entry point of the application."""
    app = QApplication(sys.argv)

    # Initialize configuration
    config_manager = ConfigManager()

    # Initialize and show main window
    main_window = MainWindow(config_manager)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
