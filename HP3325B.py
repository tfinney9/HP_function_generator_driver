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
# from instrument import dummy_instrument as instrument
from instrument import instrument 
import serial

BAUD_RATE = 300
BYTE_SIZE = serial.SEVENBITS
PARITY = serial.PARITY_EVEN


class HP3325B(instrument):
    def __init__(self, com_port = 'COM1', baud_rate = 300,  byte_size = serial.SEVENBITS, 
                 parity = serial.PARITY_EVEN, timeout = 5, debug = True, dummy_mode = False):

        #initialize instrument with parameters
        super().__init__(com_port = com_port, baud_rate = baud_rate, byte_size = byte_size, 
                         parity = parity, timeout = timeout, name = 'HP3325B',dummy_mode = dummy_mode)

        
        # pass
    
    def get_trigger_state(self):
        """
        I have no need for this 
        trigger stuff right now
        """
        # self.ask('TRIG:SOUR?')
        pass

    def connect(self):
        # self.write('Not Yet Implemented!')
        write_out = self.write('RMT')
        return write_out

    def disconnect(self):
        o1 = self.write('LCL')
        o2 = self.disconnect()
        return o1,o2

    def reset(self):
        return self.write('*RST')

    #function shape
    def set_function(self, function):
        """
        sine, square, Triangle, other that I'm not going to use
        """
        # self.write('SOUR:FUNC:SHAP %s' % shape)
        if function == 'DC':
            return self.write('FU0')
        if function == 'SINE':
            return self.write('FU1')
        if function == 'SQUARE':
            return self.write('FU2')
        if function == 'TRIANGLE':
            return self.write('FU3')
        if function == 'POSITIVE RAMP':
            return self.write('FU4')
        if function == 'NEGATIVE RAMP':
            return self.write('FU5')

    def set_triangle_shape(self):
        return self.set_function('TRIANGLE')
        
    def set_sine_shape(self):
        return self.set_function('SINE')
    
    def set_square_shape(self):
        return self.set_function('SQUARE')

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
        return self.write('FR%8.3fHZ' % freq)
    
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
        return self.write('AM%5.6fVO' % amp)
    
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
        return self.write('OF%5.6fVO' % offset)
    
    def get_offset(self):
        response = self.ask('IOF')
        amp = response[2:-2]
        if response[-2:] == 'VO':
            return amp
        elif response[-2:] == 'MV':
            return amp*1000

    def get_error(self):
        # return 'HP3325B does not support error messaging'
        ask_out = self.ask('ERR?')
        return ask_out
    



if __name__ == "__main__":
    pass
    test = HP3325B(com_port = '/dev/ttyUSB1')