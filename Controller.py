
import sys
import time
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication

import MainWindow as mw
import OpenCV as ocv

class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.threads = []
        
    def convert(self, cvImg, qSize):
        height, width, _ = cvImg.shape
        bytesPerLine = 3 * width
        qImage = QImage(cvImg.data, width, height, bytesPerLine, 
                                            QImage.Format_RGB888)
        qImage = qImage.scaled(qSize.width(), qSize.height(), 
                                Qt.KeepAspectRatio)
        qPixmap = QPixmap.fromImage(qImage)
        return qPixmap

    def grabImages(self, id):        
        b = self.model[id].init(id)
        if not b: return
               
        while self.view.capturing:
            if not self.view.stop:
                qsize = self.view.labels[id].size()
                frame = model[id].getFrame()
                newFrame = model[id].processFrame(frame)                          
                qpix = self.convert(newFrame, qsize)
                self.view.labels[id].setPixmap(qpix)
                
            time.sleep(50 / 1000.0)
        
        self.model[id].free()
        
    def start(self, id):
            thread = threading.Thread(target=self.grabImages, args=[id])
            self.threads.append(thread)
            self.threads[-1].start()

    def waitAll(self):
        i = 0
        for thread in self.threads:
            thread.join();
            i += 1
            print("finish:" + std(i))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    count = ocv.OpenCV().getDeviceCount();
    
    view = mw.MainWindow(count)
    view.show()
    
    model = []
    
    for i in range(count):
        obcv = ocv.OpenCV()
        model.append(obcv)
    
    controller = Controller(model, view)
    
    for i in range(count):
        controller.start(i)
    
    sys.exit(app.exec_())
    
    
    
