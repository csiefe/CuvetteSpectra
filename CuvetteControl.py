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

for t in Temp:
    C.set_temp(t)
    temp = C.get_current_temp()
    while t != float(str(temp)[-7:-2]):
        time.sleep(5)
        temp = get_temp()
    
    spectra = plt.figure()
    plt.plot(spec.wavelengths(),spec.intensities())
    #make this plot more readable 
    spectra.set(xlabel = 'Wavelength (nm)', ylabel = 'Intensity (a.u.)', 
                title = "Spectra at temperature {} C".format(t)+r'$^\circ$')
   
def read():
    #The bits sent through the USB end with a ']' instead of a '\n', so we're
    #using that to read until the end of the command
    return ser.read_until(b']')

def get_id():
    ser.write(b'[F1 ID ?]')
    return read()

def set_temp(temp):
    ser.write(bytes('[F1 TT S {}]'.format(temp),'utf-8'))
    

def get_temp():
    ser.write(b'[F1 TT ?]')
    return read()