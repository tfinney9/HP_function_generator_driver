#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 15:17:30 2022

@author: tfinney

translate to function generator language for HP3325B

Based on qtlab stuff
https://github.com/heeres/qtlab
# HP_33120A.py class, to perform the communication between the Wrapper and the device
# Pieter de Groot <pieterdegroot@gmail.com>, 2008
# HP_3325B.py class, to perform the communication between the Wrapper and the device
# Gabriele de Boo <ggdeboo@gmail.com> 2014
"""


import logging
from instrument import dummy_instrument as instrument
import serial

class HP3325B(instrument):
    def __init__(self, com_port = 'COM1', baud_rate = 300,  byte_size = serial.SEVENBITS, 
                 parity = serial.PARITY_EVEN, timeout = 5, debug = True):

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
        self.write('Not Yet Implemented!')

    def reset(self):
        self.write('*RST')

    #function shape
    def set_function(self, function):
        """
        sine, square, Triangle, other that I'm not going to use
        """
        # self.write('SOUR:FUNC:SHAP %s' % shape)
        if function == 'DC':
            self.write('FU0')
        if function == 'SINE':
            self.write('FU1')
        if function == 'SQUARE':
            self.write('FU2')
        if function == 'TRIANGLE':
            self.write('FU3')
        if function == 'POSITIVE RAMP':
            self.write('FU4')
        if function == 'NEGATIVE RAMP':
            self.write('FU5')

    def get_function_shape(self):
        # self.ask('SOUR:FUNC:SHAP?')
        response = self.ask('IFU')
        if response[2] == '0':
            return 'DC'
        elif response[2] == '1':
            return 'sine'
        elif response[2] == '2':
            return 'square'
        elif response[2] == '3':
            return 'triangle'
        elif response[2] == '4':
            return 'positive ramp'
        elif response[2] == '5':
            return 'negative ramp'

    #frequency
    def set_frequency(self, freq):
        """
        in Hz
        """
        self.write('FR%8.3fHZ' % freq)
        
    def get_frequency(self):
        response =  self.ask('IFR')
        if response[-2:] == 'HZ':
            freq = response[2:-2]
        elif response[-2:] == 'KH':
            freq = response[2:-2]*1e3
        elif response[-2:] == 'MH':
            freq = response[2:-2]*1e6
            
        return freq
    
    
    #function amplitude
    def set_amplitude(self, amp):
        """
        in volts
        """
        self.write('AM%5.6fVO' % amp)
    
    def get_amplitude(self):
        response = self.ask('IAM')
        amp = response[2:-2]
        if response[-2:] == 'VO':
            return amp
        elif response[-2:] == 'MV':
            return amp*1000
        
    #offset, even though i don't need this
    #no intention of adding this to GUI
    def set_offset(self, offset):
        self.write('OF%5.6fVO' % offset)
    
    def get_offset(self):
        response = self.ask('IOF')
        amp = response[2:-2]
        if response[-2:] == 'VO':
            return amp
        elif response[-2:] == 'MV':
            return amp*1000

    



if __name__ == "__main__":
    pass
    test = HP3325B(com_port = '/dev/ttyUSB1')