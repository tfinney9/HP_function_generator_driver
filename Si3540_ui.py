#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 26 10:19:10 2022

@author: tfinney

simple stupid user interface to run an Si3540 from serial on both linux and windows
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSlot, QThread, pyqtSignal, QObject
from PyQt5 import QtGui
import numpy
import time
import sys

import random

from instrument import get_serial_ports
import instrument

# these parameters are generaly immutable and set by the si3540
BYTE_SIZE = instrument.serial.EIGHTBITS
PARITY = instrument.serial.PARITY_NONE
BAUD_RATE = 9600



class main(QMainWindow):
    
    def __init__(self, parent):
        super().__init__()
        # self._main = QWidget()
        """
        Initial connections
        """
        # self.parent = parent
        QMainWindow.__init__(self)

        self.super_layout = QVBoxLayout()


        self.main_layout = QVBoxLayout()
        # self.right_layout = QVBoxLayout()
        # self.left_layout = QVBoxLayout()
        self.setWindowTitle('Si3540 Motor')
        # self.setWindowIcon(QtGui.QIcon('triangle.png'))
        self.setWindowIcon(QtGui.QIcon('ico/fg.png'))


        self.setMinimumWidth(250)
        
        self.dummy_mode = True
        
        self.console_box = QGroupBox('Command Log')
        self.console_layout = QHBoxLayout()
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console_idx = 0
        
        self.console_layout.addWidget(self.console)
        self.console_box.setLayout(self.console_layout)
        
        bar = self.menuBar()
        
        console_menu = bar.addMenu('&Log')
        clear_console_action = QAction('Clear Log', self)
        dump_console_action = QAction('Dump Log to Disk',self)
        
        console_menu.addAction(clear_console_action)
        console_menu.addAction(dump_console_action)
        

        
        self.about = bar.addAction('&About') # a help menu etc


        io_box = QGroupBox('Device Control')
        io_layout = QVBoxLayout()

        com_layout = QHBoxLayout()
        com_label = QLabel('Serial Port')

        if self.dummy_mode == True:
            self.write_to_console('Test Mode Activated!')
            com_ports = ['COM1', 'COM2'] #for testing!
        else:
            com_ports = get_serial_ports()

        com_box = QComboBox()
        com_box.addItems(com_ports)
        self.com_box = com_box

        com_layout.addWidget(com_label)
        com_layout.addWidget(com_box)

        # self.main_layout.addLayout(com_layout)
        io_layout.addLayout(com_layout)

        connect_button = QPushButton('Connect to Device')
        reset_button = QPushButton('Reset')
        disconnect_button = QPushButton('Disconnect')
        # disconnect_button.setIcon(QtGui.QIcon('disconnect.png'))
        disconnect_button.setToolTip('Disconnect')

        button_layout = QHBoxLayout()
        button_layout.addWidget(connect_button)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(disconnect_button)

        # self.main_layout.addLayout(button_layout)
        io_layout.addLayout(button_layout)
        io_box.setLayout(io_layout)

        self.super_layout.addWidget(io_box)
        
        
        # End IO Box
        
        # begin command writer
        self.cmd_layout = QHBoxLayout()
        self.cmd_box = QGroupBox('Write Command')
        command_line = QLineEdit()
        self.command_line = command_line
        # ask_button = QPushButton()
        # write_button = QPushButton('Write!')
        # clear_button = QPushButton('Clear')
        # self.write_button = write_button

        self.cmd_layout.addWidget(command_line)
        self.cmd_box.setLayout(self.cmd_layout)
        # self.cmd_layout.addWidget(write_button)
        # self.cmd_layout.addWidget(clear_button)

        
        
        """
        Layout Building
        """
        widget = QWidget()

        # self.super_layout.addLayout(self.main_layout)
            



        self.super_layout.addWidget(self.console_box)
        self.super_layout.addWidget(self.cmd_box)

        widget.setLayout(self.super_layout)



        self.setCentralWidget(widget)


        """
        connections
        """
        self.inst = None
        self.selected_serial_port = ''

        #menubar things
        dump_console_action.triggered.connect(self.dump_console_to_disk)
        clear_console_action.triggered.connect(self.clear_console)
        self.about.triggered.connect(self.show_about)

        # self.set_serial(com_ports[0])
        self.com_box.currentTextChanged.connect(lambda: self.set_serial(self.com_box.currentText()))

        connect_button.clicked.connect(self.connect_to_inst)
        disconnect_button.clicked.connect(self.disconnect_inst)
        
        self.command_line.returnPressed.connect(lambda: self.write_cmd(self.command_line.text()))
        # reset_button.clicked.connect(self.reset_inst)
        # z
    def write_to_console(self, content):
        """
        Write whatever to the console and terminal for debugging
        and clarity.
        """
        console_str = '[{}] '.format(self.console_idx) + str(content) #+ '\n'
        # self.console.append(console_str)
        print(console_str)
        self.console.appendHtml(console_str)
        self.console_idx += 1
        
    def write_cmd(self, command):
        if self.inst is None and self.dummy_mode == False:
            return 
        
        if self.dummy_mode == True:
            self.write_to_console('Dummy_mode:')
            self.write_to_console(command)
            self.command_line.clear()
            return 
        
        out = self.inst.ask(command)
        self.write_to_console(out)
        self.command_line.clear()

        # pass
    
    
    def check_connection(self):
        """
        quick check before doing anything to see if
        there is someone to talk to.
        """
        # check if instrument and fg are set properly

        if self.inst is None:
            self.write_to_console('No connection Found')
            raise ValueError('No Connection Found!')
        if self.selected_FG is None:
            self.write_to_console('Function Generator Method Not Set!')
            raise ValueError('Function Generator Method Not Set!')

        else:
            return 0
        
    def clear_console(self):
        """
        delete contents of the console so it looks nice again
        """
        self.console_idx = 0
        self.console.clear()
        self.write_to_console('Console Cleared!')
        
    def dump_console_to_disk(self):
        """
        Dump the console to a text file with a random number as its name
        """
        console_dump_name = 'fg_console_dump_{}.txt'.format(str(random.randint(100,1000)))
        self.write_to_console('Dumping Console to Disk at: {}'.format(console_dump_name))
        with open(console_dump_name, 'a') as f:
            f.write(self.console.toPlainText())
            
    def connect_to_inst(self):
        """
        Initialize a connection to the function generator
        and return the serial connection object as
        self.inst
        """
        if self.selected_FG is None:
            self.write_to_console('Select Function Generator Model First!')
            return

        # print(self.com_box.currentText())
        if str(self.com_box.currentText()) == '':
            self.write_to_console('Please select a Serial Port to Start!')
            return
        
        self.inst = instrument(self.serial_port, BAUD_RATE, BYTE_SIZE, PARITY, name = 'SI3540')
        setup_out = self.inst.setup_connection()
        self.write_to_console(setup_out)
        
    def disconnect_inst(self):
        """
        close out the connection
        """
        disconnect_result = self.inst.disconnect()
        self.write_to_console(disconnect_result)

    # def reset_inst(self):
    #     """
    #     send the reset command
    #     """
    #     self.check_connection()
    #     rst_rslt = self.inst.reset()
    #     self.write_to_console(rst_rslt)
    
    def show_about(self):
        """
        An about window that needs some work.
        """
        dlg = QDialog()
        dlg.setWindowTitle('About Si3540')
        # dlg_btn = QPushButton('Close')

        dlg_label = QLabel('Stand Old Ivy!')
        dlg_layout = QHBoxLayout()
        dlg_layout.addWidget(dlg_label)
        dlg.setLayout(dlg_layout)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()
    
        
        
        
if __name__ == '__main__':
    app = QApplication([])
    fg = main(parent = None)
    fg.show()
    sys.exit(app.exec_())        
        
        
        
        
        
