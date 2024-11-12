import sys
from PyQt5 import QtWidgets, uic

from MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog

# Uses the Ui_MainWindow class from the generated file:
# pyuic5 mainwindow.ui -o MainWindow.py



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.labelClod.setText("VOY A MUTARRRRRR")
        self.pushButtonClod.setText("PUSH ME")
        self.pushButtonClod.clicked.connect(self.change_text)

    def openFileDialog(self):
        # Single file selection
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",  # Starting directory
            "All Files (*);;Text Files (*.txt)"
        )
        
        # Multiple file selection
        filenames, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "",
            "All Files (*)"
        )
        
        # Directory selection
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            "",
            QFileDialog.ShowDirsOnly
        )
    
    def change_text(self):
        self.labelClod.setText("Hello World")
        self.openFileDialog(self)
        

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
print(MainWindow.__mro__)
window.show()
app.exec()