# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:04:56 2019
preprocess data needed 
@author: Max
"""

import APS_Data_Trans as adt
import pandas as pd
import datetime

import data.data_load as d_load

def preprocess_orders(start,merge_days,buffer):
    orderPool=d_load.load_orders()
    work_day=d_load.load_workday()
    orderPool['abstdate']=orderPool['epst'].apply(lambda x: adt.workday_idf(x,work_day))
    startAbst=work_day[work_day['day_date']==datetime.datetime.strptime(start,'%Y-%m-%d')]['workday_id'].item()
    
    orderPool['ahdate']=orderPool['deli_date']-datetime.timedelta(days=3)
    orderPool['delidate']=orderPool['ahdate'].apply(lambda x:adt.workday_idf(x,work_day,isback=False))
    ##transform and clean data，create order pool, practice matrice as input or reference data
    #order pool
    #orderPool=rawPool.copy()
    #absolute epst when first plan_date is 0
    orderPool['absEpst']=orderPool['abstdate']-startAbst
    orderPool['desLpst']=orderPool['delidate']-startAbst
    
    #absolute lpst when first plan_date is 0
    #orderPool['absLpst']=orderPool['deli_date'].apply(lambda x:(x-datetime.datetime.strptime(start,'%Y-%m-%d')).days)-orderPool['deli_ahead']+buffer
    #orderPool['desLpst']=orderPool['deli_date'].apply(lambda x:(x-datetime.datetime.strptime(start,'%Y-%m-%d')).days)-orderPool['deli_ahead']
    orderPool['absLpst']=orderPool['desLpst']+buffer
    orderPool['date_tag']=orderPool['desLpst'].apply(lambda x:adt.orderdate_period_tag(x,merge_days=merge_days,start_date=startAbst))
    orderPool.rename({'model_no':'model_no_o'},axis='columns',inplace=True)
    orderPool['date_tag']=orderPool['date_tag'].apply(lambda x:str(x))
    orderPool['order_pty']=orderPool['date_tag'].apply(lambda x: 1.0 if x=='1' else 0.5)
    
    
    #orderPool.rename({0:'order_pty'},axis='columns',inplace=True)
    orderPool['model_no_o']=orderPool['model_no_o'].apply(lambda x:str(x))
    orderPool['model_no']=orderPool['model_no_o'].str.cat(orderPool['date_tag'],sep='_')
    #orderPool['deli_date']-datetime.timedelta(days=orderPool['deli_ahead'])
    #orderPool['epst'].apply(lambda x:max((x-datetime.datetime.strptime(start,'%Y-%m-%d')).days,0))
    modelpty=orderPool.groupby('model_no')['order_pty'].mean()
    print("Finish preprocess orders!")
    
    return orderPool,modelpty

