import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar,
    QCheckBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Awesome App")

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        # Set toolbar icon size
        toolbar.setIconSize(QSize(16,16))
        # Add toolbar to the window
        self.addToolBar(toolbar)

        # Set toolbar button style
        # Qt.ToolButtonTextOnly	        Text only, no icon
        # Qt.ToolButtonTextBesideIcon	Icon and text, with text beside the icon
        # Qt.ToolButtonTextUnderIcon	Icon and text, with text under the icon
        # Qt.ToolButtonFollowStyle	    Follow the host desktop style
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # Toolbar is not movable
        toolbar.setMovable(False)

        button_action = QAction(QIcon("bug.png"), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        # Button acts as toggle
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("burn.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addSeparator()

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        # Add a status bar
        self.setStatusBar(QStatusBar(self))


    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
