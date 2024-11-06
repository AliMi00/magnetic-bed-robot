#views/detailed_view.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QSizePolicy, QFrame
from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt, QSize
from core.data_simulator import DataSimulator
from core.motor_controller import MotorController
from core.camera_stream import CameraStreamHandler
from sections.graph_section import GraphSection
from sections.animation_section import AnimationSection
from sections.video_section import AnimationSection as VideoSection 
from sections.motor_control_section import MotorControlSection

class DetailedView(QWidget):
    # Define a custom signal to notify MainWindow to switch back to the main view
    back_to_main = pyqtSignal()

    def __init__(self, config_manager, ):
        super().__init__()
        self.config = config_manager
        
        self.init_ui()

        # Set background color based on data type
        background_color = self.config.get(
            'simulated',
            'background_color',
            default='lightgray'
        )
        self.setStyleSheet(f"background-color: {background_color};")

        # Initialize components
        self.graph_section = GraphSection(self.config)
        self.animation_section = AnimationSection()
        self.video_section = VideoSection()
        self.motor_control_section = MotorControlSection(self.config)

        # Layout setup
        main_layout = QVBoxLayout()
       
        grid_layout = QGridLayout()
        self.setLayout(main_layout)

        # Add button to move to main window
        self.main_window_button = QPushButton("Home")
        self.main_window_button.setFixedSize(60, 20)
        self.main_window_button.clicked.connect(self.move_to_main_window)
        main_layout.addWidget(self.main_window_button)

        # Add sections to grid with frames for separation
        main_layout.addLayout(grid_layout)

        # Create frames for separation
        self.graph_frame = QFrame()
        self.graph_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_frame.setFrameShadow(QFrame.Shadow.Raised)
        graph_layout = QVBoxLayout(self.graph_frame)
        graph_layout.addWidget(self.graph_section)
        grid_layout.addWidget(self.graph_frame, 0, 0)

        self.animation_frame = QFrame()
        self.animation_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.animation_frame.setFrameShadow(QFrame.Shadow.Raised)
        animation_layout = QVBoxLayout(self.animation_frame)
        animation_layout.addWidget(self.animation_section)
        grid_layout.addWidget(self.animation_frame, 0, 1)

        self.camera_frame = QFrame()
        self.camera_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.camera_frame.setFrameShadow(QFrame.Shadow.Raised)
        camera_layout = QVBoxLayout(self.camera_frame)
        camera_layout.addWidget(self.video_section)
        grid_layout.addWidget(self.camera_frame, 1, 0)

        self.motor_control_frame = QFrame()
        self.motor_control_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.motor_control_frame.setFrameShadow(QFrame.Shadow.Raised)
        motor_control_layout = QVBoxLayout(self.motor_control_frame)
        motor_control_layout.addWidget(self.motor_control_section)
        grid_layout.addWidget(self.motor_control_frame, 1, 1)

        # Configure grid layout ratios
        grid_layout.setRowStretch(0, 1)
        grid_layout.setRowStretch(1, 1)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

    def resizeEvent(self, event):
            """Handle the window resize event to adjust the animation size to 1/4 of the screen."""
            window_width = self.width()
            window_height = self.height()
            quarter_size = QSize(window_width // 2, window_height // 2)
            
            self.video_section.update_gif_size(quarter_size)
            super().resizeEvent(event)

    def init_ui(self):
        """Initialize the detailed view UI."""
        width = self.config.get('window_settings', 'width', default=1200)
        height = self.config.get('window_settings', 'height', default=800)
        self.setWindowTitle("Detailed View - Magnet Placement Machine")

    @pyqtSlot()
    def move_to_main_window(self):
        """Handle the button click to move to the main window."""
        # Emit the signal to notify MainWindow to switch views
        self.back_to_main.emit()
        self.cleanup()
        self.graph_section.clear_graph_data()
        print("Home button clicked. Emitting back_to_main signal...")

    # def set_real_data(self, real_data):
    #     """Update the view to use simulated data."""

    #     background_color = self.config.get(
    #         'real_data' , 
    #         'background_color', 
    #         default='lightgray'
    #     )
    #     self.setStyleSheet(f"background-color: {background_color};")
        
    #     self.cleanup_simulated_data()
    #     self.init_simulated_data()

    def set_simulated(self):
        """Update the view to use simulated data."""

        background_color = self.config.get(
            'simulated', 
            'background_color', 
            default='lightgray'
        )
        self.setStyleSheet(f"background-color: {background_color};")
        
        self.cleanup_simulated_data()
        self.init_simulated_data()

    def init_simulated_data(self):
        """Initialize simulated data components."""
        if not hasattr(self, 'data_simulator'):
            self.data_simulator = DataSimulator()
            self.data_simulator.data_updated.connect(self.graph_section.update_graph_data)
            self.data_simulator.start()

    def cleanup_simulated_data(self):
        """Cleanup simulated data components."""
        if hasattr(self, 'data_simulator'):
            self.data_simulator.stop()
            del self.data_simulator

    def cleanup(self):
        """Cleanup resources when switching views."""
        if hasattr(self, 'data_simulator'):
            self.data_simulator.stop()
        self.animation_section.stop_animation()
        # Add any other cleanup tasks here
