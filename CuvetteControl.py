# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:00:49 2019
Simple control code for Cuvette holder and ocean optics. We input a temperature
range and integration time

@author: Claire
"""

import serial
import time
from matplotlib import pyplot as plt
import time

#May need to change port name, look up in Device Manager on Windows

try:
    
    COM_PORT = 'com3'
    ser = serial.Serial(COM_PORT)

    #Baudrate is the rate at which information is being transferred through the USB
    ser.baudrate = 19200
    #Timeout forces the program to stop if nothing happens after 5 seconds.
    ser.timeout = 5
    print("Serial port is being opened")
except:
    print("serial port was initiated")


try:
    spec = sb.Spectrometer.from_serial_number()
except:
    'Device is opened'
intTime = 20000
spec.integration_time_micros(20000)

#Goal is to sweeep through temperatures and plot spectra

Temp = [19, 20, 21]

for t in Temp:
    set_temp(t)
    temp = get_temp()
    while t != float(str(temp)[-7:-2]):
        time.sleep(5)
        temp = get_temp()
    
    spectra = plt.figure()
    plt.plot(spec.wavelengths(),spec.intensities())
    spectra.suptitle("Spectra at temperature {} C".format(t))

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