#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 12:27:10 2022

@author: tfinney
"""

import matplotlib.pyplot as plt
import numpy as np


#%% generate square wave

x = np.arange(0,50)

def square_wave(x):
    # y = np.zeros()
    y = []
    div = 0.25*len(x)
    for i in range(len(x)):
        if i < div:
            y.append(0)
        if i > div and i < div * 2:
            y.append(1)
        if i > div * 2 and i < div * 3:
            y.append(-1)
        if i > div*3:
            y.append(0)
        
    return y
    
y = square_wave(x)
plt.plot(x[1:],y,'-', color = 'k', linewidth = 20)
# plt.spine
plt.axis('off')
plt.savefig('square.png', transparent = True)


#%% sine wave
x = np.linspace(0, 2*np.pi)


# def sine(x)
y = np.sin(x)
plt.plot(x,y,'-', color = 'k', linewidth = 20)
# plt.spine
plt.axis('off')
plt.savefig('sine.png', transparent = True)



#%% triangle wave

x = [0,1,2,3,4]
y = [0,1,0,-1,0]

plt.plot(x,y,'-', color = 'k', linewidth = 20)
plt.axis('off')
plt.savefig('triangle.png', transparent = True)


