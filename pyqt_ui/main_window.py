from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QComboBox, QGridLayout
from scenario_1 import Scenario1
from scenario_2 import Scenario2
from scenario_3 import Scenario3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Magnet Placement Techniques")

        # Central widget
        self.central_widget = QWidget()
        self.layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Combo box to select different scenarios
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Scenario 1", "Scenario 2", "Scenario 3"])
        self.combo_box.currentIndexChanged.connect(self.change_scenario)

        self.layout.addWidget(self.combo_box, 0, 0, 1, 1)

        # Placeholder for the current scenario page
        self.scenario_widget = None

        # Initialize the first scenario
        self.change_scenario(0)

    def change_scenario(self, index):
        """Switches the scenario page based on the combo box selection."""
        if self.scenario_widget:
            # Remove the existing scenario widget
            self.layout.removeWidget(self.scenario_widget)
            self.scenario_widget.deleteLater()

        if index == 0:
            self.scenario_widget = Scenario1()
        elif index == 1:
            self.scenario_widget = Scenario2()
        elif index == 2:
            self.scenario_widget = Scenario3()

        # Add the new scenario widget to the layout
        self.layout.addWidget(self.scenario_widget, 1, 0, 1, 8)