import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QDialogButtonBox, QVBoxLayout, QLabel

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel 

        # You could of course choose to ignore this and use a standard QButton in a layout, but the approach outlined here ensures that your dialog respects the host desktop standards (OK on left vs. right for example). 
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        """
        Constructor for the main window.

        This constructor sets up the main window with a toolbar, a status bar, a
        central widget and a menu bar. The toolbar has 3 buttons that are also
        available from the menu bar. The buttons are toggle buttons. The
        application quits when the user clicks the "File" -> "Exit" menu item or
        presses Ctrl+Q.

        :return: None
        """
        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("click", s)

        # dlg = QDialog(self)
        # dlg.setWindowTitle("HELLO!")
        # dlg.exec()

        #dlg = CustomDialog() # Positions the dialog in the center of the screen
        dlg = CustomDialog(self) # Positions the dialog in the center of the window
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
