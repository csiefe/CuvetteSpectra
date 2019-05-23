# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:00:49 2019
Simple control code for Cuvette holder and ocean optics. We input a temperature
range and integration time

@author: Claire
"""
import os
import serial
import time
import seabreeze.spectrometers as sb
from matplotlib import pyplot as plt
plt.rcParams.update({'font.size': 22})
import datetime
import pandas as pd
import numpy as np
from Cuvette_Class import Cuvette
#May need to change port name, look up in Device Manager on Windows
COM_NAME = 'COM5'


#Create a folder for the day if it doesn't exist
#%%
#fileLocation = 'C:/Users/Claire/Documents/PostDoc/CuvetteSpectra/data/'
fileLocation = 'C:/Users/Chris/Documents/Dionne Group/Lab Software/CuvetteSpectra/CuvetteSpectra/data/'
date = datetime.datetime.now().strftime("%Y%m%d")
while not os.path.isdir(fileLocation + date):
    os.mkdir(fileLocation+date)

#Create an experiment (next in line)

expNum = 0
#%%
ExpNamePrefix = 'exp'
ExpName = ExpNamePrefix + '_{}'.format(expNum)
#%%

while not os.path.isdir(fileLocation + date + '/' + ExpName + '/'):
    
    ExpName = ExpNamePrefix + '_{}'.format(expNum)
    
    exists = os.path.isdir(fileLocation + date + '/' + ExpName + '/')


    path = fileLocation + date + '/' + ExpName + '/'

    os.mkdir(path)
    expNum = expNum+1
#%%
#Create a metafile
dataFile = open(path+'metaData.csv',"w+")

now = datetime.datetime.now()
#write meta data
sample = 'sample'
dataFile.write(now.strftime("%Y-%m-%d %H:%M")+'\n')
dataFile.write(sample + '\n')
dataFile.close()
#%%

#Create running experiment

try:
    C = Cuvette.open_from_port(COM_NAME)
    print("Serial port is being opened")
except:
    print("serial port was initiated")
#%%

try:
    spec = sb.Spectrometer.from_serial_number()
except:
    'Device is opened'
intTime = 20000
spec.integration_time_micros(20000)
#%%
#Goal is to sweeep through temperatures and plot spectra

Temp = [19, 20, 21]
C.temp_control_on()

for t in Temp:
    C.set_temp(t)
    temp = C.get_current_temp()
    while t != temp:
        time.sleep(5)
        temp = C.get_current_temp()
        print(temp)

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
    