from PySide6.QtWidgets import QWidget
from abc import abstractmethod

class ScenarioBase(QWidget):
    """Base class for all magnet placement technique scenarios."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def setup_ui(self):
        """Method to set up the UI for each scenario."""
        pass
