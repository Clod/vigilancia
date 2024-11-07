from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtCore import QSize
# Only needed for access to command line arguments
import sys


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() # ALWAYS call the base class init

        self.setWindowTitle("My App")
        button = QPushButton("Press Me!")

        # self.setFixedSize(QSize(400, 300)) # For a fixed size

        self.setMinimumSize(QSize(200, 100))
        self.setMaximumSize(QSize(800, 600))

        # Set the central widget of the Window.
        self.setCentralWidget(button)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
# window = QWidget()
# window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# window1 = QPushButton("Push Me")
# window1.show()

# window2 = QMainWindow()
# window2.show()

window3 = MainWindow()
window3.show()

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.

