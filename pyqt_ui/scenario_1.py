from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QLineEdit
from scenario_base import ScenarioBase

class Scenario1(ScenarioBase):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("Scenario 1: Magnet Placement Technique 1")
        layout.addWidget(label)
        # Additional widgets and logic specific to Scenario 1 can be added here

        button = QPushButton("Press Me!")
        layout.addWidget(button)

        # You can connect signals for the button if needed
        button.clicked.connect(self.button_clicked)



    def button_clicked(self):
        print("Button in Scenario 1 clicked!")