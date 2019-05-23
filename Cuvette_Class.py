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
    
    @classmethod
    def open_from_port(cls, COM_name):
        ser = serial.Serial(COM_name)
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
    
    def auto_report_temp_on(self):
        self.ser.write(b'[F1 TT +]')
        print("Automatic reporting of temperature changes turned on.")
    
    def auto_report_temp_off(self):
        self.ser.write(b'[F1 TT -]')
        print("Automatic reporting of temperature changes turned off.")
    
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
    
    def auto_report_status_on(self):
        self.ser.write(b'[F1 IS +]')
        print("Automatic reporting of instrument status turned on.")
    
    def auto_report_status_off(self):
        self.ser.write(b'[F1 IS -]')
        output = self.read().decode("utf-8")
        print("Automatic reporting of instrument status turned off.")  
        
    def get_current_temp(self):
        self.ser.write(b'[F1 CT ?]')
        output = self.read().decode("utf-8")
        return float(output[7:-1])
    
    def auto_report_current_temp_on(self, time=3):
        #time in seconds
        self.ser.write(bytes('[F1 CT +{}]'.format(time),'utf-8'))
        print("Automatic reporting of current temperature every {} seconds.".format(time))
        
    def auto_report_current_temp_off(self):
        self.ser.write(b'[F1 CT -]')
        print("Automatic reporting of current temperature turned off.")
        
    def check_external_prove(self):
        self.ser.write(b'[F1 PS ?]')
        output = self.read().decode("utf-8")
        if output[7:8] == '+':
            print("An external temperature probe is connected.")
        elif output[7:8] == '-':
            print("No external temperature probe is connected.")
    
    def auto_report_probe_connection_on(self):
        self.ser.write(b'[F1 PS +]')
        print("Probe status will automatically be reported when changed.")
        
    def auto_report_probe_connection_off(self):
        self.ser.write(b'[F1 PS -]')
        print("Probe status will not automatically be reported when changed.")  
        
    def get_current_probe_temp(self):
        self.ser.write(b'[F1 PT ?]')
        output = self.read().decode("utf-8")
        return float(output[7:-1])
    
    def auto_report_current_probe_temp_on(self, time=3):
        #time in seconds
        self.ser.write(bytes('[F1 PT +{}]'.format(time),'utf-8'))
        print("Automatic reporting of current probe temperature every {} seconds.".format(time))
        output = self.read().decode("utf-8")
        if output[7:-1].isdigit():
            return float(output[7:-1])
        else:
            print("Probe temperature not available.")
            
    def auto_report_current_probe_temp_off(self):
        self.ser.write(b'[F1 PT -]')
        print("Automatic reporting of current probe temperature disabled.")
        
    def auto_report_probe_temp_incrementally(self, increment=0.5):
        #Increment must be a positive value without sign in tenths between 0.1
        #and 9.9 degrees and will work for ramps going up or down.
        self.ser.write(bytes('[F1 PA S {}]'.format(increment),'utf-8'))
        print("Automatic reporting of current probe temperature every {} degrees.".format(increment))
        
    def auto_report_probe_temp_incrementally_on(self):
        self.ser.write(b'[F1 PA +]')
        print("Automatic reporting of current probe temperature enabled.")
        output = self.read().decode("utf-8")
        return float(output[7:-1])
          
    def auto_report_probe_temp_incrementally_off(self):
        self.ser.write(b'[F1 PA -]')
        print("Automatic reporting of current probe temperature disabled.")
          
    def increase_probe_temp_precision(self):
        #Increase probe temperature probe precision to 0.01 degree
        self.ser.write(b'[F1 PX +]')
        print("Probe temperature precision changed to 0.01 degrees.")
    
    def check_error(self):
        self.ser.write(b'[F1 ER ?]')
        output = self.read().decode("utf-8")
        error = output[7:-1]
        if error == '-1':
            print("No current error.")
        elif error == '05':
            print("Cell temperature out of range.")
        elif error == '06':
            print("Cell and heat exchanger temperature out of range.")
        elif error == '07':
            print("Heat exchanger temperature out of range.")
        elif error == '08':
            print("Inadequate coolant (check flow). Control shut down.")
        elif error == '09':
            print("Syntax error on previous command.")
            
    def auto_report_error_on(self):
        self.ser.write(b'[F1 ER +]')
        print("Automatic reporting of errors turned on.")
        
    def auto_report_error_off(self):
        self.ser.write(b'[F1 ER -]')
        print("Automatic reporting of errors turned off.")
        
    def set_ramp_time_increment(self, increment=1):
        #Increment time in seconds, must be positive
        self.ser.write(bytes('[F1 RS S {}]'.format(increment),'utf-8'))
        print("Ramp time increment set to {} seconds.".format(increment))
        
    def set_ramp_temp_increment(self, increment=0.1):
        #Temperature increment in degrees, command reads hundredths of degrees
        temp_increment = increment * 100 
        self.ser.write(bytes('[F1 RT S {}]'.format(temp_increment),'utf-8'))
        print("Ramp temperature increment set to {} degrees.".format(increment))
    
    