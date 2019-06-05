# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:39:45 2019

@author: Max
"""
import pulp

def aps_solve():
    #all possible groups of lines,orders,plan dates
    order_line=[tuple(c) for c in pulp.allcombinations(prod_line,orderList)]
    #line_date=[tuple(c) for c in pulp.allcombinations(prod_line,plan_dates)]
    
    #orders=adt.table_to_Adict(ordertable,'product','order_num')
    
    #the problem variables
    Csums=pulp.LpVariable.dict("line_prod",(prod_line,orderList),0,None, pulp.LpInteger)
    r=pulp.LpVariable.dict("release",(prod_line,orderList),0)
    compD=pulp.LpVariable.dict("compDate",(prod_line,orderList),0)
    #CLines=pulp.LpVariable("CLines",[j for j in line_date] ,0) #total amount of all lines by day
    Cmax=pulp.LpVariable.dict("max date by order",[i for i in orderList],0)
    #Create the 'prob' variable to contain the problem data
    prob=pulp.LpProblem("The APS Problem",pulp.LpMaximize)
    #prob=pulp.LpProblem("The APS Problem",pulp.LpMinimize)
    
    #objective function： consider order priority and leadtime
    #eps=1e-2 
    prob+=pulp.lpSum([Csums[i_group]* orderPool['priority'][i_group[1]]*orderPool['order_type'][i_group[1]]  for i_group in order_line]),"Production Compacity considering order type"
    #prob+=Cmax+eps*lpSum([r[j] for j in order_line])-eps*[compD[j] for j in order_line]
    #The constraints
    #1. every order has to be completed before due date
    #2. relationships between release date and due date
    #3. release date>=max(0,epst-plan_dates[0]) 
    #4.fixed sum across day and lines equal total num of orders
    for o in orderList:
        for l in prod_line:
            prob+=compD[l][o] <= Cmax[o]
            prob+=compD[l][o] >=r[l][o]+(Csums[l][o]/orderPool['order_num'][o])*process_day[o][l] 
            prob+=r[l][o]>=max(0,orderPool['epst'][o]-plan_dates[0])
        prob+=pulp.lpSum(Csums[l][o] for l in prod_line)==orderPool['order_num'][o],"produce according to orders"
        prob+=Cmax[o]<=orderPool['deli_date'][o]
    
    prob.writeLP("APSModel.lp")
    prob.solve()
    
    for i in order_line:
        if Csums[i]>0:
            print(i, Csums[i],r[i],compD[i])