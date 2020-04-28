

import math
import sys
import time
import threading

# Import QApplication and the required widgets from PyQt5.QtWidgets

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QWidget

__version__ = "0.1"
__author__ = ""

# Create a subclass of QMainWindow to setup the application's GUI
class MainWindow(QMainWindow):

    def __init__(self, count):
        super().__init__()
        self.labels = []
        self.setWindowTitle("Cams Capturing")
        self.__createLabels(count)
        self.__createToolbar()
        self.capturing = True
        self.stop = False
        
        ag = QDesktopWidget().availableGeometry()
        self.resize(ag.size() * 0.85);

        
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


    def closeEvent(self, event):
        self.capturing = False
        
    def __createLabels(self, count):        
        for i in range(count):
            self.labels.append(QLabel())
            self.labels[i].setStyleSheet("QLabel { background-color : gray}");

        root = math.sqrt(count)        
        cols = math.trunc(root)
        cols += 1        
        
        layout = QGridLayout()
        n = 0
        for i in range(cols):
            for j in range(cols):
                layout.addWidget(self.labels[n], i, j, 1, 1)
                n += 1
                if n == count: break
            if n == count: break
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
                           
        

    def __createToolbar(self):
        self.buttons = {}
        
        toolbar = QToolBar("bottom toolbar");        
        toolbar.setOrientation(Qt.Horizontal);
        toolbar.setAllowedAreas(Qt.BottomToolBarArea);
        toolbar.setIconSize(QSize(32, 32));
        
        button1 = QPushButton("Show All");
        toolbar.addWidget(button1);        
        toolbar.addSeparator()        
        
        button2 = QPushButton("Play");
        toolbar.addWidget(button2);
        toolbar.addSeparator()
        
        button3 = QPushButton("Stop");
        toolbar.addWidget(button3);
        toolbar.addSeparator()
        
        button4 = QPushButton("Record");
        toolbar.addWidget(button4);
        toolbar.addSeparator()
        
        self.addToolBar(Qt.BottomToolBarArea, toolbar);

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MainWindow(1)
    view.show()
    
    sys.exit(app.exec_())
    
    
