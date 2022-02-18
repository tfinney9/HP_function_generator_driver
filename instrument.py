#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 15:34:01 2022

@author: tfinney
"""

import logging #someday?
import serial
import serial.tools.list_ports

def get_serial_ports():
    port_obj = serial.tools.list_ports.comports()
    port_list = []
    # print(port_obj)
    for i in range(len(port_obj)):
        port_list.append(port_obj[i].device)
        
    return port_list


class instrument:
    def __init__(self, com_port, baud_rate, byte_size, 
                 parity, name = 'inst', timeout = 5):
        
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.byte_size = byte_size
        self.parity = parity
        self.timeout = timeout
        self.name = name
        
        self.message = ''
    
    def __repr__(self):
        rep = 'instrument({},{},{},{},{},{})'.format(self.com_port,
                                                    self.baud_rate,
                                                    self.byte_size,
                                                    self.parity,
                                                    self.name,
                                                    self.timeout)
        return rep
        
    def process_cmd_str(self, cmd_str):
        end_char = '\n'
        
        proc_str = cmd_str + end_char
        
        return bytes(proc_str)
    
    def write(self, command):
        cmd = self.process_cmd_str(command)
        
        with serial.Serial(self.com_port, 
                           self.baud_rate, 
                           bytesize = self.byte_size,
                           parity = self.parity,
                           stopbits = serial.STOPBITS_TWO,
                           timeout = self.timeout) as ser:
            self.message = cmd
            ser.write(cmd) #write command 
            
    def get_last_cmd(self):
        return message
    
    def ask(self, query):
        """
        write and then read
        """
        cmd = self.process_cmd_str(query)
        
        with serial.Serial(self.com_port, 
                           self.baud_rate, 
                           bytesize = self.byte_size,
                           parity = self.parity,
                           timeout = self.timeout) as ser:
            
            ser.write(cmd) #write command 
        
        output = ser.readline()
        self.message = output
        print(output)

    
    
class dummy_instrument:
    """
    everything just to test and print nothing
    """
    def __init__(self, com_port, baud_rate, byte_size, 
                 parity, name = 'Dummy', timeout = 5):
        
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.byte_size = byte_size
        self.parity = parity
        self.timeout = timeout
        self.name = name
        self.message = ''        
        # pass
    
    def __repr__(self):
        rep = 'dummy_instrument({},{},{},{},{},{})'.format(self.com_port,
                                                           self.baud_rate,
                                                           self.byte_size,
                                                           self.parity,
                                                           self.name,
                                                           self.timeout)
        return rep
        
    def process_cmd_str(self, cmd_str):
        """
        note that this does ascii  for now
        the function generators probably don't dig utf-8
        """
        end_char = '\n'
        
        proc_str = cmd_str + end_char
        
        return bytes(proc_str, 'ascii')

    def write(self, command):
        cmd = self.process_cmd_str(command)
        self.message = cmd
        print(cmd)
    
    def ask(self, query):
        qry = self.process_cmd_str(query)
        print(qry)
        self.message = qry
        print('Here is the response')
    
    def get_last_cmd(self):
        return message
    
if __name__ == "__main__":
    di = dummy_instrument('COM1', 999, 8, 'none')
    
    
    
    
    
    
    
        
        