# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:00:49 2019

@author: Claire
"""

import serial

COM_PORT = 'com3'
ser = serial.Serial(COM_PORT)

ser.baudrate = 19200
ser.timeout = 5

def read():
    return ser.read_until(b']')


def get_id():
    ser.write(b'[F1 ID ?]')
    return read()