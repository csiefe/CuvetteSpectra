# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:23:03 2019

@author: Claire
"""

import pandas as pd
import numpy as np

wavelengths = np.arange(0,100,1)
intensities = wavelengths*2
temp = np.array([20])

df2 = pd.DataFrame({"intensities": intensities})
df3 = pd.DataFrame({"temp": temp})
df1 = pd.DataFrame({"wavelengths": wavelengths})

df = pd.concat([df1,df2,df3], ignore_index = True, axis = 1)
df.to_csv("test3.csv", index = False, header = ["WL", "Int", "temp"])