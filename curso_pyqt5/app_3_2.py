import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        # LABEL CON TEXTO
        # widget = QLabel("Hello")
        # # if you want to change the properties of a widget font it is usually 
        # # better to get the current font, update it, and then apply it back. 
        # # This ensures the font face remains in keeping with the desktop 
        # # conventions.
        # font = widget.font()
        # font.setPointSize(30)
        # widget.setFont(font)
        # widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.setCentralWidget(widget)

        # LABEL CON IMAGEN
        # widget1 = QLabel()
        # pixmap = QPixmap("otje.webp")
        # if pixmap.isNull():
        #     print("Image file not found or invalid.")
        # else:
        #     widget1.setPixmap(pixmap)
        # widget1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # # Estira la imagen para que se ajuste al tamaño de la ventana
        # widget1.setScaledContents(True) 
        # self.setCentralWidget(widget1)

        widget = QCheckBox()
        widget.setCheckState(Qt.Checked)

        # For tristate: widget.setCheckState(Qt.PartiallyChecked)
        # Or: widget.setTriState(True)
        widget.stateChanged.connect(self.show_state)
        widget.setText("Hello")

        self.setCentralWidget(widget)

    def show_state(self, s):
        print(s == Qt.Checked)
        print(s)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()