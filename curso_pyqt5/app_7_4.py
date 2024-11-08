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
        # Persistent window
        self.w = AnotherWindow()
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)
        # Set handler for window close event
        self.closeEvent = self.closeEvent
        

    def closeEvent(self, event):
        print("Close event")
        # Delete the window and set the reference to None
        self.w.deleteLater()

    def show_new_window(self, checked):
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()