# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:46:54 2019
two phase 
phase 1 : orders across the lines
phase 2: schedule
@author: Max
"""
import src.APS_Data_Trans as adt
import src.preprocess as prep
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

#f only models with more than 2 lines should be in the dicts

model1Pool,model2Pool=prep.pools_1linedays(ModelPool,dp_matrix)

f_comb=prep.get_model2lines(model_line)

k_comb=prep.get_klist(model_line,P)


prob=pulp.LpProblem('Phase 1 order across Line',pulp.LpMinimize)

f=pulp.LpVariable.dicts('f',f_comb,0,1,pulp.LpContinuous)

k=pulp.LpVariable.dicts('k',k_comb,0,1,pulp.LpContinuous)

prob+=

