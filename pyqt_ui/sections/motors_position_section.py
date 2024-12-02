# sections/motors_position_section.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import yaml

class MotorsPositionSection(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.num_axes = self.load_axes("config/param_set_axes.yaml")
        self.init_ui()
    
    def load_axes(self, filename):
        """Load the number of axes to plot from .yaml file"""
        with open(filename, "r") as file:
            data = yaml.safe_load(file)
            num_axes = data.get('axes', 3)  # Default to 3 if not specified
            if num_axes not in [2, 3]:
                raise ValueError("Axes value must be either 2 or 3.")
            return num_axes
    
    def init_ui(self):
        """Initialize the Motors Position UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Motors Position")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 16px; padding-bottom: 10px;")
        layout.addWidget(title)

        # Create a table for motor positions
        if self.num_axes == 3:
            self.table = QTableWidget(3, 3)  # 4 rows for X, Y, Z; 3 columns for Axis, Actual Position, Target Position
        else:
            self.table = QTableWidget(2, 3)  # 3 rows for X, Y; 3 columns for Axis, Actual Position, Target Position

        self.table.setHorizontalHeaderLabels(["Axis", "Actual Position", "Target Position"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set default values for the table
        axes = ['X', 'Y', 'Z'] if self.num_axes == 3 else ['X', 'Y']

        for i, axis in enumerate(axes):
            # Axis column - Non-editable
            axis_item = QTableWidgetItem(axis)
            axis_item.setFlags(axis_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i, 0, axis_item)

            # Actual Position column - Non-editable
            actual_position_item = QTableWidgetItem("+0.00 mm")
            actual_position_item.setFlags(actual_position_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i, 1, actual_position_item)

            # Target Position column - Editable
            target_position_item = QTableWidgetItem("+0.00 mm")
            self.table.setItem(i, 2, target_position_item)

        # Style the table
        self.table.setFont(QFont('Arial', 10))
        self.table.setStyleSheet("QTableWidget { border: 1px solid #ccc; } QHeaderView::section { background-color: lightgray; }")
        layout.addWidget(self.table)

        # Connect the item changed signal to a slot
        self.table.itemChanged.connect(self.on_item_changed)

    def update_motor_positions(self, data):
        """Update the motor positions with actual and target data."""
        for i, (axis, values) in enumerate(data.items()):
            actual_position_item = QTableWidgetItem(f"{values['actual']} mm")
            actual_position_item.setFlags(actual_position_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(i, 1, actual_position_item)
            
            target_position_item = QTableWidgetItem(f"{values['target']} mm")
            self.table.setItem(i, 2, target_position_item)

    def on_item_changed(self, item):
        """Handle changes made to the table."""
        # Only handle changes in the target position column (column index 2)
        if item.column() == 2:
            try:
                # Validate and process the target position input
                value = item.text().strip()
                if not value.endswith("mm"):
                    raise ValueError("Invalid notation. Only 'mm' is allowed for Target Position.")
                
                # Remove 'mm' and convert to float to validate
                numeric_value = float(value.replace("mm", "").strip())
                
                # Here, you could trigger an update to the actual motor positions
                # Example: Send the updated target position to the motor controller
                print(f"Updated Target Position for Axis {self.table.item(item.row(), 0).text()}: {numeric_value} mm")
            
            except ValueError as e:
                # Show an error message box to the user
                QMessageBox.warning(self, "Invalid Input", f"{e}\nPlease enter a value in 'mm' (e.g., '+10.00 mm').")

                # Reset the item text to the previous value or default
                item.setText("+0.00 mm")
