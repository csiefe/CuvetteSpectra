# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:10:56 2019
@author: Claire
"""


""

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QObject

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
from Model import Model

global filePath
qtCreatorFile = "CuvetteSpectra_GUI.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QMainWindow):
    
    def __init__(self):
        super(MyApp, self).__init__()
        self.model = Model()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #initialize the two instruments
        self.ui.init_spec_button.clicked.connect(self.initSpec)
        self.ui.init_cuvette_button.clicked.connect(self.initCuvette)
        #Quick spectrum plot
        self.ui.collect_spectrum_button.clicked.connect(self.plotSomething)
        #Temp Series Experiment
        self.ui.start_temp_series_button.clicked.connect(self.tempSeries)
        self.ui.stop_exp_button.setCheckable(True)
        self.ui.stop_exp_button.toggle()
        
        self.ui.stir_button.setCheckable(True)
        self.ui.stir_button.toggle()
        self.ui.stir_button.setStyleSheet("QPushButton { background-color: purple }")
        self.ui.stir_button.clicked.connect(self.stir)
    
        #add file buttons
        self.ui.file_button.clicked.connect(self.browseSlot)
        self.ui.file_lineedit.returnPressed.connect(self.returnPressedSlot)
        self.ui.int_time.returnPressed.connect(self.setIntTime)
    
    def refreshAll( self ):
        '''
        Updates the widgets whenever an interaction happens.
        Typically some interaction takes place, the UI responds,
        and informs the model of the change.  Then this method
        is called, pulling from the model information that is
        updated in the GUI.
        '''
        self.ui.file_lineedit.setText( self.model.getFileName() )
    
    
    def debugPrint(self, msg):
        self.ui.logOutput.setText(msg)
        
    @pyqtSlot()
    def returnPressedSlot(self):
        global filePath
        self.debugPrint("RETURN key Pressed in LineEDIT widget")
        filePath =  self.ui.file_lineedit.text()
        if self.model.isValid(filePath):
            self.model.setFileName( self.lineEdit.text() )
            self.refreshAll()
        else:
            print("invalid file path?")
            m = self.ui.logOutput
            m.setText("Invalid file name!\n" + filePath )
            m.setIcon(QtWidgets.QMessageBox.Warning)
            m.setStandardButtons(QtWidgets.QMessageBox.Ok
                                 | QtWidgets.QMessageBox.Cancel)
            m.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            self.ui.file_lineedit.setText( "" )
            self.refreshAll()
            self.debugPrint( "Invalid file specified: " + filePath  )
            
            
    @pyqtSlot()
    def browseSlot(self):
        global filePath
        self.debugPrint("BrowseButtonPressed")
        ''' Called when the user presses the Browse button
        '''
        #self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filePath = QtWidgets.QFileDialog.getExistingDirectory(
                        None,
                        "Select Directory")
        if filePath:
            self.debugPrint( "setting file name: " + filePath )
            self.model.setFileName( filePath )
            self.refreshAll()

    
    
    
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
        
        
    def setIntTime(self):
        #Set integration time for spectrometer
        try:
            spec.integration_time_micros(float(self.ui.int_time.text())*10**6)
        except:
            self.ui.logOutput.setText('Spectrometer probably not initialized.')
            self.ui.logOutput.setText(str(float(self.ui.int_time.text())*10**6))
        
        
    def initCuvette(self):
        
        try:
            global cuvette
            COM_NAME = str(self.ui.comPort.text())
            cuvette = Cuvette.open_from_port(COM_NAME)
            text = "Serial port is being opened"
            self.ui.logOutput.setText(text) 
            return cuvette
        except:
            COM_NAME = self.ui.comPort.text()
            self.ui.logOutput.setText('error, either already connected, ComPort was incorrect, or cuvette' +
                                      'holder not connected ' + str(COM_NAME))
    
    def stop(self):
        return False
        
    def stir(self):
        if self.ui.stir_button.isChecked():
            cuvette.stir_on()
            self.ui.stir_button.setText("Stir On")
            self.ui.stir_button.setStyleSheet("QPushButton { background-color: blue }")
        else:
            cuvette.stir_off()
            self.ui.stir_button.setText("Stir Off")
            self.ui.stir_button.setStyleSheet("QPushButton { background-color: red }")
            
    def plotSomething(self):
        mask = (spec.wavelengths() > 500) & (spec.wavelengths() < 750)
        wavelengths = spec.wavelengths()[mask]
        intensities = spec.intensities()[mask]
        self.ui.MplWidget.canvas.axes.clear()
        self.ui.MplWidget.canvas.axes.plot(wavelengths, intensities)
        self.ui.MplWidget.canvas.axes.set_xlabel('Wavelength (nm)')
        self.ui.MplWidget.canvas.axes.set_ylabel('Intensity (counts)')
        self.ui.MplWidget.canvas.draw()
        current_temp = cuvette.get_current_temp()
        self.ui.displayCurrentTemp.display(current_temp)
            
    
    def tempSeries(self):
        start_temp = float(self.ui.start_temp_temp_series.text())
        end_temp = float(self.ui.end_temp_temp_series.text())
        temp_int = float(self.ui.temp_int_temp_series.text())
        Temp = np.linspace(start_temp, end_temp, abs((start_temp - end_temp))/temp_int + 1)
        cuvette.temp_control_on()
        name = self.ui.file_name_lineedit.text()
        folderNum = self.ui.file_number_lineedit.text()
        folderNum = int(folderNum)

        folderNum = Model.createExpFolder(name, folderNum, filePath)
        #update GUI with new name
        self.ui.file_number_lineedit.setText(str(folderNum))
        app.processEvents()
        print('filePath is ' + filePath)
        
        spectra_repeat = self.ui.spectra_repeat_num.text()
        spectra_repeat = int(spectra_repeat)
        
        
        for t in Temp:
            self.ui.stop_exp_button.setChecked(False)
            cuvette.set_temp(t)
            self.ui.displaySetTemp.display(t)
            time.sleep(2)
            current_temp = cuvette.get_current_temp()
            self.ui.displayCurrentTemp.display(current_temp)
            status = cuvette.status()
            status_text = str(status[3])
            self.ui.stabilityDisplay.setText(status_text) 
            
            while not status[3]:
                app.processEvents()
                time.sleep(0.1)
                if self.ui.stop_exp_button.isChecked():
                    self.ui.stop_exp_button.setChecked(False)
                    return
               
                current_temp = cuvette.get_current_temp()
                self.ui.displayCurrentTemp.display(current_temp)
                status = cuvette.status()
                status_text = str(status[3])
                self.ui.stabilityDisplay.setText(status_text)
                
            #mask = (spec.wavelengths() > 500) & (spec.wavelengths() < 750)
            #wavelengths = spec.wavelengths()[mask]
            #intensities = spec.intensities()[mask]
            self.plotSomething()
            #check to see if we can click button
            
            
            app.processEvents()
            columnNames = ["temp","wavelengths"]
            df1 = pd.DataFrame({"temp": np.array([t])})
            df2 = pd.DataFrame({"wavelengths": spec.wavelengths()})
            df = pd.concat([df1,df2], ignore_index = True, axis = 1)
            
            for  i in range(spectra_repeat):
                columnNames.append("intensity_{}".format(i))
                dfi = pd.DataFrame({"intensities{}".format(i): spec.intensities()})
                df = pd.concat([df,dfi], ignore_index = True, axis = 1)
            #path = 'C:/Users/Chris/Documents/Dionne Group/Lab Software/CuvetteSpectra/CuvetteSpectra/data/'
            #path = 'C:/Users/Claire/Documents/Postdoc/CuvetteSpectra/data/'
            
            df.to_csv(filePath + "/" + name + str(folderNum) +"/spectra{}.csv".format(t), index = False, header = columnNames)
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
    