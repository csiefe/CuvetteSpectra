# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:10:56 2019

@author: Claire
"""


""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import pyqtgraph as pg
from pyqtgraph import PlotWidget

import os
import serial
import time
import seabreeze.spectrometers as sb
import datetime
import pandas as pd
import numpy as np
from Cuvette_Class import Cuvette
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


qtCreatorFile = "CuvetteSpectra_GUI.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow):
    
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #initialize the two instruments
        self.ui.init_spec_button.clicked.connect(self.initSpec)
        self.ui.init_cuvette_button.clicked.connect(self.initCuvette)
<<<<<<< HEAD
        self.ui.plot_button.clicked.connect(self.plotSomething)
        
=======
        self.ui.collect_spectrum_button.clicked.connect(self.collectSpectrum)

>>>>>>> 229278959f38821df363b2a67e66244d1196266c
    def initSpec(self):
        #how do we except 2 different types of error (already connected and not connected at all)
        try:
            spec = sb.Spectrometer.from_serial_number()
            x = 'device was initialized'
            self.ui.logOutput.setText(x)
        except:
            x = 'Device is opened'
            self.ui.logOutput.setText(x)
        
    def initCuvette(self):
        
        try:
            COM_NAME = str(self.ui.comPort.text())
            cuvette = Cuvette.open_from_port(COM_NAME)
            text = "Serial port is being opened"
            self.ui.logOutput.setText(text)
        except:
            COM_NAME = self.ui.comPort.toPlainText()
            self.ui.logOutput.setText('error, either already connected, ComPort was incorrect, or cuvette' +
                                      'holder not connected ' + str(COM_NAME))
<<<<<<< HEAD
    

=======
            
    def collectSpectrum(self):
        data = [0, 1, 2, 3, 4]
        self.ui.spectrumPlot.plot(data, data)
>>>>>>> 229278959f38821df363b2a67e66244d1196266c
        
    def plotSomething(self):
    
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot((np.random.rand(5)))
        self.ui.MplWidget.canvas.draw()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    
