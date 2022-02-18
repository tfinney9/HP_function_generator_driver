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
import instrument
import random

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
        self.setWindowIcon(QtGui.QIcon('fg.png'))

        self.setMinimumWidth(250)


        # bar = QMenuBar()
        bar = self.menuBar()
        fg_menu = bar.addMenu('&Select FG Model')
        # fg_menu.setIcon(QtGui.QIcon('fg.png'))
        fg_group = QActionGroup(self)
        fg_group.setExclusive(True)
        
        action_HP_33120A = QAction('HP 33120A',self, checkable = True, checked = False)
        action_HP_3325B = QAction('HP 3325B',self, checkable = True, checked = False)
        fg_group.addAction(action_HP_33120A)
        fg_group.addAction(action_HP_3325B)
        
        fg_menu.addActions([action_HP_33120A, action_HP_3325B])
        
        # bar.addAction('Serial &Port') #need to add ability to select com or whatever!
        
                
        # self.main_layout.addWidget(bar)
        console_menu = bar.addMenu('&Console')
        clear_console_action = QAction('Clear Console', self)
        dump_console_action = QAction('Dump Console to Disk',self)
        # bar.addAction(dump_console_action)
        console_menu.addAction(clear_console_action)
        console_menu.addAction(dump_console_action)      

        bar.addAction('&About') # a help menu etc


        com_layout = QHBoxLayout()
        com_label = QLabel('Serial Port')
        com_ports = instrument.get_serial_ports()
        com_box = QComboBox()
        com_box.addItems(com_ports)
        
        com_layout.addWidget(com_label)        
        com_layout.addWidget(com_box)
        
        self.main_layout.addLayout(com_layout)
        
        connect_button = QPushButton('Connect to Device')
        reset_button = QPushButton('Reset')
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(connect_button)
        button_layout.addWidget(reset_button)
        
        self.main_layout.addLayout(button_layout)

        function_box = QGroupBox('Set Waveform')
        func_layout = QHBoxLayout()
        sine_wave_button = QPushButton(QtGui.QIcon('sine.png'),'')
        sine_wave_button.setToolTip('Sine Wave')
        square_wave_button = QPushButton(QtGui.QIcon('square.png'),'')
        square_wave_button.setToolTip('Square Wave')
        triangle_button = QPushButton(QtGui.QIcon('triangle.png'),'')
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
        
        
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console_idx = 0
        
        self.super_layout.addWidget(self.console)
        widget.setLayout(self.super_layout)
        

        self.setCentralWidget(widget)
        
        
        
        """
        Connections        
        """
        
        # these may change
        self.connected_to_33120A = False
        self.connected_to_3325B = False 
        
        #menu connections        
        dump_console_action.triggered.connect(self.dump_console_to_disk)
        clear_console_action.triggered.connect(self.clear_console)
        
        #instrument connections
        # self.inst = instrument.dummy_instrument('/dev/ttyUSB0',9600,)
        # action_HP_33120A.triggered.connect(self.connect_to_33120A)
        # action_HP_3325B.triggered.connect(self.connect_to_3325B)

        
        
        
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


    def connect_to_inst(self):
        pass
        
    # def connect_to_33120A(self):
    #     pass
    
    # def connect_to_3325B(self):
    #     pass
    
    def disconnect(self):
        pass
        

        
if __name__ == '__main__':
    app = QApplication([])
    fg = fg_window(parent = None)
    fg.show()
    sys.exit(app.exec_())
