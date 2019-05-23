# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:31:27 2019
Testing if I can find a file and create a new one if it exists already
@author: Claire
"""
import os
import datetime

# class dataFile(object):
    
#     def __init__(self, fileNamePrefix = 'exp', fileLoc, metaData = ''):
        
#         exists = os.path.isfile(fileLoc+fileName+ '.csv')
#         while exists:
#             i = i+1
#             fileName = fileNamePrefix + '_{}'.format(i)
        
#             exists = os.path.isfile(fileLoc+fileName+ '.csv')

#         self.file = open(fileLoc + filename + '.csv')
#         self.file.write(metaData)
    
#     def appendData():
        
#         self.file.write()
        
    
now = datetime.datetime.now()
sample = 'sample'

fileLocation = "C:/Users/Claire/Documents/PostDoc/CuvetteSpectra/Data/"
#enter location of where data should be saved
i = 0
fileNamePrefix = 'Exp' #change this to a useful file name
fileName = fileNamePrefix + '_{}'.format(i)
#create a new file for the experiment
exists = os.path.isfile(fileLocation+fileName+ '.csv')
print(exists)
while exists:
    print(i)
    print(exists)
    i = i+1
    fileName = fileNamePrefix + '_{}'.format(i)
        
    exists = os.path.isfile(fileLocation+fileName+ '.csv')

dataFile = open(fileLocation+fileName+'.csv',"w+")

#write meta data
dataFile.write(now.strftime("%Y-%m-%d %H:%M")+'\n')
dataFile.write(sample + '\n')
dataFile.close()

