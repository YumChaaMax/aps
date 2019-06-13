# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:28:36 2019
Data Transformation for APS 
@author: Max
"""
import pandas as pd
import numpy as np
import datetime
import pulp
import math


def cross_sep_dict(table,sep_dimen,foc_dimen,ref_list):
    """a crosstable to seperate dicts based on diferent dimensions
    dimen is the dimension/factor you want to seperate, the key of the outside dict
    foc_dimen is the dimension you try to compare, the key of the inside key
    ref_list is  a list of the unique elements of the dimension
    returns a big dict
    """
    
    rlt_dict=dict()
    for i in ref_list():
        temp_table=table[sep_dimen==i].reset_index(foc_dimen)
        rlt_dict[i]=temp_table.to_dict()[i]
            
    return rlt_dict   

def table_to_Adict(table,key_col,foc_col):
    """
    a function that turns dataframe to dict
    
    """
    rlt_dict=dict()
    keys=table[key_col].unique().to_list()
    for i in keys:
        
        rlt_dict[i]=table[key_col==i][foc_col].to_list()
        
    return rlt_dict

def checknum(l,n=1):
    #计算列表中连续=n的数目，返回最大连续数
    res=[]
    count=0
    for i in l:
        if i == n:
            count+=1
        else:
            res.append(count)
            count=0
    return max(res)


def EPST(order_start,purchase_delay=12):
    """got EPST"""
    assert type(order_start) is str
    assert type(purchase_delay) is int
    epst=datetime.datetime.strptime(order_start,'%Y-%m-%d')+datetime.timedelta(days=purchase_delay)
    return epst.strftime('%Y-%m-%d')
    
def PST_onLine_date(order_start,end_date,purchase_delay=12,deliver_delay=3):
    """
    max on-line date based on LSPT and EPST, named PST
    order_start time of creating order
    end_date   delivery date
    purchase_delay  days that factory need to prepare semi-finished goods
    deliver_delay   days that factory need to pack finished goods ready for delivery
    """
    assert type(order_start) is str 
    assert type(end_date) is str
    assert type(purchase_delay) is int
    assert type(deliver_delay) is int
    pur_epst=EPST(order_start,purchase_delay)
    LPST=datetime.datetime.strptime(end_date,'%Y-%m-%d')-datetime.timedelta(days=deliver_delay)
    return max(pur_epst,LPST).strftime('%Y-%m-%d')


def left_lower_matrix(a_list):
    len_lst=len(a_list)
    rslt_lst=list()
    f=[0]*len_lst
    for i in range(len_lst):
        f.insert(0,a_list[i])
        f.pop(-1)  
        rslt_lst.append(f.copy())
    return rslt_lst
    
def practice_hour(line_task_dict,practice_curve,order_no,model,lines,plan_dates,):
    """Got a dict of working hours using pracitce_curve matirx and total tasks
    """
    maxLine=''
    ready_date=dict()
    for l in lines:
        pace_choice=[np.sign(line_task_dict[l][order_no][d]) for d in plan_dates].find(1)
        speeds=max(np.matrix(practice_curve[pace_choice][practice_curve['line']==l&practice_curve['model_no']==model]),1e-10)
        wDay=np.ceil(np.ture_divide(np.matrix([line_task_dict[l][order_no][d] for d in plan_dates]),speeds).sum()/8)
        done_date=EPST(max([line_task_dict[l][order_no][d] for d in plan_dates]),wDay+3)
        ready_date[l]=done_date
        if done_date>maxLine:
            maxLine=done_date
            
    return(maxLine,ready_date)    
    
def process_day(order_info:pd.DataFrame, practice_curve:pd.DataFrame,std_hour:pd.DataFrame,line_info:pd.DataFrame):
    """
        order_info: includes order_no., model_no., amount;
        pratice_curve: includes line_no., model_no. day pace, efficiency;
        std_hour: includes model_no, sah
        line_info: includes line_no, staff_num, work_hour
        
        returns a dict that contains all process days of orders if they are produced
        by each line solely.
    """
    prod_speed=practice_curve.merge(std_hour,how='left',left_on='model_no',right_on='model_no')
    line_info=line_info.drop(columns=['line_no'])
    prod_speed=prod_speed.merge(line_info,how='left',left_on='line_no',right_index=True)
    prod_speed['num_by_day']=round((prod_speed['work_hour']/prod_speed['sah'])*prod_speed['effi']*prod_speed['staff_num'],0)
    o_dict=order_info['order_num'].to_dict()
    model_dict=order_info['model_no'].to_dict()
    prcs_dict={}
    orderlist=order_info.index.tolist()
    linelist=line_info.index.tolist()
    for oid in orderlist:
        a_model={}
        for line in linelist:
             
            order_amt=o_dict[oid]
            
            temp_pace=prod_speed[(prod_speed['line_no']==line) & \
                                 (prod_speed['model_no']==model_dict[oid])].\
                                 sort_values(by='day_process',ascending=True)
            temp_pace=temp_pace['num_by_day'].tolist()
            
            n=len(temp_pace)
            loop=0
            while order_amt>=0:
                if loop<(n-1):
                    pace=temp_pace[loop]
                else:
                    pace=temp_pace[n-1]
                order_amt=order_amt-pace
                loop+=1
            temp_prcs=loop+round((order_amt+pace)/pace,1)
            a_model[line]=temp_prcs
        prcs_dict[oid]=a_model
    return prcs_dict
                
def day_speed_df(practice_curve:pd.DataFrame,std_hour:pd.DataFrame,line_info:pd.DataFrame):
    """
        
        pratice_curve: includes line_no., model_no. day pace, efficiency;
        std_hour: includes model_no, sah
        line_info: includes line_no, staff_num, work_hour
        
        returns a dict that contains all process days of orders if they are produced
        by each line solely.
    """           
    prod_speed=practice_curve.merge(std_hour,how='left',left_on='model_no',right_on='model_no')
    line_info=line_info.drop(columns=['line_no'])
    prod_speed=prod_speed.merge(line_info,how='left',left_on='line_no',right_index=True)
    prod_speed['num_by_day']=round((prod_speed['work_hour']/prod_speed['sah'])*prod_speed['effi']*prod_speed['staff_num'],0)
    #o_dict=order_info['order_num'].to_dict()
    
    return(prod_speed)

def order_speed_df(day_model_df:pd.DataFrame,order_info:pd.DataFrame):
    """
        day_model_df: includes model,day_process,num_by_day
        order_info includes order,model

        returns relationship between order and num_by_day
    """
    day_model_df['rid']=day_model_df.index
    order_info['order_id']=order_info.index
    order_model=order_info[['order_id','model_no','deli_date']]
    order_speed=order_model.merge(day_model_df,how='inner',left_on='model_no',right_on='model_no')            
    
    return order_speed

def model_total_volume(production_speed:pd.DataFrame,d_day:pulp.LpAffineExpression,plan_days:int):
    """
        production_speed: product speed of a model in a line
                          includes: day process, num_by_day
        d_day: days to produce 
        
        returns total volume given by days
    """
    if d_day==0:
        tot_vol=0
    else:
        tot_vol=0
        loop_day=0
        #modf_ofday=math.modf(d_day)
        #int_ofday=pulp.roundSolution(d_day,0))
        #deci_ofday=d_day-int_ofday
        nday=len(production_speed['day_process'])-1
        speed_list=production_speed.sort_values(by='day_process')['num_by_day'].tolist()
        for i in range(plan_days+1):
            loop_day+=1
            if i <nday:
                pace=speed_list[i]
            else:
                pace=speed_list[-1]
            tot_vol+=pace
            if pulp.LpConstraint(d_day-loop_day,sense=pulp.LpConstraintLE,rhs=1):
                
                break
            
        if loop_day<nday:
            deci_day=speed_list[loop_day]*(d_day-loop_day)
        else:
            deci_day=speed_list[-1]*(d_day-loop_day)
        tot_vol=tot_vol+deci_day
    
    return tot_vol        

def process_csum(Ccsum:int,order_spdid:pd.DataFrame):
    """
        Ccsum: the amount of every line will process
        order_spdpid: a data frame that includes  day_process,num_by_day
    
        returns process time of Ccsum
    """
    
    temp_pace=order_spdid['num_by_day'].tolist()
    m=len(order_spdid)
    loop=0
    if Ccsum>=1:    
        while Ccsum>=1:
            if loop<(m-1):
                pace=temp_pace[loop]
            else:
                pace=temp_pace[m-1]
            Ccsum-=pace
            loop+=1
    
        plus=(Ccsum+pace)/pace
    else:
        plus=1
    temp_prcs=loop-1+plus
    
    return temp_prcs
    
def prod_days(x,y,z):
    if z<=y:
        if x<=y:
            a=x
        else:
            a=y
        result=a-z
    else:
        a=0
        result=0
    return result

def total_volume(production_speed:pd.DataFrame,d_day,order,line):
    """
        production_speed: product speed of a model/order in a line
                          includes: day process, num_by_day
        d_day: days to produce 
        
        returns total volume given by days
    """
    if d_day==0:
        tot_vol=0
    else:
        tot_vol=0
        loop_day=0
        modf_ofday=math.modf(d_day)
        #int_ofday=pulp.roundSolution(d_day,0))
        int_ofday=modf_ofday[1]
        deci_ofday=d_day-int_ofday
        
        nday=len(production_speed['day_process'])-1
        speed_list=production_speed[(production_speed['order_id']==order)&\
                                    (production_speed['line_no']==line)][['day_process','num_by_day']].\
                                    sort_values(by='day_process')['num_by_day'].tolist()
        for i in range(int(int_ofday)):
            loop_day+=1
            if i <nday:
                pace=speed_list[i]
            else:
                pace=speed_list[-1]
            tot_vol+=pace
            if d_day-loop_day==0:
                
                break
            
        if loop_day<nday:
            deci_day=speed_list[loop_day]*deci_ofday
        else:
            deci_day=speed_list[-1]*deci_ofday
        tot_vol=tot_vol+deci_day
    
    return tot_vol   

def total_vol_15(d_day,df,order,line):
    return d_day*df[(df['order_id']==order)&(df['line_no']==line)]['spd_15'] 

def df_to_dict(df:pd.DataFrame,outkey,interkey,value):
    rlt_dict={}
    outi=df[outkey].unique().tolist()
    for i in outi:
        tempDict={}
        tempdf=df[df[outkey]==i][[interkey,value]]
        tempdf.index=tempdf[interkey]
        intj=tempdf.index
        for j in intj:
            tempDict[j]=tempdf[value][j]
        rlt_dict[i]=tempDict
    return rlt_dict