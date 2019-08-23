# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:04:56 2019
preprocess data needed 
@author: Max
"""

import src.APS_Data_Trans as adt
import pandas as pd
import datetime

import src.data.data_load as d_load

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



def get_model2lines(model_line):
    model2lines=adt.multi_find(model_line)
    rlt_list=[]
    for index,row in model2lines.iterrows():
        rlt_list.append(tuple(row.tolist()))
    
    return rlt_list

def get_klist(model_line,P):
    model2lines=adt.multi_find(model_line)
    modellist=model2lines['model_no'].unique()
    k_list=[]
    for i in modellist:
        
        loop_loop=model2lines[model2lines['model_no']==i]['line_no']
        for l in loop_loop:
            
            for item in P[i][l][0]:
                
                k_list.append((i,l,item))
    
    return k_list            


def pools_1linedays(modelpool:pd.DataFrame,dp_matrix:pd.DataFrame):
    """return model pools 1line and 2lines
    days of 1-line model"""
    modelLine=dp_matrix[['model_no','line_no']].drop_duplicates()
    modelLine.reset_index(drop=True,inplace=True)
    model2lines=adt.multi_find(modelLine)
    model2ls=model2lines.groupby('model_no')['line_no'].count()
    model2ls=model2ls.reset_index()
    model1l=modelLine.merge(model2ls,how='left',left_on='model_no',right_on='model_no')
    modelTline=modelLine[model1l['line_no_y'].isna()]
    #model2lines.rename({'model_no':'model_no_1','line_no':'line_no_1'},axis='columns')
    temppool=modelpool.merge(model2ls,how='left',left_on='model_no',right_on='model_no')
    model1pool=modelpool[temppool['line_no'].isna()]
    model2pool=modelpool[temppool['line_no'].isna()==False]
    model1pool['days']=model1pool.apply(lambda x:adt.process_csum(x['order_num'],dp_matrix[dp_matrix['model_no']==x['model_no']][['day_process','num_by_day','cum_day']].set_index('day_process')),axis=1)
    model1pool=model1pool.merge(modelTline,how='left',right_on='model_no',left_on='model_no')
    
    return model1pool, model2pool

def get_ftlist(model_line,Tn):
    modelList=model_line['model_no'].unique().tolist()
    ft_list=[]
    for i in modelList:
        
        loop_loop=model_line[model_line['model_no']==i]['line_no']
        for l in loop_loop:
            for item in Tn[i]:
                ft_list.append((i,l,item))
    return ft_list         

def get_zlist(model_line):
    modelList=model_line['model_no'].unique().tolist()
    z_comb=[]
    for i in modelList:
        #for j in modelList:
            #if i!=j:
        
        loop_loop=model_line[model_line['model_no']==i]['line_no']
        for l in loop_loop:
            jmodel=model_line[model_line['line_no']==l]['model_no']
            
            for j in jmodel:
                if i!=j:
                    z_comb.append((i,j,l))
    return z_comb