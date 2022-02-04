#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 15:17:30 2022

@author: tfinney

translate to function generator language for HP33120A

Based on 
# HP_33120A.py class, to perform the communication between the Wrapper and the device
# Pieter de Groot <pieterdegroot@gmail.com>, 2008
"""


import logging


class HP33120A(instrument):
    def __init__(self, ser_connection, debug = True):
        self.ser = ser_connection
        self.debug = debug       
  
    
    def get_trigger_state(self):
        """
        I have no need for this 
        trigger stuff right now
        """
        self.ask('TRIG:SOUR?')


    def connect(self):
        self.write('SYST:REM')
        