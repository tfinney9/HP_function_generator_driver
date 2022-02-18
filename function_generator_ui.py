# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 11:46:16 2021

@author: Tanner Finney
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
# from instrument import dummy_instrument as instrument
import HP33120A
import HP3325B

class fg_window(QMainWindow):
    """
    User Interface for talking to HP 3325B Function generator
    """
    def __init__(self, parent):
        super().__init__()
        # self._main = QWidget()
        """
        Initial connections
        """
        # self.parent = parent
        QMainWindow.__init__(self)
        
        self.super_layout = QHBoxLayout()
        
       
        self.main_layout = QVBoxLayout()
        # self.right_layout = QVBoxLayout()
        # self.left_layout = QVBoxLayout()
        self.setWindowTitle('Function Generator')
        # self.setWindowIcon(QtGui.QIcon('triangle.png'))
        self.setWindowIcon(QtGui.QIcon('ico/fg.png'))

        self.setMinimumWidth(250)

        self.dummy_mode = True
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console_idx = 0

        # bar = QMenuBar()
        bar = self.menuBar()
        fg_menu = bar.addMenu('&Select FG Model')
        # fg_menu.setIcon(QtGui.QIcon('fg.png'))
        self.fg_group = QActionGroup(self)
        self.fg_group.setExclusive(True)
        
        self.action_HP_33120A = QAction('HP 33120A',self, checkable = True, checked = False)
        self.action_HP_3325B = QAction('HP 3325B',self, checkable = True, checked = False)
        self.fg_group.addAction(self.action_HP_33120A)
        self.fg_group.addAction(self.action_HP_3325B)
        
        fg_menu.addActions([self.action_HP_33120A, self.action_HP_3325B])
        
        
        err_action = bar.addAction('Get &Error Msg')
        err_action.triggered.connect(self.get_error_msg)
        # bar.addAction('Serial &Port') #need to add ability to select com or whatever!
        
                
        # self.main_layout.addWidget(bar)
        console_menu = bar.addMenu('&Console')
        clear_console_action = QAction('Clear Console', self)
        dump_console_action = QAction('Dump Console to Disk',self)
        # bar.addAction(dump_console_action)
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
        
        self.main_layout.addWidget(io_box)


        function_box = QGroupBox('Waveform')
        func_layout = QHBoxLayout()
        sine_wave_button = QPushButton(QtGui.QIcon('ico/sine.png'),'')
        sine_wave_button.setToolTip('Sine Wave')
        square_wave_button = QPushButton(QtGui.QIcon('ico/square.png'),'')
        square_wave_button.setToolTip('Square Wave')
        triangle_button = QPushButton(QtGui.QIcon('ico/triangle.png'),'')
        triangle_button.setToolTip('Triangle Wave')
        
        func_layout.addWidget(sine_wave_button)
        func_layout.addWidget(square_wave_button)
        func_layout.addWidget(triangle_button)
        function_box.setLayout(func_layout)
        self.main_layout.addWidget(function_box)
        

        voltage_box = QGroupBox('Voltage (Peak to Peak)')
        voltage_layout = QHBoxLayout()
        voltage_label = QLabel('V')
        voltage_input_box = QSpinBox()
        voltage_input_box.setRange(0,40)
        voltage_input_box.setValue(10)
        self.voltage_input_box = voltage_input_box
        
        voltage_button = QPushButton('Set Voltage')
        
        voltage_layout.addWidget(voltage_input_box)
        voltage_layout.addWidget(voltage_label)
        voltage_layout.addWidget(voltage_button)
        voltage_box.setLayout(voltage_layout)
        
        
        freq_box = QGroupBox('Frequency')
        freq_layout = QHBoxLayout()
        freq_label = QLabel('Hz')
        
        freq_input_box = QDoubleSpinBox()
        freq_input_box.setRange(0,10)
        freq_input_box.setValue(0.1)
        freq_input_box.setSingleStep(0.001)
        freq_input_box.setDecimals(4)
        self.freq_input_box = freq_input_box
        
        freq_button = QPushButton('Set Frequency')
        zero_freq_button = QPushButton('Zero Frequency')
        
        freq_layout.addWidget(freq_input_box)
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(freq_button)
        freq_layout.addWidget(zero_freq_button)
        
        freq_box.setLayout(freq_layout)
        
        offset_box = QGroupBox('Voltage Offset')
        offset_layout = QHBoxLayout()
        offset_label = QLabel('V')
        offset_input_box = QSpinBox()
        offset_input_box.setRange(-40,40)
        offset_input_box.setValue(0)
        self.offset_input_box = offset_input_box
        
        offset_button = QPushButton('Set Offset Voltage')
        
        offset_layout.addWidget(offset_input_box)
        offset_layout.addWidget(offset_label)
        offset_layout.addWidget(offset_button)
        offset_box.setLayout(offset_layout)
        
        
        
        self.main_layout.addWidget(voltage_box)
        self.main_layout.addWidget(freq_box)
        self.main_layout.addWidget(offset_box)
        # self.(self.main_layout)
        # self.setCentralWidget(self.main_layout)        
        widget = QWidget()
        
        self.super_layout.addLayout(self.main_layout)
        
        

        
        self.super_layout.addWidget(self.console)
        widget.setLayout(self.super_layout)
        

        self.setCentralWidget(widget)
        
        
        
        """
        Connections        
        """
        
        # these may change
        # self.connected_to_33120A = False
        # self.connected_to_3325B = False 
        self.selected_FG = None
        self.selected_serial_port = ''
        self.inst = None
        
        #menu connections        
        dump_console_action.triggered.connect(self.dump_console_to_disk)
        clear_console_action.triggered.connect(self.clear_console)
        self.about.triggered.connect(self.show_about)
        
        #instrument connections
        # self.inst = instrument.dummy_instrument('/dev/ttyUSB0',9600,)
        # action_HP_33120A.triggered.connect(self.connect_to_33120A)
        # action_HP_3325B.triggered.connect(self.connect_to_3325B)
        
        self.action_HP_33120A.triggered.connect(lambda: self.set_FG('HP33120A'))
        self.action_HP_3325B.triggered.connect(lambda: self.set_FG('HP3325B'))
        

        
        #initialize com_box with something
        self.set_serial(com_ports[0])
        #for if the user changes something
        self.com_box.currentTextChanged.connect(lambda: self.set_serial(self.com_box.currentText()))

        
        connect_button.clicked.connect(self.connect_to_inst)
        disconnect_button.clicked.connect(self.disconnect_inst)
        reset_button.clicked.connect(self.reset_inst)
        
        #waveform connections
        sine_wave_button.clicked.connect(self.set_sine)
        triangle_button.clicked.connect(self.set_triangle)
        square_wave_button.clicked.connect(self.set_square)
        
        #A-F-O connectioned
        voltage_button.clicked.connect(self.set_voltage)
        freq_button.clicked.connect(self.set_frequency)
        offset_button.clicked.connect(self.set_offset)
        zero_freq_button.clicked.connect(self.zero_frequency)
        
        
        
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
        
    def dump_console_to_disk(self):

        console_dump_name = 'fg_console_dump_{}.txt'.format(str(random.randint(100,1000)))
        self.write_to_console('Dumping Console to Disk at: {}'.format(console_dump_name))
        with open(console_dump_name, 'a') as f:
            f.write(self.console.toPlainText())
            
    def clear_console(self):
        self.console_idx = 0
        self.console.clear()
        self.write_to_console('Console Cleared!')


    def set_FG(self, FG):
        self.selected_FG = FG
        self.write_to_console('Selected {} Function Generator'.format(FG))
        
    def get_FG(self):
        return self.selected_FG

    
    def set_serial(self, serial_port):
        self.serial_port = serial_port
        # self.serial_port = self.com_box.currentText()
        self.write_to_console('Serial Port Set to: {}'.format(self.serial_port))
    
    def get_serial(self):
        return self.serial_port

    


    def connect_to_inst(self):
        
        if self.selected_FG is None:
            self.write_to_console('Select Function Generator Model First!')
            return 
        
        # print(self.com_box.currentText())
        if str(self.com_box.currentText()) == '':
            self.write_to_console('Please select a Serial Port to Start!')
            return
        
        if self.selected_FG == 'HP33120A':
            byte_size = HP33120A.BYTE_SIZE
            baud_rate = HP33120A.BAUD_RATE
            parity = HP33120A.PARITY
            
            self.inst = HP33120A.HP33120A(self.serial_port,
                                          baud_rate,
                                          byte_size,
                                          parity,
                                          dummy_mode = self.dummy_mode)
            
        elif self.selected_FG == 'HP3325B':
            byte_size = HP3325B.BYTE_SIZE
            baud_rate = HP3325B.BAUD_RATE
            parity = HP3325B.PARITY
            self.inst = HP3325B.HP3325B(self.serial_port,
                                          baud_rate,
                                          byte_size,
                                          parity,
                                          dummy_mode = self.dummy_mode)
        
        
        
        
        setup_out = self.inst.setup_connection()
        self.write_to_console(setup_out)
        
        connect_out = self.inst.connect()
        self.write_to_console(connect_out)
        
    def disconnect_inst(self):
        disconnect_result = self.inst.disconnect()
        self.write_to_console(disconnect_result)
        
    def reset_inst(self):
        rst_rslt = self.inst.reset()
        self.write_to_console(rst_rslt)
        
    def get_error_msg(self):
        if self.inst is None:
            return 
        
        if self.selected_FG is None:
            return
        
        err_out = self.inst.get_error()
        self.write_to_console(err_out)
    
    def check_connection(self):
        # check if instrument and fg are set properly
        
        if self.inst is None:
            self.write_to_console('No connection Found')
            raise ValueError('No Connection Found!')
        if self.selected_FG is None:
            self.write_to_console('Function Generator Method Not Set!')
            raise ValueError('Function Generator Method Not Set!')
        
        else:
            return 0
    
    def set_sine(self):
        self.check_connection()
        x = self.inst.set_sine_shape()
        self.write_to_console(x)
    
    def set_square(self):
        self.check_connection()
        x = self.inst.set_square_shape()
        self.write_to_console(x)

    
    def set_triangle(self):
        self.check_connection()
        x = self.inst.set_triangle_shape()
        self.write_to_console(x)
        
    def set_voltage(self):
        voltage = self.voltage_input_box.value()
        self.check_connection()
        x = self.inst.set_amplitude(voltage)
        self.write_to_console(x)

        
    def set_frequency(self):
        freq = self.freq_input_box.value()
        self.check_connection()
        x = self.inst.set_frequency(freq)
        self.write_to_console(x)
    
    def zero_frequency(self):
        self.check_connection()
        x = self.inst.set_frequency(0)
        self.write_to_console(x)
        self.write_to_console('Frequency set to 0 Hz!')

    def set_offset(self):
        offset = self.offset_input_box.value()
        x = self.inst.set_offset(offset)
        self.write_to_console(x)
   
        
    def show_about(self):
        dlg = QDialog()
        dlg.setWindowTitle('About Function Generator')
        # dlg_btn = QPushButton('Close')

        dlg_label = QLabel('A Simple Function Generator Control Panel!\nFor use with HP33120A and HP3325B')
        dlg_layout = QHBoxLayout()
        dlg_layout.addWidget(dlg_label)
        dlg.setLayout(dlg_layout)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.exec_()





        
if __name__ == '__main__':
    app = QApplication([])
    fg = fg_window(parent = None)
    fg.show()
    sys.exit(app.exec_())
