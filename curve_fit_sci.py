# -*- coding: utf-8 -*-
"""
Created on Mon May 20 17:33:28 2019

@author: Max
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

x = np.array([ 1,2,3,4 ])
y = np.array([ 0.60,0.65,0.68,0.70])

def func(x,k,a):
    return(k*x**a)

sol1,sol2 = curve_fit(func, x, y, p0=[0.61,0.1] )
#sol2 = curve_fit(func_powerlaw, x, y, p0 = np.asarray([-1,10**5,0]))