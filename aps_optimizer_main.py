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
L=prod_line.copy()
line_num=len(prod_line)
#read working days referenc table
#working_days=pd.read_excel(.columns=['work_dates','type'])
#plan_dates=['2019-04-20','2019-04-21','2019-04-22','2019-04-23','2019-04-24','2019-04-25']

#days=len(plan_dates)
start='2019-01-01'
buffer=5
#设定一起考虑的同型号订单区间（以交付时间为准）
merge_days=90

# standard work hours for each product line in the next week, suppose is defined as hour 
#stdH=10*6

model_SAH=pd.read_excel(r"./data/model_std_hour.xlsx",names=['model_no','sah'])

#read learn pace table,H/piece
practice_pace=pd.read_excel(r"./data/practice_curve.xlsx",names=['uid','model_no','line_no','day_process','effi'])


#read order table actual and other predicted confirmed by production manager 
rawPool=pd.read_excel(r'./data/orderPool.xlsx',names=['order_id','model_no','order_num',\
                                                      'order_date','deli_date','order_type','priority','epst','deli_ahead'])

rawPool.index=rawPool['order_id']
#need to adjust the parameter (which could affect the deputy of order type)

#read production records
#prd_records=pd.read_excel(names=['line_id','order_id','model_no','prd_num','prd_date'])




##transform and clean data，create order pool, practice matrice as input or reference data
#order pool
orderPool=rawPool.copy()
#absolute epst when first plan_date is 0
orderPool['absEpst']=orderPool['epst'].apply(lambda x:max((x-datetime.datetime.strptime(start,'%Y-%m-%d')).days,0))
#absolute lpst when first plan_date is 0
#orderPool['absLpst']=orderPool['deli_date'].apply(lambda x:(x-datetime.datetime.strptime(start,'%Y-%m-%d')).days)-orderPool['deli_ahead']+buffer
orderPool['desLpst']=orderPool['deli_date'].apply(lambda x:(x-datetime.datetime.strptime(start,'%Y-%m-%d')).days)-orderPool['deli_ahead']
orderPool['absLpst']=orderPool['desLpst']+buffer
#orderPool['deli_date']-datetime.timedelta(days=orderPool['deli_ahead'])
#orderPool['epst'].apply(lambda x:max((x-datetime.datetime.strptime(start,'%Y-%m-%d')).days,0))
g=adt.df_to_dict(orderPool,'model_no','order_id','desLpst')

# get min epst by models
modelPool=orderPool.groupby('model_no')['order_num'].sum()



#dicts that contain the process time(day) produced by each line sole
process_days=adt.process_day(orderPool,practice_pace,model_SAH,prodline)
#process_day=new_dict

#unique order_no. and model_no.
orderList=orderPool.index.tolist()
modelList=orderPool['model_no'].unique().tolist()
modelDict=orderPool[['model_no']].to_dict()['model_no']

modelTot=orderPool.groupby('model_no')['order_num'].sum()
modelSum={}
for i in modelList:
    modelSum[i]=modelTot[i]

orderD=adt.df_to_dict(orderPool,'model_no','order_id','order_num')
Oepst=adt.df_to_dict(orderPool,'model_no','order_id','absEpst')
Olpst=adt.df_to_dict(orderPool,'model_no','order_id','desLpst')

w={}
for i in modelList:
    temp_df=orderPool[orderPool['model_no']==i]
    
    tempdict={}
    tOlist=temp_df.index
    for j in tOlist:
    
        tempdict[j]=temp_df['priority'][j]
        
    w[i]=tempdict

modelEP=orderPool.groupby(by='model_no')['absEpst'].min()
modelLpst1=orderPool.groupby(by='model_no')['absLpst'].min()
modelLpst2=orderPool.groupby(by='model_no')['absLpst'].max()





Md={}
for k, v in modelDict.items():
    if v in Md.keys():
        #modelindex[v]=[]
        Md[v].append(k)
    else:
        Md[v]=[k]


N=dict([(modelList[i],modelList[i]) for i in range(len(modelList))])

#abslpst=orderPool[['model_no','order_id','absLpst']]

#lpst={}
#for i in modelList:
    #tempDidt={}
    #for j in orderList:
        #tempDidt[j]=abslpst['absLpst'][j]
       
#date_s=pd.Series(plan_dates)
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
dp_matrix['cum_day']=dp_matrix.groupby(['model_no','line_no'])['num_by_day'].cumsum()
#reform the speed to the form 


order_spd=adt.order_speed_df(dp_matrix,orderPool)
order_spd['cum_day']=order_spd.groupby(['order_id','line_no'])['num_by_day'].cumsum()

#三条产线同时作业该型号的最快时间
e={}
for i in modelList:
    temp_fst=pd.DataFrame(dp_matrix[dp_matrix['model_no']==i].groupby('day_process')['num_by_day'].sum())
    temp_fst['day_process']=temp_fst.index
    e[i]=adt.process_csum(modelPool[i],temp_fst)+modelEP[i]
#fast speed
#fst=dp_matrix.groupby(by=['model_no','day_process'])['num_by_day'].sum()

#earlist model finish time
Tm={}
for i in modelList:
    tempL=[]
    for m in range(int(e[i]),modelLpst2[i]+1):
        tempL.append(m)
    Tm[i]=tempL

#
#同理，三条产线同时作业订单的最快时间，到订单的最早完成时间
oe={}
for i in modelList:
    temp={}
    temp_fst=pd.DataFrame(dp_matrix[dp_matrix['model_no']==i].groupby('day_process')['num_by_day'].sum())
    for j in Md[i]:
        temp[j]=adt.process_csum(orderPool[orderPool['model_no']==i]['order_num'][j],temp_fst)+orderPool['absEpst'][j]
    oe[i]=temp
T={}
for i in modelList:
    temP={}
    for j in Md[i]:
        tempL=[]
        for m in range(int(oe[i][j]),modelLpst2[i]+1):
            tempL.append(m)
        temP[j]=tempL
    T[i]=temP
#每条产线总运行时间下，所有可能的时间t
TL=[]
for i in range(0,orderPool['absLpst'].max()+1):
    TL.append(i)
#根据TL 算出每条产线的capacity during time t
R={}
for l in prod_line:
    tempR={}
    for t in TL:
        tempR[t]=1
    R[l]=tempR

Tn={}
for i in modelList:
    tempL=[]
    for m in range(modelEP[i],modelLpst2[i]+1):
        tempL.append(m)
    Tn[i]=tempL
#learning df to learning dict
P={}
for i in modelList:
    tempTable=dp_matrix[dp_matrix['model_no']==i]
    tempm={}
    for l in prod_line:
       tempdf=tempTable[tempTable['line_no']==l][['day_process','cum_day']]
       a_dict={}
       a_dict[0]=tempdf['day_process'].tolist()
       a_dict[0].insert(0,0)
       a_dict[1]=tempdf['cum_day'].tolist()
       a_dict[1].insert(0,0)
       #a_dict[2]=len(a_dict[0])
       tempm[l]=a_dict
    P[i]=tempm

#same thing but in different form       
Pv={}
for i in modelList:
    tempTable=dp_matrix[dp_matrix['model_no']==i]
    tempm={}
    for l in prod_line:
       tempdf=tempTable[tempTable['line_no']==l][['day_process','cum_day']]
       tempdf.index=tempdf['day_process']
       a_dict={}
       loop=tempdf['day_process'].tolist()
       for d in loop:
           a_dict[d]=tempdf['cum_day'][d]
           
       tempm[l]=a_dict
    Pv[i]=tempm
    
x_comb={}
for i in modelList:
    tempL=[]
    for j in Md[i]:
        
        for item in T[i][j]:
            tempL.append((N[i],j,item))
    x_comb[i]=tempL

h_comb={}
for i in modelList:
    tempL=[]
    for item in Tm[i]:
        tempL.append((N[i],item))            
    h_comb[i]=tempL
    
qls_comb={}
for i in modelList:
    tempL=[]
    for l in prod_line:
        for t in TL:
            tempL.append((N[i],l,t))
    qls_comb[i]=tempL
    

k_comb={}
for i in modelList:
    tempL=[]
    for l in prod_line:
        for item in P[i][l][0]:
            tempL.append((N[i],l,item))
    k_comb[i]=tempL        

prob=pulp.LpProblem("The APS Problem",pulp.LpMinimize)
x={}
h={}
LS={}
zz ={}
QLS={}
k={}
modeln=len(modelList)
for i in modelList:
    #a variable which is one if order j of the model i is completed in time t
    x[i]=pulp.LpVariable.dicts('x',x_comb[i],0,1,pulp.LpInteger)
    
    # a variable which is 1 in period t if all orders of model i
    #have been comlpeted , 0 otherwise
    h[i]=pulp.LpVariable.dicts('h',h_comb[i],0,1,pulp.LpInteger)
    
    #a variable which is 1 if the line is assigned to complete model i during period t
    #LS[i]=pulp.LpVariable('ls',(N[i],Md[i],L),0,1,pulp.LpInteger)
    QLS[i]=pulp.LpVariable.dicts('qls',qls_comb[i],0,1,pulp.LpInteger)
    
    #zz[i]=pulp.LpVariable('zz',(N[i],Md[i],T[i]),0,1,pulp.LpInteger)
    
    k[i]=pulp.LpVariable.dicts('k',k_comb[i],0,1,pulp.LpContinuous)
        
    
    
#Csums=pulp.LpVariable.dicts("line_prod",(prod_line,orderList),0,None, pulp.LpInteger)
#r=pulp.LpVariable.dicts("release",(prod_line,orderList),0)
#compD=pulp.LpVariable.dicts("compDate",(prod_line,orderList),0)
#CLines=pulp.LpVariable("CLines",[j for j in line_date] ,0) #total amount of all lines by day
#Pday=pulp.LpVariable.dicts("Processdays",(prod_line,orderList),0)
#AM=pulp.LpVariable.dicts('planAmountEveryorder',(prod_line,orderList,plan_dates),0)
#Create the 'prob' variable to contain the problem data
#prob=pulp.LpProblem("The APS Problem",pulp.LpMinimize)

#objective function： consider order priority and leadtime
#eps=1e-2 
#lambda compD[l][o] if compD[l][o]<=len(plan_dates) else len(plan_dates)
#adt.model_total_volume(order_spd[(order_spd['order_id']==o)&(order_spd['line_no']==l)][['day_process','num_by_day']],adt.prod_days(compD[l][o],len(plan_dates),r[l][o]),len(plan_dates))
prob+=pulp.lpSum([x[i][(i,j,t)]*(t-g[i][j]) for i in modelList for j in Md[i] for t in T[i][j] if t>g[i][j]])+pulp.lpSum([0.5*k[i][(i,l,m)]*P[i][l][0][m] for i in modelList for l in prod_line for m in P[i][l][0]])
#pulp.lpSum([orderPool['priority'][o]*orderPool['order_type'][o]*\
                  #Csums[l][o] for o in orderList for l in prod_line])

#prob+=Cmax+eps*lpSum([r[j] for j in order_line])-eps*[compD[j] for j in order_line]
#The constraints
#1. every order has to be completed before due date
#2. relationships between release date and due date
#3. release date>=max(0,epst-plan_dates[0]) 
#4.fixed sum across day and lines equal total num of orders
for i in modelList:
    #prob+=pulp.lpSum([LS[i][i][l] for l in prod_line])>=1
    #prob+=pulp.lpSum([k[i][(i,l,m)] for l in prod_line for m in P[i][l][0]])==pulp.lpSum([LS[i][(i,j,l)] for j in Md[i] for l in prod_line])
    #限定分割总量
    prob+=pulp.lpSum([k[i][(i,l,m)]*P[i][l][1][m] for l in prod_line for m in P[i][l][0]])>=modelSum[i]
    #限定完成只出现一次
    prob+=pulp.lpSum([h[i][(i,t)] for t in Tm[i]])==1
    #限定订单总量即型号总量，x与h的关系
    prob+=pulp.lpSum([x[i][(i,j,t)]*orderD[i][j] for j in Md[i] for t in T[i][j]])==pulp.lpSum([h[i][(i,t1)]*modelSum[i] for t1 in Tm[i]])
    for l in prod_line:
        #限定k的取值
        prob+=pulp.lpSum([k[i][(i,l,m)] for m in P[i][l][0]])==1
        prob+=pulp.lpSum([k[i][(i,l,m)]*P[i][l][0][m] for m in P[i][l][0]])+modelEP[i]<=pulp.lpSum([h[i][(i,t)]*t for t in Tm[i]])
        #prob+=pulp.lpSum([QLS[i][i][l][t4] for t4 in TL])==pulp.lpSum([k[i][i][l][m]*P[i][l][0][m] for m in P[i][l][0]])
    for j in Md[i]:
        #限定x=1只能出现一次
        prob+=pulp.lpSum([x[i][(i,j,t)] for t in T[i][j]])==1
        #缩小x出现的时间点
        prob+=pulp.lpSum([x[i][(i,j,t)] for t in T[i][j] if t<=oe[i][j]])==0
    
    for t3 in Tm[i]:
        #限定x与h的关系
        prob+=pulp.lpSum([x[i][(i,j,t4)] for j in Md[i] for t4 in T[i][j] if t4<=t3])>=pulp.lpSum([h[i][(i,t3)]*len(Md[i])])
    
for l in prod_line:
    prob+=pulp.lpSum([k[i][(i,l,m)]*P[i][l][0][m] for i in modelList for m in P[i][l][0]])<=sum([R[l][t] for t in TL])       
        #prob+=compD[l][o] <= Cmax[l][o]
        #prob+=compD[l][o] >=r[l][o]+Csums[l][o]*(process_days[o][l]/orderPool['order_num'][o])
        
        #prob+=r[l][o]+Pday[l][o]<=(orderPool['deli_date'][o]-datetime.datetime.strptime(plan_dates[0],'%Y-%m-%d')).days
        #prob+=r[l][o]>=max(0,(orderPool['epst'][o]-datetime.datetime.strptime(plan_dates[0],'%Y-%m-%d')).days)
    #prob+=pulp.lpSum([order_spd[(order_spd['order_id'==o])&(order_spd['line_o']==l)&(order_spd['day_process']==Pday[l][o])] for l in prod_line])==orderPool['order_num'][o]
    #prob+=compD[l][o]<=(orderPool['deli_date'][o]-datetime.datetime.strptime(plan_dates[0],'%Y-%m-%d')).days
#prob+=pulp.lpSum([Csums[l][o] for l in prod_line for o in orderList])==orderPool['order_num'].sum()
#5.every line cannot made two orders at the same time

#eps=1e-2 
#for o in orderList:
    #prob+=Cmax+eps*pulp.lpSum([r[l][o] for l in prod_line])-eps*pulp.lpSum([compD[l][o] for l in prod_line])   
    
prob.writeLP("APSModel.lp")
prob.solve()
print("Status:", pulp.LpStatus[prob.status])



#for o in orderList:
    #for l in prod_line:
        #print((l,o),r[l,o].value(),compD[l,o].value(),Cmax[l,o].value())
#a=[]
#for v in prob.variables():
    #print(v.name, "=", v.varValue)
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
 