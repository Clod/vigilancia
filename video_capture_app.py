# Note: This script should be executed in the opencv_pyqt5 environment

# Import required libraries
# sys for system-specific parameters and functions
import sys
# OpenCV for video capture and image processing
import cv2
# PyQt5 widgets for creating the graphical user interface
from PyQt5.QtWidgets import (
    QApplication,   # Manages the GUI application's control flow and main settings
    QMainWindow,    # Main application window
    QLabel,         # Widget for displaying text or images
    QPushButton,    # Clickable button widget
    QVBoxLayout,    # Vertical layout for arranging widgets
    QWidget         # Base class for all user interface objects
)
# PyQt5 GUI-related modules for image and pixel manipulation
from PyQt5.QtGui import QImage, QPixmap
# PyQt5 core module for core non-GUI functionality
from PyQt5.QtCore import Qt, QTimer
# Main application class for video capture
class VideoCapture(QMainWindow):
    def __init__(self):
        # Call the parent class's __init__ method
        super().__init__()
        
        # Set the window title and initial geometry
        self.setWindowTitle("Video Capture App")
        # Position the window at (100, 100) with width 800 and height 600
        self.setGeometry(100, 100, 800, 600)

        # Create a vertical layout to organize widgets
        self.main_layout = QVBoxLayout()

        # Create a label to display video frames
        self.video_label = QLabel()
        # Center-align the video label within its container
        self.video_label.setAlignment(Qt.AlignCenter)
        # Add the video label to the main layout
        self.main_layout.addWidget(self.video_label)

        # Create a button to start/stop video capture
        self.toggle_button = QPushButton("Start Video")
        # Connect the button's click event to the toggle_video method
        self.toggle_button.clicked.connect(self.toggle_video)
        # Add the toggle button to the main layout
        self.main_layout.addWidget(self.toggle_button)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Initialize video capture from the default camera (index 0)
        self.cap = cv2.VideoCapture(0)
        
        # Create a timer to periodically update video frames
        self.timer = QTimer()
        # Connect the timer's timeout signal to the update_frame method
        self.timer.timeout.connect(self.update_frame)

        # Flag to track video capture state
        self.is_video_running = False
    # Method to toggle video capture on and off
    def toggle_video(self):
        """
        Start or stop video capture based on current state.
        
        If video is not running:
        - Start the timer to update frames every 30 ms
        - Change button text to "Stop Video"
        
        If video is running:
        - Stop the timer
        - Change button text to "Start Video"
        """
        if not self.is_video_running:
            # Start updating frames every 30 milliseconds
            self.timer.start(30)
            self.toggle_button.setText("Stop Video")
        else:
            # Stop updating frames
            self.timer.stop()
            self.toggle_button.setText("Start Video")
        
        # Toggle the video running state
        self.is_video_running = not self.is_video_running

    # Method to update video frame in the label
    def update_frame(self):
        """
        Read a frame from the video capture device and display it.
        
        Converts the frame from BGR to RGB color space and 
        displays it in the video label using QImage and QPixmap.
        """
        # Read a frame from the video capture device
        ret, frame = self.cap.read()
        
        # Check if frame was successfully read
        if ret:
            # Convert frame from BGR (OpenCV default) to RGB color space
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get frame dimensions
            h, w, c = frame.shape
            
            # Create a QImage from the frame data
            # Parameters: data, width, height, bytes per line, image format
            qimg = QImage(frame.data, w, h, w * c, QImage.Format_RGB888)
            
            # Convert QImage to QPixmap for display
            pixmap = QPixmap.fromImage(qimg)
            
            # Set the pixmap in the video label
            self.video_label.setPixmap(pixmap)
# Main entry point of the script
if __name__ == "__main__":
    # Create the Qt application
    app = QApplication(sys.argv)
    
    # Create the video capture window
    window = VideoCapture()
    
    # Show the window
    window.show()
    
    # Start the application's event loop
    # sys.exit ensures a clean exit when the application is closed
    sys.exit(app.exec_())
