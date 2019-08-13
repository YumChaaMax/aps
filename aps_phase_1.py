# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:46:54 2019
two phase 
phase 1 : orders across the lines
phase 2: schedule
@author: Max
"""
import APS_Data_Trans as adt
import pandas as pd
import pulp
#import boto3
import datetime
import numpy as np
import time

start='2019-01-02'
buffer=30
#设定一起考虑的同型号订单区间（以交付时间为准）
merge_days=40

#weight of the working hours
alpha=0.05
#beta weight of the leadtime
beta=0.95
#gamma weight of hours in every line
gamma=0.35

