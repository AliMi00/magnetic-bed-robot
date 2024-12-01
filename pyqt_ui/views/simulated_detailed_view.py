# views/simulated_detailed_view.py

from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QSizePolicy, QFrame, QHBoxLayout, QLabel
from PyQt6.QtCore import pyqtSlot, pyqtSignal, Qt, QSize
from core.data_simulator import DataSimulator
from core.motor_controller import MotorController
from core.camera_stream import CameraStreamHandler
from sections.graph_section import GraphSection
from sections.animation_section import AnimationSection
from sections.video_section import AnimationSection as VideoSection 
from sections.motor_control_section import MotorControlSection
from sections.motors_position_section import MotorsPositionSection


class DetailedView(QWidget):
    # Define a custom signal to notify MainWindow to switch back to the main view
    back_to_main = pyqtSignal()

    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
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
        self.motors_position_section = MotorsPositionSection(self.config)
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

        # Add horizontal layout for Home button and Page Title
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins from the header layout
        header_layout.setSpacing(0)  # Minimize spacing between items in the header layout

        # Title Label 
        self.page_title_label = QLabel("Simulation Page")  # Change to "Real Page" in real_detailed_view.py
        self.page_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_title_label.setStyleSheet("""
            font-weight: bold; 
            font-size: 16px; 
            background-color: white;  /* Set background to white */
            padding: 0px;  /* Remove extra padding */
            margin: 0px;   /* Remove extra margin */
        """)
        header_layout.addWidget(self.page_title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the header layout to the main layout
        main_layout.addLayout(header_layout, stretch=0)


        # Add sections to grid with frames for separation
        main_layout.addLayout(grid_layout)

        # Create frames for separation
        self.graph_frame = QFrame()
        self.graph_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_frame.setFrameShadow(QFrame.Shadow.Raised)
        graph_layout = QVBoxLayout(self.graph_frame)
        graph_layout.addWidget(self.graph_section)
        grid_layout.addWidget(self.graph_frame, 0, 0)

        self.motors_position_frame = QFrame()
        self.motors_position_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.motors_position_frame.setFrameShadow(QFrame.Shadow.Raised)
        animation_layout = QVBoxLayout(self.motors_position_frame)
        animation_layout.addWidget(self.motors_position_section)
        grid_layout.addWidget(self.motors_position_frame, 0, 1)

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

        # Connect the motor control section's signal to the video section's slot
        self.motor_control_section.next_video.connect(self.video_section.next_video)
        self.motor_control_section.previous_video.connect(self.video_section.previous_video)

        # Connect the frameChanged signal to update the graph and motor positions
        self.video_section.frame_changed.connect(self.update_on_frame_change)

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
    def goto_next_video(self):
        self.video_section.next_video()
    
    @pyqtSlot()
    def goto_previous_video(self):
        self.video_section.previous_video()

    @pyqtSlot()
    def move_to_main_window(self):
        """Handle the button click to move to the main window."""
        # Emit the signal to notify MainWindow to switch views
        self.back_to_main.emit()
        self.cleanup()
        self.graph_section.clear_graph_data()
        print("Home button clicked. Emitting back_to_main signal...")

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
            self.data_simulator.data_updated.connect(self.update_motor_positions)
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
        # Add any other cleanup tasks here

    @pyqtSlot(int)
    def update_on_frame_change(self, frame_number):
        """Update the graph data and motor positions when the frame of the GIF changes."""
        if frame_number == 0:
            self.graph_section.clear_graph_data()
        else:
            if hasattr(self, 'data_simulator'):
                self.data_simulator.emit_next_data(frame_number - 1)

    @pyqtSlot(dict)
    def update_motor_positions(self, data):
        """Update motor positions based on the data."""
        motor_data = {
            'X': {'actual': data['Distance'], 'target': data['Distance_adjusted']},
            'Y': {'actual': data['Distance'], 'target': data['Distance_adjusted']},
            'Z': {'actual': data['Distance'], 'target': data['Distance_adjusted']}
        }
        self.motors_position_section.update_motor_positions(motor_data)

    # @pyqtSlot(int)
    # def update_graph_on_frame_change(self, frame_number):
    #     """Update the graph data when the frame of the GIF changes."""
    #     if frame_number == 0:
    #         self.graph_section.clear_graph_data()
    #     else:
    #         if hasattr(self, 'data_simulator'):

    #             self.data_simulator.emit_next_data(frame_number -1)