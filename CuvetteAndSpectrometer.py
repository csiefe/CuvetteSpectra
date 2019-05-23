# -*- coding: utf-8 -*-
"""
Created on Wed May 15 14:24:53 2019

@author: Claire
"""

import CuvetteControl as CC
import seabreeze.spectrometers as sb
import time

#initialize spectrometer and set integration time
try:
    spec = sb.Spectrometer.from_serial_number()
except:
    'Device is opened'
intTime = 20000
spec.integration_time_micros(20000)

#Goal is to sweeep through temperatures and plot spectra

Temp = [19, 20, 21]

for t in Temp:
    CC.set_temp(t)
    temp = get_temp()
    while t != float(str(temp)[-7:-2]):
        time.sleep(5)
        temp = CC.get_temp()
    
    spectra = plt.figure()
    plt.plot(spec.wavelengths(),spec.intensities())
    spectra.title("Spectra at temperature {} C".format(t))
