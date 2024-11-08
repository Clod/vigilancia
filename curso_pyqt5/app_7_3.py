from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from random import randint
import sys


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window % d" % randint(0,100))
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.w = None
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, checked):
        # self is necessary to keep the window alive
        # once the function returns (if it were a local 
        # variable it would be destroyed)
        # Toggle the window
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()
        else:
            self.w.close() # Close the window
            self.w = None # Discard the reference


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()