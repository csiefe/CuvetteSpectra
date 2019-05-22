# -*- coding: utf-8 -*-
"""
Created on Thu May 16 17:36:28 2019
Define class for control of cuvette holder.
This class includes all commands outlined in 
the manual for the qpod 2e: Temperature-Controlled
Sample Compartment for Fiber Optic Spectroscopy
from Quantum Northwest, Inc.

@author: Chris
"""
import serial

class Cuvette():
    #This needs to be checked. Make sure that I'm using __init__() correctly.
    def __init__(self, ser):
        #Create attribute for serial port
        self.ser = ser
        self.ser.baudrate = 19200
        self.ser.timeout = 5
        
    def open_from_port(cls, COM_name):
        ser = serial.Serial(COM_PORT)
        return cls(ser = ser)
        
    def read(self):
        #The bits sent through the USB end with a ']' instead of a '\n', so we're
        #using that to read until the end of the command
        return self.ser.read_until(b']')
        
    def get_id(self):
        self.ser.write(b'[F1 ID ?]')
        output = self.read().decode("utf-8")
        print("Sample Holder ID Number: " + str(output[7:-1]))
    
    def get_software_version(self):
        self.ser.write(b'[F1 VN ?]')
        output = self.read().decode("utf-8")
        print("Software Version Number: " + str(output[7:-1]))
        
    def stir_on(self):
        self.ser.write(b'[F1 SS +]')
        print("Stirring on.")
        
    def stir_off(self):
        self.ser.write(b'[F1 SS -]')
        print("Stirring off.")
        
    def temp_control_on(self):
        self.ser.write(b'[F1 TC +]')
        print("Temperature Control enabled.")
    
    def temp_control_off(self):
        self.ser.write(b'[F1 TC i]')
        print("Temperature Control disabled.")
        
    def set_temp(self, temp):
        self.ser.write(bytes('[F1 TT S {}]'.format(temp),'utf-8'))
        
    def get_set_temp(self):
        self.ser.write(b'[F1 TT ?]')
        output = self.read().decode("utf-8")
        return float(output[7:-1])
    
    #def auto_report_temp_on(self):
    
    #def auto_report_temp_off(self):
    
    def status(self):
        self.ser.write(b'[F1 IS ?]')
        output = self.read().decode("utf-8")
        num_errors = int(output[7:8])
        if output[8:9] == '+':
            stir_status = True
        else:
            stir_status = False
        if output[9:10] == '+':
            temp_control_status = True
        else:
            temp_control_status = False 
        if output[10:11] == 'S':
            temp_stability = True
        else:
            temp_stability = False
        return num_errors, stir_status, temp_control_status, temp_stability
        
        