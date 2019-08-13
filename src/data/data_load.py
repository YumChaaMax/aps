# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:49:04 2019

@author: Max
"""

import pandas as pd




def load_prodline():
    prodline=pd.read_excel(r'./data/prod_line_info.xlsx',names=['line_no','line_desp','staff_num','work_hour'])
    prodline.index=prodline['line_no']
    prod_line=prodline.index.tolist()
    
    line_num=len(prod_line)
    print("Loading Production Lines: Complete.")
    print("Plan %d lines."%line_num)
    return prod_line

def load_stdhour():
    model_SAH=pd.read_excel(r"./data/model_std_hour.xlsx",names=['model_no','sah'])
    model_SAH['sah']=model_SAH['sah']/3600
    model_num=len(model_SAH['model_no'].unique())
    print("Loading standard hour of models: Complete.")
    print("Got %d models."%model_num)
    return model_SAH

def load_effi():
    practice_pace=pd.read_excel(r"./data/practice_curve.xlsx",names=['uid','model_no','line_no','day_process','effi'])
    mdln_match=len(practice_pace[['model_no','line_no']].drop_duplicates())
    print("Loading practice curve-efficiency: Complete")
    print("Got %d matches."%mdln_match)
    return practice_pace

def load_orders():
    rawPool=pd.read_excel(r'./data/orderPool1.xlsx',names=['order_id','model_no','order_num',\
                                                      'order_date','deli_date','order_type','priority','epst','deli_ahead'])
    order_num=len(rawPool)
    print("Loading Orders: Complete.")
    print("Got %d orders."%order_num)
    rawPool.index=rawPool['order_id']
    return rawPool

def load_workday():
    work_day=pd.read_excel(r"./data/work_day.xlsx",names=['day_date','is_holiday','workday_id'])
    print("Loading %d days in this year:Complete "%len(work_day))
    return work_day

