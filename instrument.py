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
    """
    Parent class for both instruments to do all the
    boring stuff

    Parameters
    ----------
    com_port -- str -- a string corresponding to the serial port: /dev/ttyUSB0, or COM1 for example

    baud_rate -- int -- function generator baud rate
    byte_size -- serial.SEVENBITS for example
    parity -- serial.PARITY
    name -- str -- a name for debugging etc
    timeout -- int -- how long we wait in seconds before we quit
    dummy_mode -- Bool -- for debugging and playing around

    """
    def __init__(self,com_port, baud_rate, byte_size,
                 parity, name = 'inst', timeout = 5, dummy_mode = False):

        self.com_port = com_port
        self.baud_rate = baud_rate
        self.byte_size = byte_size
        self.parity = parity
        self.timeout = timeout
        self.name = name

        self.message = ''

        self.connection = None
        self.dummy_mode = dummy_mode
        if self.dummy_mode == True:
            self.name = self.name + '_dummy'

    def __repr__(self):
        rep = 'instrument({},{},{},{},{},{})'.format(self.com_port,
                                                    self.baud_rate,
                                                    self.byte_size,
                                                    self.parity,
                                                    self.name,
                                                    self.timeout)
        return rep


    def setup_connection(self):
        """
        create a serial connection at the
        specified port with baud rate etc
        """
        # print('Connecting to ')
        if self.dummy_mode == True:
            self.connection = 'Dummy connection'
            return 'DUMMY: Connected to {} on {}'.format(self.name, self.com_port)

        self.connection = serial.Serial(self.com_port,
                            self.baud_rate,
                            bytesize = self.byte_size,
                            parity = self.parity,
                            stopbits = serial.STOPBITS_TWO,
                            timeout = self.timeout)
        return 'Connected to {} on {}'.format(self.name, self.com_port)


    def disconnect_instrument(self):
        """
        close the serial connection gracefully
        """
        if self.dummy_mode == True:
            self.connection = None
            return 'Connection Closed'

        self.connection.close()
        print('Connection Closed!')
        return 'Connection Closed!'


    def process_cmd_str(self, cmd_str):
        """
        add the right stuff to the command we send to the
        function generator, typically that is a newline and to
        set the encoding as ascii
        """
        end_char = '\n'

        proc_str = cmd_str + end_char

        return bytes(proc_str,encoding = 'ASCII')

    def write(self, command):
        """
        write a command and don't expect an output from the FG
        """
        if self.dummy_mode == True:
            return 'SENDING', command

        cmd = self.process_cmd_str(command)
        self.connection.write(cmd)
        return 'SENDING', cmd



    def get_last_cmd(self):
        """
        not sure what I was thinking for this.
        """
        return self.message

    def ask(self, query):
        """
        send a command to the function generators
        and then get an output
        return that output to whatever wants it
        """
        if self.dummy_mode == True:
            return 'I:{}\nO:Dummy Mode Result of Query'.format(query)
            # print(query)
            # print('Dummy mode result of query')
            # return query '\ndummy mode result of query'

        cmd = self.process_cmd_str(query)
        self.connection.write(cmd)

        output = self.connection.readline()
        self.message = output

        return 'I:{}\nO:{}'.format(query,output)




class instrument_X:
    """
    a different implementation, I'm not sure
    How I want to do this yet....

    don't use this.
    """
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
        return self.message

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
        # print(output)
        return output



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

    def connect(self):
        print('Conneceted!!!')
        return 'connected to dummy inst'

    def disconnect(self):
        print('disconnected!')
        return 'disconnect'

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
        return qry

    def get_last_cmd(self):
        return self.message

if __name__ == "__main__":
    di = dummy_instrument('COM1', 999, 8, 'none')
