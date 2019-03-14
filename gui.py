import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import\
(QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QGroupBox, QLabel, QComboBox, QSlider)
from PyQt5.QtGui import QIcon, QPixmap


class SegementationApp(QWidget):
    def __init__(self, path):
        super(SegementationApp, self).__init__()
        self.workImagePath  = path 
        self.initUI()

        
    def createSlider(self, name, min, max):
        sliderBox = QGroupBox(name)
        vbox = QVBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(1)
        slider.setSingleStep(1) 
        slider.setRange(min, max) 
        vbox.addWidget(slider)
        sliderBox.setLayout(vbox)

        return sliderBox

    def createCropBox(self):
        group = QGroupBox("Cropped Image")
        vbox = QVBoxLayout()
        cropPreviewPic = QLabel(self)
        cropPreviewPic.setPixmap(QPixmap('./data/no_image.png').scaled(600, 256))        
        vbox.addWidget(cropPreviewPic)
        group.setLayout(vbox)        
        return group
        
    def initUI(self):
        autoCropButton = QPushButton("Atuo Crop")
        confirmButton = QPushButton("Confirm")
        cancelButton = QPushButton("Cancel")
        setButton = QPushButton("Set")

        self.filterMethods = ["laplacian"]

        # image preview
        previewPic = QLabel(self)
        previewPic.setPixmap(QPixmap('./data/no_image.png').scaled(255,255))
        
        # control layout -- horizontal
        controlLayout = QVBoxLayout()
        controlLayout.addWidget(self.createSlider("Threshold",-1.0 ,1.0))
        controlLayout.addWidget(self.createSlider("Filter Size", 0, 1.0))
        controlLayout.addWidget(self.createSlider("Exponent", 1, 15))
        
        firstRow = QHBoxLayout()
        firstRow.addWidget(previewPic)
        firstRow.addLayout(controlLayout)

        secondRow = QHBoxLayout()
        secondRow.addWidget(self.createCropBox())

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(setButton)
        hbox.addWidget(autoCropButton)
        hbox.addWidget(cancelButton)
        hbox.addWidget(confirmButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(firstRow)
        vbox.addLayout(secondRow)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Buttons')    
        self.show()

import argparse
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', help='image to work on')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    ex = SegementationApp(args.image)
    sys.exit(app.exec_())