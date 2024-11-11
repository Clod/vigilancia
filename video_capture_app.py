# Ejecutarlo en env opencv_pyqt5
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer

class VideoCapture(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Capture App")
        self.setGeometry(100, 100, 800, 600)

        # Create the main layout
        self.main_layout = QVBoxLayout()

        # Create the video display label
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.video_label)

        # Create the toggle button
        self.toggle_button = QPushButton("Start Video")
        self.toggle_button.clicked.connect(self.toggle_video)
        self.main_layout.addWidget(self.toggle_button)

        # Create the central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Initialize the video capture
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.is_video_running = False

    def toggle_video(self):
        if not self.is_video_running:
            self.timer.start(30)
            self.toggle_button.setText("Stop Video")
        else:
            self.timer.stop()
            self.toggle_button.setText("Start Video")
        self.is_video_running = not self.is_video_running

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to a QImage and display it
            h, w, c = frame.shape
            qimg = QImage(frame.data, w, h, w * c, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.video_label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoCapture()
    window.show()
    sys.exit(app.exec_())
