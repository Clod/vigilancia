import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QApplication, QLabel, QMainWindow, QMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, e):
        """
        Override the default context menu event to display a custom context menu with actions.

        This method creates a QMenu with several QAction items and displays it at the
        global position of the mouse event.

        Args:
            e (QContextMenuEvent): The event object containing details about the context menu event.
        """
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        # context.triggered.connect(lambda action: print(action.text()))
        context.triggered.connect(self.contextMenuHandler) 
        
        context.exec(e.globalPos())

    def contextMenuHandler(self, e):
        print("Option selected:", e.text())


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()