# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:00:49 2019

@author: Claire
"""

import serial

#May need to change port name, look up in Device Manager on Windows
COM_PORT = 'com5'
ser = serial.Serial(COM_PORT)

#Baudrate is the rate at which information is being transferred through the USB
ser.baudrate = 19200
#Timeout forces the program to stop if nothing happens after 5 seconds.
ser.timeout = 5

def read():
    #The bits sent through the USB end with a ']' instead of a '\n', so we're
    #using that to read until the end of the command
    return ser.read_until(b']')


def get_id():
    ser.write(b'[F1 ID ?]')
    return read()

def set_temp(temp):
    #command = '[F1 TT S ' + str(temp) + ']'
    #ser.write(bytes(command, 'utf-8'))
    ser.write(b'[F1 TT S 20.00]')
    ser.write(b'[F1 TT ?]')
    return read()