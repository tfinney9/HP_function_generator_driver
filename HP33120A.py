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
# from instrument import dummy_instrument as instrument
from instrument import instrument
import serial

BAUD_RATE = 9600
BYTE_SIZE = serial.EIGHTBITS
PARITY = serial.PARITY_NONE

class HP33120A(instrument):
    """
    The HP 33120A driver, has all the commands
    that I want to use with the FG.

    Assumes default:
    9600 baud rate, 8 bits ,no parity
    """
    def __init__(self, com_port = 'COM1', baud_rate = 9600,  byte_size = serial.EIGHTBITS,
                 parity = serial.PARITY_NONE, timeout = 5, debug = True, dummy_mode = False):

        #initialize instrument with parameters
        super().__init__(com_port = com_port, baud_rate = baud_rate, byte_size = byte_size,
                         parity = parity, timeout = timeout, name = 'HP33120A', dummy_mode = dummy_mode)


        # pass

    def get_trigger_state(self):
        """
        I have no need for this
        trigger stuff right now
        """
        ask_out = self.ask('TRIG:SOUR?')
        return ask_out

    def connect(self):
        """
        tell the FG that we want to control remotely
        """
        write_out = self.write('SYST:REM')
        return write_out

    def reset(self):
        """
        reset the FG to default state
        """
        return self.write('*RST')

    def disconnect(self):
        """
        return to local control and
        disconnect
        """
        o1 = self.write('SYST:LOC') #return to local control
        o2 = self.disconnect_instrument()
        return o1,o2

    def get_error(self):
        """
        ask the FG what the issue is, if we send a bad
        command and print to console
        """
        ask_out = self.ask('SYST:ERR?')
        return ask_out

    #function shape
    def set_function(self, shape):
        """
        sine, square, Triangle, other that I'm not going to use
        shape : { SIN, SQU, TRI, RAMP, NOIS, DC, USER }

        """
        return self.write('SOUR:FUNC:SHAP %s' % shape)

    def set_triangle_shape(self):
        return self.set_function('TRI')

    def set_sine_shape(self):
        return self.set_function('SIN')

    def set_square_shape(self):
        return self.set_function('SQU')

    def get_function_shape(self):
        return self.ask('SOUR:FUNC:SHAP?')

    #frequency
    def set_frequency(self, freq):
        """
        in Hz
        """
        return self.write('SOUR:FREQ %f' % freq)

    def get_frequency(self):
        return self.ask('SOUR:FREQ?')

    #function amplitude
    def set_amplitude(self, amp):
        """
        in volts
        """
        return self.write('SOUR:VOLT %f' % amp)

    def get_amplitude(self):
        return self.ask('SOUR:VOLT?')

    #offset, even though i don't need this
    #no intention of adding this to GUI
    def set_offset(self, offset):
        return self.write('SOUR:VOLT:OFFS %f' % offset)

    def get_offset(self):
        return self.ask('SOUR:VOLT:OFFS?')




if __name__ == "__main__":
    test = HP33120A(com_port = '/dev/ttyUSB1')
