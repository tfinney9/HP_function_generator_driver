#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 15:17:30 2022

@author: tfinney

translate to function generator language for HP33120A

Based on qtlab stuff
https://github.com/heeres/qtlab
# HP_33120A.py class, to perform the communication between the Wrapper and the device
# Pieter de Groot <pieterdegroot@gmail.com>, 2008
"""


import logging
from instrument import dummy_instrument as instrument
import serial

class HP33120A(instrument):
    def __init__(self, com_port = 'COM1', baud_rate = 9600,  byte_size = serial.EIGHTBITS, 
                 parity = serial.PARITY_NONE, timeout = 5, debug = True):

        #initialize instrument with parameters
        super().__init__(com_port = com_port, baud_rate = baud_rate, byte_size = byte_size, 
                         parity = parity, timeout = timeout)

        
        # pass
    
    def get_trigger_state(self):
        """
        I have no need for this 
        trigger stuff right now
        """
        self.ask('TRIG:SOUR?')

    def connect(self):
        self.write('SYST:REM')

    def reset(self):
        self.write('*RST')

    def get_error(self):
        self.ask('SYST:ERR?')

    #function shape
    def set_function(self, shape):
        """
        sine, square, Triangle, other that I'm not going to use
        shape : { SIN, SQU, TRI, RAMP, NOIS, DC, USER }

        """
        self.write('SOUR:FUNC:SHAP %s' % shape)

    def get_function_shape(self):
        self.ask('SOUR:FUNC:SHAP?')

    #frequency
    def set_frequency(self, freq):
        """
        in Hz
        """
        self.write('SOUR:FREQ %f' % freq)
        
    def get_frequency(self):
        self.ask('SOUR:FREQ?')
    
    #function amplitude
    def set_amplitude(self, amp):
        """
        in volts
        """
        self.write('SOUR:VOLT %f' % amp)    
    
    def get_amplitude(self):
      self.ask('SOUR:VOLT?')      
    
    #offset, even though i don't need this
    #no intention of adding this to GUI
    def set_offset(self, offset):
        self.write('SOUR:VOLT:OFFS %f' % offset)
    
    def get_offset(self):
        self.ask('SOUR:VOLT:OFFS?')
    



if __name__ == "__main__":
    test = HP33120A(com_port = '/dev/ttyUSB1')