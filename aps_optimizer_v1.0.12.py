# -*- coding: utf-8 -*-
"""
Created on Fri May 17 12:01:27 2019

@author: Max
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:25:25 2019
APS /WEEK
@author: Max
"""
import APS_Data_Trans as adt
import pandas as pd
import pulp

import datetime

#hyposthesis: All models can be done by all lines
#mkdates=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
#mkdates='2018-05-21'
##read in all data
#a list of production line 
prodline=pd.read_excel(r'./data/prod_line_info.xlsx',names=['line_no','line_desp','staff_num','work_hour'])
prodline.index=prodline['line_no']
prod_line=prodline.index.tolist()
line_num=len(prod_line)
#read working days referenc table
#working_days=pd.read_excel(.columns=['work_dates','type'])
plan_dates=['2019-04-25','2019-04-26','2019-04-27','2019-04-28','2019-04-29','2019-04-30']
days=len(plan_dates)


# standard work hours for each product line in the next week, suppose is defined as hour 
#stdH=10*6

model_SAH=pd.read_excel(r"./data/model_std_hour.xlsx",names=['model_no','sah'])

#read learn pace table,H/piece
practice_pace=pd.read_excel(r"./data/practice_curve.xlsx",names=['uid','model_no','line_no','day_process','effi'])


#read order table actual and other predicted confirmed by production manager 
rawPool=pd.read_excel(r'./data/orderPool.xlsx',names=['order_id','model_no','order_num','order_date','deli_date','order_type','priority','epst','deli_ahead'])
rawPool.index=rawPool['order_id']
#need to adjust the parameter (which could affect the deputy of order type)

#read production records
#prd_records=pd.read_excel(names=['line_id','order_id','model_no','prd_num','prd_date'])




##transform and clean data，create order pool, practice matrice as input or reference data
#order pool
orderPool=rawPool.copy()
orderPool['cof']=orderPool['order_type']*orderPool['priority']


#dicts that contain the process time(day) produced by each line sole
process_days=adt.process_day(orderPool,practice_pace,model_SAH,prodline)
#process_day=new_dict

#unique order_no. and model_no.
orderList=orderPool.index.tolist()
modelList=orderPool['model_no'].unique().tolist()
order_sah=orderPool[['order_id','model_no']].merge(model_SAH,how='left',left_on='model_no',right_on='model_no')
date_s=pd.Series(plan_dates)

#practice matrix
#practice_matrix=pd.DataFrame()
#for l in prod_line:
    #for i_m in modelList:
        #a=practice_pace[practice_pace['line']==l&practice_pace['model']==i_m].reset_index('day_process')
        #ref=a['learn_pace'].to_list()
        #rlt_table=pd.DataFrame(adt.left_lower_matrix(ref))
        
        #rlt_table['model_no']=i_m
        #rlt_table['line']=l
        #rlt_table=rlt_table.merge(date_s,left_index=True,right_index=True)
        
        #practice_matrix=practice_matrix.append(rlt_table)
                      
    
#a dict that contains the relationship between order and  model, model is the key
#model_orderDict=adt.table_to_Adict(orderPool[['order_id','mode_no']],'model_no','order_id')


#last six working days of certain models produced 
#dateindex=working_days[working_days['work_dates']==mkdates].index()
#index_list=working_days[(dateindex-7):dateindex].to_list()
#latest_6=prd_records[(prd_records['prd_date'].isin(index_list))&(prd_records['model_no'].isin(modelList))] 


#slowest speed of all models
#slowest=practice_pace[['line','model_no','learn_pace']][practice_pace['day_process']==1]


#product_pace=adt.cross_sep_dict(learn_pace,'model_no','prod_no')

#a list of all products to be manufactured
#prod_list=ordertable['product'].unique()

#all possible groups of lines,orders,plan dates
#order_line=[tuple([i,k]) for i in prod_line for k in orderList]
#line_date=[tuple(c) for c in pulp.allcombinations(prod_line,plan_dates)]

#orders=adt.table_to_Adict(ordertable,'product','order_num')
#got day volume produced based on practice curve
dp_matrix=adt.day_speed_df(practice_pace,model_SAH,prodline)
order_spd=adt.order_speed_df(dp_matrix,orderPool)
order_spd['std']=order_spd['work_hour']*order_spd['staff_num']/order_spd['sah']
order_std=order_spd[['order_id','model_no','line_no','std']].drop_duplicates()
k_a_df=pd.read_excel(r'./data/effi_ka.xlsx',names=['model_no','line_no','k','a'])
o_l_ka=orderPool[['order_id','model_no']].merge(k_a_df,how='inner',left_on='model_no',right_on='model_no')
new_df=o_l_ka.merge(order_std,how='left',left_on=['order_id','line_no'],right_on=['order_id','line_no'])
new_df['k2']=new_df['k']*2
new_df['spd']=new_df['k']*new_df['std']
new_df['spd_2']=new_df['k2']*new_df['std']
new_df['spd_15']=new_df['k']*1.5*new_df['std']
#the problem variables
#Csums=pulp.LpVariable.dicts("line_prod",(prod_line,orderList),0,None, pulp.LpInteger)
r=pulp.LpVariable.dicts("release",(prod_line,orderList),0)
Comp1=pulp.LpVariable.dicts("compDate2",(prod_line,orderList),0,2)
Comp2=pulp.LpVariable.dicts("compDatalst",(prod_line,orderList),0)
#CLines=pulp.LpVariable("CLines",[j for j in line_date] ,0) #total amount of all lines by day
##Create the 'prob' variable to contain the problem data
x=pulp.LpVariable.dicts("x",(prod_line,orderList),0,1,pulp.LpInteger)
prob=pulp.LpProblem("The APS Problem",pulp.LpMaximize)
#prob=pulp.LpProblem("The APS Problem",pulp.LpMinimize)

#objective function： consider order priority and leadtime
#eps=1e-2 
#lambda compD[l][o] if compD[l][o]<=len(plan_dates) else len(plan_dates)
#
#prob+=pulp.lpSum([orderPool['priority'][o]*orderPool['order_type'][o]*\
                  #adt.model_total_volume(order_spd[(order_spd['order_id']==o)&(order_spd['line_no']==l)][['day_process','num_by_day']],adt.prod_days(Comp[l][o],len(plan_dates),r[l][o]),len(plan_dates))\
                  #for o in orderList for l in prod_line])
prob+=0

#prob+=Cmax+eps*lpSum([r[j] for j in order_line])-eps*[compD[j] for j in order_line]
#The constraints
#1. every order has to be completed before due date
#2. relationships between release date and due date
#3. release date>=max(0,epst-plan_dates[0]) 
#4.fixed sum across day and lines equal total num of orders
for o in orderList:
    for l in prod_line:
        prob+=r[l][o]+Comp1[l][o]+Comp2[l][o] <= (orderPool['deli_date'][o]-datetime.datetime.strptime(plan_dates[0],'%Y-%m-%d')).days#reference the first day of plan-dates as the first day
        prob+=Comp1[l][o]>=-Comp2[l][o]
        #prob+=Comp2[l][o]+Comp1[l][o]>=Comp2[l][o]
        
        #prob+=r[l][o]+adt.process_csum(Csums[l][o],order_spd[(order_spd['order_id']==o)&(order_spd['line_no']==l)][['day_process','num_by_day']])<=(orderPool['deli_date'][o]-datetime.datetime.strptime(plan_dates[0],'%Y-%m-%d')).days
        prob+=r[l][o]>=max(0,(orderPool['epst'][o]-datetime.datetime.strptime(plan_dates[0],'%Y-%m-%d')).days)
    prob+=pulp.lpSum([(new_df[(new_df['order_id']==o)&(new_df['line_no']==l)]['spd']*Comp1[l][o])+(new_df[(new_df['order_id']==o)&(new_df['line_no']==l)]['spd_15']*Comp2[l][o]) for l in prod_line])==orderPool['order_num'][o]
    #prob+=pulp.lpSum([new_df[(new_df['order_id']==o)&(new_df['line_no']==l)]['spd']*Comp[l][o] for l in prod_line])<=orderPool['order_num'][o]

for l in prod_line:
    prob+=pulp.lpSum([Comp1[l][o]+Comp2[l][o] for o in orderList if r[l][o]<=len(plan_dates)])>=len(plan_dates)
    #prob+=pulp.lpSum([Comp[l][o] for o in orderList if r[l][o]+Comp[l][o]<=len(plan_dates)])<=len(plan_dates)    
#for l in prod_line:
    
    #prob+=pulp.lpSum([Comp[l][o] for o in orderList if r[l][o]<=(len(plan_dates)-1)])>=len(plan_dates)
#prob+=pulp.lpSum([k_a_dict[l][o]['k']*Comp[l][o]**k_a_dict[l][o]['a'] for l in prod_line for o in orderList])==orderPool['order_num'].sum()
#5.every line cannot made two orders at the same time

#eps=1e-2 
#for o in orderList:
    #prob+=Cmax+eps*pulp.lpSum([r[l][o] for l in prod_line])-eps*pulp.lpSum([compD[l][o] for l in prod_line])   
    
prob.writeLP("APS.lp")
prob.solve()
print("Status:", pulp.LpStatus[prob.status])



#for o in orderList:
    #for l in prod_line:
        #print((l,o),r[l,o].value(),compD[l,o].value(),Cmax[l,o].value())
#a=[]
a=[]
for v in prob.variables():
    
    b=v.name.split(sep='_')
    b.append(v.varValue)
    a.append(b)
    print(v.name, "=", v.varValue)

rlt_df=pd.DataFrame(a)  
rlt_df.columns=['name','line_no','order_id','num']  
lch_df=rlt_df[(rlt_df['num']!=0) & (rlt_df['name']=='compDate')]

rls_df=rlt_df[rlt_df['name']=='release']
temp_df=lch_df.merge(rls_df,how='left',left_on=['line_no','order_id'],right_on=['line_no','order_id'])
temp_df.columns=['c_name','line_no','order_id','compD','r_name','release']
result=temp_df[['line_no','order_id','compD','release']].sort_values(by=['line_no','release'])
result['deli']=result['release']+result['compD']
result['num']=result.apply(lambda x:adt.total_volume(order_spd,x['compD'],x['order_id'],x['line_no']),axis=1)
temp_result=result.merge(new_df,how='left',left_on=['order_id','line_no'],right_on=['order_id','line_no'])
result['num_1']=temp_result['compD']*temp_result['spd_15']
solution1=result.copy()
    #a.append((v.name,v.varValue))
#rlt_df=pd.DataFrame(a)
#rlt_df.to_csv("test.csv")
    
print("Total amounts of products by week =", pulp.value(prob.objective)) 
#for i in order_line:
    #if Csums[i]>0:
        #print(i, Csums[i],r[i],compD[i])
        
    #5 orders with the same models tend to be planned together, because a.change time and b.high efficiency
    #6  
    #prob+=orderPool['deli_date'][order]-datetime.timedelta(days=3)==prod_sums[l][order][d]/speed[order] for l in prod_lines for d in plan_dates
#2.use practice curve to compute PST (LPST,EPST),plan_date should be greater than PST
#3.the same model has to be planned in consecutive days
#mo_prac=dict()
#for line in prod_line:
    #inter_dict=dict()
    #check_startups=dict()
    #every line produced models
    #temp_one_line=latest_6[latest_6['line_id']==line]
    #if len(temp_one_line)!=0:
        #temp_old=np.zeros((6,1))
        #temp_old_dict=adt.table_to_Adict(temp_one_line,'model_no','order_no')
        
    #for model in modelList:
        #get model's plan_date if planned =1,not planed =0
        #consecutive pattern better than sparsely manufacture the same models(required now)
        #prob+=adt.checknum([np.sign(sum([prod_sums[line][order][d] for order in model_orderDict[model]])) for d in plan_dates])==[np.sign(sum([prod_sums[line][order][d] for order in model_orderDict[model]])) for d in plan_dates].count(1)
        #inter_dict[model]=temp
        
        #practice_pace['learn_pace'][practice_pace['line']==line & practice_pace['model_no']==model].max()
        #adt.checknum([np.sign(sum([prod_sums[line][order][d] for order in model_orderDict[model]])) for d in plan_dates)]))>=0
        #for now choose the slowest speed to simplify the problem
        #for a in model_orderDict[model]:
            #PST=adt.PST_onLine_date(orderPool['order_date'][orderPool['order_no']==a],12,orderPool['deli_date'][orderPool['order_no']==a],prod_sums[line][a][d]*slowest['learn_pace'][slowest['line']=line & slowest['model_no'=model]]+3
            #PST=adt.PST_onLine_date(orderPool['order_date'][orderPool['order_no']==a],\
                                    #orderPool['deli_date'][orderPool['order_no']==a],12,\
                                    #math.ceil(float(orderPool['order_num'][orderPool['order_no']==a]/(8*slowest['learn_pace'][slowest['line']==line & slowest['model_no']==model]))+3))
            #PST can also be just EPST,because there are more than 1 line can do manufacture
            
            #2.plan_date should be greater than EPST
            #prob+=pulp.lpSum([prod_sums[line][a][d] for d in plan_dates if d<posPool['epst'][a])])==0,"plan_dates have to be later than EPST"
    #mo_prac[line]=inter_dict
        #model-practice matirx
        #line_m_matrix=practice_matrix[practice_matrix['model_no']==model&practice_matrix['line']==line]
    #4.every line should work no more than 8 hours,use practice matrix to find the right speed
        
            #pulp.lpSum(prod_sum[line][pd][order]/ for order in orderList]
        #prob+=np.true_divide(np.matrix([sum([prod_sums[line][order][d] for order in model_orderDict[model]]) for d in plan_dates]),\
        #np.matrix(line_m_matrix[[max(np.sign(sum([prod_sums[line][order][d] for order in model_orderDict[model]])),1e-10) for d in plan_dates].find(1)]))<=8*len(plan_dates)
    
    
    
    
   
    


 


#Each of the variables is printed with it's resoved optimum value

    
 #the optimized objective function value is printed to the screen
 