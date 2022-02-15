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
        
        self.main_layout = QVBoxLayout()
        # self.right_layout = QVBoxLayout()
        # self.left_layout = QVBoxLayout()
        self.setWindowTitle('Function Generator')
        # self.setWindowIcon(QtGui.QIcon('triangle.png'))
        self.setWindowIcon(QtGui.QIcon('fg.png'))

        self.setMinimumWidth(250)


        # bar = QMenuBar()
        bar = self.menuBar()
        fg_menu = bar.addMenu('&Select FG')
        # fg_menu.setIcon(QtGui.QIcon('fg.png'))
        fg_group = QActionGroup(self)
        fg_group.setExclusive(True)
        
        action_HP_33120A = QAction('HP 33120A',self, checkable = True, checked = False)
        action_HP_3325B = QAction('HP 3325B',self, checkable = True, checked = False)
        fg_group.addAction(action_HP_33120A)
        fg_group.addAction(action_HP_3325B)
        
        fg_menu.addActions([action_HP_33120A, action_HP_3325B])
        
        bar.addAction('Serial &Port') #need to add ability to select com or whatever!
        
        bar.addAction('&About') # a help menu etc
                
        # self.main_layout.addWidget(bar)

        connect_button = QPushButton('Connect to Device')
        reset_button = QPushButton('Reset')
        

        # self.main_layout.addWidget(reset_button)
        
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
        
        self.main_layout.addWidget(voltage_box)
        self.main_layout.addWidget(freq_box)

        # self.(self.main_layout)
        # self.setCentralWidget(self.main_layout)        
        widget = QWidget()
        widget.setLayout(self.main_layout)

        self.setCentralWidget(widget)
        
if __name__ == '__main__':
    app = QApplication([])
    fg = fg_window(parent = None)
    fg.show()
    sys.exit(app.exec_())
