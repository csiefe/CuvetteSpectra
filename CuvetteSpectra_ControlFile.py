# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:10:56 2019
@author: Claire
"""


""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

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
        #Quick spectrum plot
        self.ui.collect_spectrum_button.clicked.connect(self.plotSomething)
        #Temp Series Experiment
        self.ui.start_temp_series_button.clicked.connect(self.tempSeries)
        
        
    def initSpec(self):
        #how do we except 2 different types of error (already connected and not connected at all)
        try:
            global spec
            spec = sb.Spectrometer.from_serial_number()
            x = 'device was initialized'
            self.ui.logOutput.setText(x)
            return spec
        except:
            x = 'Device is opened'
            self.ui.logOutput.setText(x)
        
    def initCuvette(self):
        
        try:
            global cuvette
            COM_NAME = str(self.ui.comPort.text())
            cuvette = Cuvette.open_from_port(COM_NAME)
            text = "Serial port is being opened"
            self.ui.logOutput.setText(text) 
            return cuvette
        except:
            COM_NAME = self.ui.comPort.toPlainText()
            self.ui.logOutput.setText('error, either already connected, ComPort was incorrect, or cuvette' +
                                      'holder not connected ' + str(COM_NAME))

    def plotSomething(self):
        wavelengths = spec.wavelengths()
        intensities = spec.intensities()
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(wavelengths, intensities)
        self.ui.MplWidget.canvas.axes.set_xlabel('Wavelength (nm)')
        self.ui.MplWidget.canvas.axes.set_ylabel('Intensity (counts)')
        self.ui.MplWidget.canvas.draw()
        current_temp = cuvette.get_current_temp()
        self.ui.displayCurrentTemp.display(current_temp)
            
    
    def tempSeries(self):
        start_temp = self.ui.start_temp_temp_series.value()
        end_temp = self.ui.end_temp_temp_series.value()
        temp_int = self.ui.temp_int_temp_series.value()
        Temp = np.arange(start_temp, end_temp, temp_int)
        cuvette.temp_control_on()

        for t in Temp:
            cuvette.set_temp(t)
            current_temp = cuvette.get_current_temp()
            self.ui.displayCurrentTemp.display(current_temp)
            
            while t != temp:
                time.sleep(5)
                temp = cuvette.get_current_temp()


    #spectra = plt.figure()
    wavelengths = spec.wavelengths()
    intensities = spec.intensities()
    #make this plot more readable 
    #spectra.set(xlabel = 'Wavelength (nm)', ylabel = 'Intensity (a.u.)', 
                #title = "Spectra at temperature {} C".format(t)+r'$^\circ$')
    df2 = pd.DataFrame({"intensities": intensities})
    df3 = pd.DataFrame({"temp": np.array([t])})
    df1 = pd.DataFrame({"wavelengths": wavelengths})
    df = pd.concat([df1,df2,df3], ignore_index = True, axis = 1)
    df.to_csv(path + "test{}.csv".format(t), index = False, header = ["WL", "Int", "temp"])
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    