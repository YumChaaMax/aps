# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:26:16 2019

@author: Max
"""
from collections import namedtuple
class Setup(namedtuple('IAmReallyLazy', 'name ' + ' '.join(f's{s}' for s in range(36, 47)))):
    # inits with name and sizes 's36', 's37'... 's46'
    repetitions = 0
    
setups = [
    Setup('A1', 1, 2, 3, 3, 2, 1, 0, 0, 0, 0, 0),
    Setup('A2', 0, 1, 2, 3, 3, 2, 1, 0, 0, 0, 0),
    Setup('R7', 0, 0, 1, 1, 1, 1, 2, 0, 0, 0, 0),
    Setup('D1', 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0),
    # and others
]

setup_names = [s.name for s in setups]

k=[s.repetitions for s in setups]   

min_size = 36
max_size = 46
sizes = ['s' + str(s) for s in range(min_size, max_size+1)

if __name__=='__main__':
    Setup()