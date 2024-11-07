import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
    
        # button = QPushButton("Press Me!")
        # button.setCheckable(True)
        # button.clicked.connect(self.the_button_was_clicked)
        self.button_is_checked = True

        self.button = QPushButton("Press Me!")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.the_button_was_clicked)
        self.button.clicked.connect(self.the_button_was_toggled)
        # Set the initial toggle state
        self.button.setChecked(self.button_is_checked)

        self.button.released.connect(self.the_button_was_released)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        print("Clicked!")
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)

        # Also change the window title.
        self.setWindowTitle("My Oneshot App")

    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked
        print("Checked?", checked)

    def the_button_was_released(self):
        # The release event does not send the checked state
        self.button_is_checked = self.button.isChecked()



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()