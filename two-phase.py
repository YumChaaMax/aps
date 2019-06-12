# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 12:07:39 2019

@author: Max
"""

import numpy as np
import xlrd
import time
import datetime
import matplotlib . pyplot as plt
import sys
import shutil
import os
from matplotlib . ticker import MultipleLocator ,
FormatStrFormatter
from datetime import datetime
print("#",datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'#')
book = xlrd.open_workbook ("datanew.xls")
sheet = book.sheet_by_index(18)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
for i in xrange(sheet.nrows):
    for j in xrange(sheet.ncols):
        Process = sheet.cell_value (i,j)
# print ’ Process ’, Process
sheet=book.sheet_by_index(0)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet.nrows , sheet . ncols )
Project =[]
for i in xrange(sheet.nrows) :
    for j in xrange(sheet.ncols) :
        Project.append(int(sheet.cell_value(i,j)))
# print ’ Project ’, Project
sheet = book.sheet_by_index (1)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,56 sheet .nrows , sheet . ncols )
ActualDuration = []
for i in xrange(sheet.nrows):
    ActualDuration.append(sheet.row_values(i))
for i in xrange(sheet.nrows):
    while ' ' in ActualDuration [i]:
        ActualDuration [i]. remove (' ')
# print ’ Actual Duration ’, ActualDuration
sheet = book.sheet_by_index (11)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
InflationRate = []
for i in xrange(sheet.nrows):
    InflationRate.append(sheet.row_values(i))
for i in xrange ( sheet . nrows ) :
    while '' in InflationRate[i]:
        InflationRate[i].remove ('')
# print ’ InflationRate ’, InflationRate
#
#
sheet = book.sheet_by_index (4)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )

AbsoluteDueDate = []
for i in xrange(sheet.nrows):
    for j in xrange(sheet.ncols):
        AbsoluteDueDate.append(int(sheet.cell_value (i,j)))
# print ’ AbsoluteDueDate ’, AbsoluteDueDate
#
#
sheet = book.sheet_by_index(3)
#57
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
DesiredDueDate = []
for i in xrange(sheet.nrows):
    for j in xrange(sheet.ncols):
        DesiredDueDate.append(int(sheet.cell_value(i,j)))
# print ’ DesiredDueDate ’, DesiredDueDate
#
#
sheet=book.sheet_by_index(10)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
Weight = []
for i in xrange(sheet.nrows):
    for j in xrange (sheet.ncols ) :
        Weight.append(int(sheet.cell_value(i,j)))
# print ’ Weight ’, Weight
#
#
sheet = book.sheet_by_index(2)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
Arrivall =[]
Arrival =[]
for i in xrange (sheet.nrows) :
    Arrivall.append(sheet.row_values(i))
for i in xrange(sheet.nrows):
    while '' in Arrivall[i]:
        Arrivall[i].remove('')

for i in range(len(Project)):
    Arrival.append(map(int,Arrivall[i]))
# print ’ Arrival ’, Arrival
#
#
sheet = book.sheet_by_index(5)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
PrecedenceN =[]
for i in xrange(sheet.nrows):
    PrecedenceN.append(sheet.row_values(i))
for i in xrange(sheet.nrows):
    while '' in PrecedenceN [i]:
        PrecedenceN[i].remove(' ')
# print ’ Precedence ’
Precedence = []
z = 0
for n in Project:
    n = z+n
    Precedence.append(PrecedenceN[z:n])
    z = n
# print Precedence
#
#
sheet=book.sheet_by_index(13)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
RS = []
for i in xrange(sheet.nrows):
    RS.append(sheet.row_values(i))
for i in xrange(sheet.nrows):
    while '' in RS[i]:
        RS[i]. remove ('')
# print ’ RemainingStatus ’, RS
#
#
# Auxilary
TotProj =len(Project)
IAux = range(1,TotProj +1)
JAux = dict(zip(IAux,(range(1,Project[i-1]+1) for i in IAux ) ))
#
#
Duration =[]
for i in IAux :
    InflatedDuration =[]
    for j in JAux[i]:
        InflatedDuration.append(round(ActualDuration[i-1][j-1]*InflationRate[i-1][j-1]))
    Duration.append(InflatedDuration)
#
#
for i in IAux :
    for j in JAux[i]:
        if RS[i -1][j -1] > 0:
            Duration[i-1][j-1]=(round(Duration[i -1][j -1]*RS[i -1][j-1]+0.4999))
        else:
            continue

# print ’ Duration ’, Duration
# print ’ DoubleCheckDuration ’, Duration
#
#
sheet = book.sheet_by_index (12)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
Batch = []
for i in xrange(sheet.nrows):
    Batch.append(sheet.row_values(i))
for i in xrange(sheet.nrows):
    while '' in Batch [i]:
        Batch[i].remove ('')
# print ’ Batch ’, Batch
#
#
l= [[] for x in xrange(len(Project))]

#this function does not make sense 
def EF(n,j):
    
    Templl = Arrival[n][j]+Duration[n][j]
    for k in range(Project[n]):
        if Precedence[n][j][k]==1:
            temp = EF(n,k)-Duration[n][k]+round((Duration[n][k]/Batch[n][k])+0.49999)+Duration[n][j]
            tempp = EF(n,k) + round((Duration[n][j]/Batch[n][j]) +0.49999)
    
            if temp > Templl :
                Templl = temp
            if tempp > Templl : 
                Templl = tempp
        
            
    return Templl

n = 0
while n<len(Project):
    for j in range (Project[n]):
        l[n].append (int(EF(n,j) ))
    n+=1
# print ’ Earliest Finish ’
# print l
#
#
def LF(n,j) :
    TempU = AbsoluteDueDate[n]
    for k in range(Project[n]):
        if Precedence [n][k][j]==1:
            temp = LF(n,k)-Duration[n][k]
            if temp < TempU : TempU = temp
    return TempU

u= [[] for x in xrange(len(Project))]
n = 0
while n<len( Project ):
    for j in range(Project[n]):
        u[n].append(int(LF(n,j)))
    n+=1
# print ’ Latest Finish ’
# print u
#
#
sheet = book.sheet_by_index(8)

# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )

Operatorr =[]
for i in xrange(sheet.nrows) :
    Operatorr.append(sheet.row_values(i))
OperatorReq = []
z = 0
for n in Project:
    n = z+n
    OperatorReq.append(Operatorr[z:n])
    z = n
# print ’ OperatorReq ’
# print OperatorReq
#
#
sheet = book . sheet_by_index (14)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )

CC = []
CCC = []
for i in xrange(sheet.nrows):
    CCC.append(sheet.row_values(i))
for i in xrange(sheet.nrows):
    while '' in CCC[i]:
        CCC[i]. remove ('')
        
for i in range(len(Project)):
    CC.append(map(int,CCC[i]))
# print ’ CompletionConstraint ’
# print CC
#
#

sheet = book.sheet_by_index(9)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
OperatorPartialUsage =[]
for i in xrange(sheet.nrows):
    OperatorPartialUsage.append(sheet.row_values (i))
Opu = []
z = 0
for n in Project :
    n = z+n
    Opu.append(OperatorPartialUsage[z:n])
    z = n
# print ’ OperatorPartialUsage ’
# print Opu
#
#
sheet = book.sheet_by_index(7)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
MachinePartialUsage =[]
for i in xrange(sheet.nrows):
    MachinePartialUsage.append(sheet.row_values(i))
Mpu = []
z = 0
for n in Project :
    n = z+n
    Mpu. append ( MachinePartialUsage [z:n])
    z = n
# print ’ MachinePartialUsage ’
# print Mpu

#
#
Machinee = []
sheet = book.sheet_by_index (6)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
for i in xrange(sheet.nrows):
    Machinee.append(sheet .row_values(i))

# print MC
#
#
sheet = book.sheet_by_index(16)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
OC = []
OCC =[]
for i in xrange(sheet.nrows):
    OCC.append(sheet.row_values(i))
for i in xrange(sheet.nrows):
    while ' ' in OCC[i]:
        OCC[i].remove(' ')
for i in range(len(Project)):
    OC.append(map(int,OCC [i]))
# print ’ OperatorConstraint ’
# print OC
#
#
sheet = book.sheet_by_index (17)
# print ’ Worksheet Names : % s ; Rows : %s ; Columns : % s ’% ( sheet . name
#,sheet .nrows , sheet . ncols )
LFC = []
for i in xrange(sheet.nrows):
    LFC.append(sheet.row_values(i) )
for i in xrange (sheet.nrows):
    while '' in LFC[i]:
        LFC[i].remove (' ')
# print ’ LastestFinishConstranit ’
# print LFC

# Import PuLP modeler functions
from pulp import *
# Create the ’ prob ’ variable to contain the problem data
prob=LpProblem("The Optimzation Problem",LpMinimize)
# ## - - - - - Sets - - - - -###
# number of projects
ProjNum =len(Project)

# set of project numbers
I = range(1,ProjNum +1)

# index auxilary
N =[[] for x in xrange(len(Project))]
for i in I:
    N[i -1].append(i)
    
# number of jobs in Project i
P = dict(zip(I,((Project [i-1]) for i in I)))

# set of jobs in project i
J= dict(zip(I,(range(1,Project[i-1]+1) for i in I)))

# number of machine types
Machine =22

# set of machine types
M= range (1 , Machine +1)

# number of operator types
Operator =14

# set of operators types
O=range(1,Operator+1)
for i in I:
    for j in J[i]:
        if Duration[i-1][j-1]==0:
            RS[i-1][j-1]=float(0)
            
if Process == 'Planning':
    DurationPortion =[]
    for i in I:
        DP =[]
        AbsoluteDueDate[i-1]= int(round((AbsoluteDueDate[i-1]/8.0)+0.4999))
        DesiredDueDate[i-1]= int(round((DesiredDueDate [i-1]/8.0) +0.4999))
        for j in J[i]:
            if Duration[i-1][j-1]!=0:
                DP.append(Duration[i-1][j-1]/8.0)
                Arrival[i-1][j-1]=int(round((Arrival[i-1][j-1]/8.0)+0.4999))
                for m in M:
                    Mpu[i-1][j-1][m-1]=Mpu[i-1][j-1][m-1]*((Duration[i-1][j-1]/8.0)/(round((Duration[i-1][j-1]/8.0)+0.4999)))
                for o in O:
                    Opu[i-1][j-1][o-1]= Opu[i-1][j-1][o-1]*((Duration[i-1][j-1]/8.0)/(round((Duration[i-1][j-1]/8.0)+0.4999)))
                    Duration [i-1][j-1]= round((Duration[i-1][j-1]/8.0)+0.4999)
            else :
                Duration[i-1][j-1]=0.001
                DP.append(Duration[i-1][j-1]/8.0)
                Arrival[i-1][j-1]=int(round((Arrival[i-1][j-1]/8.0)+0.4999))
                for m in M:
                    Mpu[i-1][j-1][m-1]=Mpu[i-1][j-1][m-1]*((Duration[i-1][j-1]/8.0)/(round((Duration[i-1][j-1]/8.0)+0.4999)))

                for o in O:
                    Opu[i-1][j-1][o-1]= Opu[i-1][j-1][o-1]*((Duration[i-1][j-1]/8.0)/(round((Duration[i-1][j-1]/8.0)+0.4999)))
                    Duration [i-1][j-1]= round((Duration[i-1][j-1]/8.0)+0.4999)

        DurationPortion.append(DP)
# print ’ DurationPortion ’, DurationPortion
def LFP (n,j) :
    TempU = AbsoluteDueDate[n]
    for k in range (P[n +1]) :
        if Precedence[n][k][j]==1:
            temp = LFP(n,k) - DurationPortion[n][k]
            if temp < TempU : TempU = temp
    return TempU

n = 0
u= [[] for x in xrange (len(P))]
while n<len(P):
    for j in range(P[n +1]) :
        u[n].append (int( round (LFP(n,j)+0.4999) ) )
    n+=1

def EFP(n,j):
    Templl = Arrival [n][j] + DurationPortion [n][j]
    for k in range (P[n +1]) :
        if Precedence[n][j][k]==1:
            temp = EFP(n,k)-DurationPortion[n][k]+(DurationPortion[n][k]/Batch[n][k])+DurationPortion[n][j]
            tempp = EFP(n,k) + DurationPortion [n][j]/ Batch [n][j]
            if temp > Templl:
                Templl = temp
            if tempp > Templl: Templl = tempp
        else :
            if tempp > Templl:
                Templl = tempp
    return Templl

n = 0
l= [[] for x in xrange (len(P) )]
while n<len(P):
    for j in range (P[n +1]) :
        l[n].append(int(round(EFP(n,j)+0.4999) ) )
n+=1
for i in I:
    deletlist =[]
    for j in range(Project[i-1]) :
        if RS[i-1][j]==0:
            for k in range(Project[i-1]) :
                Precedence [i-1][k][j]=0
                for z in range (Project[i-1]) :
                    Precedence[i-1][j][z]=0
                    if Process == 'Planning':
                        #EFP(i-1 ,k)
                        l[i-1][k]= int(round(EFP(i-1 ,k)+0.4999))
                        #LFP (i-1 ,k)
                        u[i-1][k]= int(round(LFP(i-1 ,k)+0.4999))
                    else :
                        #EF(i -1 ,k)
                        l[i-1][k]=int(round(EF(i-1,k) +0.4999))
                        #LF(i -1 ,k)
                        u[i-1][k]= int(round(LF(i-1 ,k)+0.4999) )
            deletlist.append (j+1)
        else :
            continue
for x in deletlist:
    J[i].remove(x)

# print ’ Latest Finish ’
# print u
# print ’ Earliest Finish ’
# print l
for i in I:
    if len(J[i])<=P[i]:
        P[i]= len(J[i])
    else:
        continue
    
deletjob =[]
for i in I:
    if not J[i]:
        deletjob.append(i)
for x in deletjob :
    I.remove (x)
    if Process =='Planning':
        for i in I:
            for j in J[i]:
                if LFC[i-1][j-1]>0:
                    LFC [i-1][j-1]= round(LFC[i-1][j-1]/8+0.4999)
                if LFC[i-1][j-1] <=u[i-1][j-1]:
                    u[i-1][j-1]= int(LFC[i-1][j-1])

    if Process !='Planning':
        for i in I:
            for j in J[i]:
                if LF(i-1 ,j-1) >0:
                    if LF(i-1 ,j-1) <=u[i-1][j-1]:
                        u[i-1][j-1]= int(LF(i-1 ,j-1))
ADD =[]
for i in I:
    ADD.append(AbsoluteDueDate[i-1])

    print('* DATA ARE IMPORTED ... ')
# earliest possible period in which project i could be completed
ee =[]
for i in I:
    x=[]
    for j in J[i]:
        x. append (l[i -1][j -1])
        eee =max (x)
        ee. append (eee)
e=dict(zip(I,ee))
# priority of project i
w= dict(zip(I, Weight))
# time interval 1
T= dict(zip(I,(range(min(Arrival[i-1]),AbsoluteDueDate[i-1]+1) for i in I)))
# time interval 2
T2=range(0,max(ADD)+1)
# time interval 3
T3= {}
for i in I:
    for j in J[i]:T3[i,j]=range(l[i-1][j-1] ,u[i-1][j-1]+1)
# time interval 4
T4 ={}
for i in I:
    for j in J[i]: T4[i,j]= range(l[i-1][j-1] , AbsoluteDueDate[i-1]+1)
# time interval 5
T5 ={}
for i in I:
    for j in J[i]: T5[i,j]= range(l[i-1][j-1] ,u[i-1][j-1]+1)
# time interval 6
TeG ={}
for i in I: TeG [i]= range(e[i], AbsoluteDueDate[i -1]+1)
# time interval 7
Tal ={}
for i in I:
    for j in J[i]: Tal[i,j]= range(Arrival[i-1][j-1] ,l[i-1][j-1])
# time interval 8
TuG ={}
for i in I:
    for j in J[i]: TuG[i,j]=range(u[i-1][j-1]+1 , AbsoluteDueDate[i-1]+1)
# time interval 9
T1e = dict(zip(I,(range(min(Arrival[i -1]) ,e[i]) for i in I)) )
R={}
for m in M:
    for t in T2: R[m,t]=1
V={}
for o in O:
    for t in T2: V[o,t]=1

# desired due date for project i
g=dict(zip(I,((DesiredDueDate[i-1]) for i in I) ))

# a variable which is 1 if job j in project i is completed in
#period t ,0 otherwise
x={}
for i in I: x[i] = LpVariable.dicts('x',(N[i-1] ,J[i] ,T[i]) ,0,1,LpInteger)

# a variable which is 1 in period t if all jobs of project i
#have been comlpeted , 0 otherwise
h={}
for i in I: h[i] = LpVariable.dicts('h',(N[i -1],TeG[i]),0,1,LpInteger)

# a varibale which is 1 within a duration of job j in project i
zz ={}
for i in I: zz[i] = LpVariable.dicts('zz',(N[i-1],J[i],T[i]),0,1,LpInteger)

# a variable which is 1 if mach
for i in I: W[i] = LpVariable.dicts ('W' ,(N[i -1],J[i],O),0,1,LpInteger)

# a variable which is used to assisst constraint 5
QS ={}
for i in I: QS[i]=LpVariable.dicts('QS' ,(N[i -1] ,J[i],M,T[i]),0,1,LpInteger)

# a variable which is used to assisst constraint 6
QW ={}
for i in I: QW[i] = LpVariable . dicts ('QW' ,(N[i-1],J[i],O,T[i]),0,1,LpInteger)

# a variable which is 1 during the period that a setup for a
#step is completed but the processing has not been
#started yet - This is only used for machine utilization
zzs ={}
for i in I: zzs[i] = LpVariable.dicts('zzs',(N[i-1],J[i],T[i]),0,1,LpInteger )

# a variable which is 1 if a machine is utilized during a period
#defined for zzs
QQS ={}
for i in I: QQS[i] = LpVariable.dicts('QQS',(N[i-1],J[i],M,T[i]),0,1,LpInteger )
Time_Start = time.clock()
print ('* VARIABLES ARE GENERATED , THE MODEL IS BEING PROCESSED ...',' ## ',Process ,' ##') 

       
# ----- Objective Function -----#
# a project is late if it is completed after the desired due -
#date , g[i]
prob += (sum(w[i]*((t-g[i])*h[i][i][t]) for i in I for t in TeG[i] if t >=g[i]+1)+sum(0.01*w[i]*h[i][i][t]*t for i in I for t in TeG[i]))
# ----- Subject To -----#
for i in I:
#job completion constraint 1
    prob += sum(h[i][i][t] for t in TeG [i]) == 1
# prob += sum(h[i][i][t] for t in T1e[i]) == 0
    for j in J[i]:
    # step completion constraint
        prob += sum(x[i][i][j][t] for t in T3[i,j] ) == 1
        prob += sum(x[i][i][j][t] for t in TuG[i,j]) == 0
        prob += sum(x[i][i][j][t] for t in Tal[i,j]) == 0
        if CC[i-1][j-1] >0:
            B = CC[i-1][j-1]
            prob += x[i][i][j][B]==1
# step duration
        for t in T[i]:
            prob += sum(x[i][i][j][t1] for t1 in T[i] if t1 >=t if t1 < t+ Duration[i -1][j -1] if t1 <= AbsoluteDueDate[i-1]) == zz[i][i][j][t]
    # prob += sum(zz[i][i][j][t] for t in T[i] if t >= AbsoluteDueDate
    #[i -1]+1)
    #== 0

# prob += sum(zz[i][i][j][t] for t in Tal[i,j] if Duration [i -1][j
#-1] <t-
#Duration [i -1][j -1]) == 0
# machine constraint auxilary
        prob += sum( MachineReq[i-1][j-1][m-1] for m in M) >= sum(S[i][i][j][m] for m in M)
        prob += sum( MachineReq[i-1][j-1][m-1] for m in M) <= sum (S[i][i][j][m] for m in M)* Machine
        prob += sum(S[i][i][j][m] for m in M) <= 1
        for m in M:
            prob += S[i][i][j][m] <= MachineReq [i-1][j-1][m-1]
            for t in T[i]:
                prob += zz[i][i][j][t]+S[i][i][j][m]-QS[i][i][j][m][t]*2 <= 1
                prob += zz[i][i][j][t]+S[i][i][j][m]-QS[i][i][j][m][t]*2 >= 0
    # machine constraint during a period , starting from setup
    #completion up to a begining of a corresponding processing
                prob += zzs[i][i][j][t]+S[i][i][j][m] - QQS [i][i][j][m][t]*2 <=1
                prob += zzs[i][i][j][t]+S[i][i][j][m] - QQS [i][i][j][m][t]*2 >=0
        if MC[i-1][j-1] >0:
            Y = MC[i-1][j-1]
            prob += S[i][i][j][Y]==1

# operator constraint auxilary
        prob += sum(OperatorReq[i-1][j-1][o-1] for o in O) >= sum(W[i][i][j][o] for o in O)
        prob += sum(OperatorReq[i-1][j-1][o-1] for o in O) <= sum(W[i][i][j][o]for o in O)*Operator

        prob += sum(W[i][i][j][o] for o in O) <= 1
        
        for o in O:
            prob += W[i][i][j][o] <= OperatorReq [i-1][j-1][o-1]
        for t in T[i]:
            prob += zz[i][i][j][t]+W[i][i][j][o] - QW[i][i][j][o][t]*2 <= 1
            prob += zz[i][i][j][t]+W[i][i][j][o] - QW[i][i][j][o][t]*2 >= 0

        if OC[i-1][j-1] >0:
            B = OC[i-1][j-1]
            prob += W[i][i][j][B]==1
    # cycle must be assigned to a machine that is assigned to its
    #corresponding setup
    for j in J[i]:
        if j%2 !=0:
            if j+1 in J[i]:
                for m in M:
                    prob += S[i][i][j][m]== S[i][i][j+1][ m]
# Machine constraint during the period in which the setup of a
#step is completed but the cycle has not been started yet
    for j in J[i]:
        if j%2 != 0:
            if j+1 in J[i]:
                for t in T[i]:
                    if Process == 'Planning':
                        if l[i-1][j-1]== l[i-1][j]:
                            prob += (sum(x[i][i][j][t1] for t1 in T[i] if t1 >=l[i -1][j -1] if t1 <=t)-sum\
                                     (x[i][i][j+1][t1] for t1 in T[i] if t1 >=l[i-1][j] if t1 <=t+Duration [i -1][ j]))== zzs[i][i][j][t]
                        else:
                            prob += ( sum(x[i][i][j][ t1] for t1 in T[i] if t1 >=l[i -1][j -1] if\
                                          t1 <t)-sum(x[i][i][j +1][ t1] for t1 in T[i] if t1 >=l[i -1][j -1] if t1 \
                                               <t+Duration[i-1][j]))== zzs[i][i][j][t]
            else:
                prob += sum(x[i][i][j][t1] for t1 in T[i] if t1 >=l[i-1][j-1] if t1 <t)-sum(x[i][i][j +1][ t1] for t1 in T[i] \
                           if t1 >l[i -1][j -1] if t1 <t+Duration [i-1][j]) == zzs[i][i][j][t]
# project completion constraint 2
    for t2 in TeG [i]:
        prob += sum(x[i][i][j][t] for j in J[i] for t in T3[i,j] if t <= t2) >= (h[i][i][t2])*P[i]
# Sequencing constraint
#for j1 in J[i]:
# for j2 in J[i]:
# prob += Precedence [i -1][ j1 -1][ j2 -1]*( sum(t*x[i][i][ j2 ][
#t] for t in T5[i,j2 ])
#+ Duration [i -1][ j1 -1]) <= sum(t*x[i][i][ j1 ][t] for t in T5[i,j1 ])
    for j1 in J[i]:
        for j2 in J[i]:
            if Process == 'Planning':
# prob += Precedence [i -1][ j1 -1][ j2 -1]*( sum(t*x[i][i][ j2 ][t] for t
#in T5[i,j2 ]) -D
#uration [i -1][ j2 -1]+ DurationPortion [i -1][ j2 -1]) <=sum (t*x[i][i][ j1
#][t] for t in T5[i,j1 ]) - DurationPortion [i -1][ j1 -1]

                prob += Precedence [i-1][j1-1][j2-1]*(sum(t*x[i][i][j2][t] for t
                                   in T5[i,j2 ]) -Duration [i-1][j2-1]+(DurationPortion[i-1][j2-1]\
                                Batch[i -1][j2 -1]))<= sum(t*x[i][i][j1 ][t] for t in T5[i,j1])\
                                   - DurationPortion[i-1][j1-1]
               prob += Precedence [i -1][ j1 -1][ j2 -1]*( sum (t*x[i][i][ j2 ][t] for t
in T5[i,j2 ]) -Duration [i -1][ j2 -1]+ DurationPortion [i -1][ j2 -1]+(
DurationPortion [i -1][ j1 -1]/ Batch [i -1][ j1 -1]) )
<= sum(t*x[i][i][ j1 ][t] for t in T5[i,j1 ])
else :
prob += Precedence [i -1][ j1 -1][ j2 -1]*( sum (t*x[i][i][ j2 ][t] for t
in T5[i,j2 ])
-Duration [i -1][ j2 -1]+( Duration [i -1][ j2 -1]/ Batch [i -1][ j2 -1]) ) <=
sum (t*x[i][i][ j1 ][t]
for t in T5[i,j1 ]) -Duration [i -1][ j1 -1]
prob += Precedence [i -1][ j1 -1][ j2 -1]*( sum (t*x[i][i][ j2 ][t] for t
in T5[i,j2 ])+
( Duration [i -1][ j1 -1]/ Batch [i -1][ j1 -1]) )
<= sum(t*x[i][i][ j1 ][t] for t in T5[i,j1 ])
# machine and operator constraint
for t in T2:
for m in M:
prob += ( sum(QS[i][i][j][m][t]* Mpu [i -1][j -1][m -1] for i in I for
j in J[i] if t in T[i])+
sum(QQS[i][i][j][m][t]for i in I for j in J[i] if t in T[i])) <=
R[m,t]
for o in O:
prob += sum(QW[i][i][j][o][t]* Opu [i -1][j -1][o -1] for i in I for
j in J[i] if t in T[i]) <= V[o,t]
# prob . writeLP (" OptimizationProblem .lp ")
80
# Gurobi Solver
print '*LP MODEL IS GENERATED ---- Solver : GUROBI '
solvers . GUROBI_CMD ( path =None , keepFiles =0, mip =1, msg =1, options =[])
. solve ( prob )# options =
['TimeLimit =10 ']). solve ( prob )
# GLPK Solver
# solvers . GLPK_CMD ( path =None , keepFiles =0, mip =1, msg =1, options =[]) .
solve ( prob )# options =
['TimeLimit =10 ']). solve ( prob )
# COIN Solver
# print 'Solver : COIN '
# prob . solve ()
print (" Status :", LpStatus [ prob . status ])
print (" Objective = ", value ( prob . objective ))
Time_Elapsed = ( time . clock () - Time_Start )
print 'Computation Time ', Time_Elapsed
if LpStatus [ prob . status ]== 'Not Solved ':
# print 'The model could not provide a feasible solution '
sys . exit ("The model could not provide a feasible solution ")
print ""
JobCompletion = ""
print "#JOB COMPLETION TIME #"
for i in I:
JobCompletion = JobCompletion + "Job "+ repr (i)+" Completion_Time
:"
for t in TeG [i]:
if h[i][i][t]. value () ==1:
JobCompletion = JobCompletion + str(t)
81
else :
continue
print JobCompletion
JobCompletion = ""
print ""
CompletionTime = ""
print "# STEP COMPLETION TIME #"
for i in I:
print " **** Job "+ repr (i)+" **** "
for j in J[i]:
CompletionTime = " Step "+ repr (j)+": "
for t in T[i]:
if x[i][i][j][t]. value () ==1:
CompletionTime = CompletionTime +str (t)
else :
continue
print CompletionTime
CompletionTime = ""
print ""
ProcessingPeriods = ""
print "#JOB PROCESSING PERIODS #"
for i in I:
print " **** Job "+ repr (i)+" **** "
for j in J[i]:
ProcessingPeriods = ProcessingPeriods +" Step "+ repr (j)+": "+"(
"
for t in T[i]:
if zz[i][i][j][t]. value () ==1:
82
ProcessingPeriods = ProcessingPeriods + str(t)+" "
else :
continue
ProcessingPeriods = ProcessingPeriods + ")"
print ProcessingPeriods
ProcessingPeriods = ""
print ""
MachineUsagePeriod = ""
print "# Machine USAGE PERIOD #"
for m in M:
print " **** Machine "+ repr (m)+" **** "
print " Job - step - period "
for t in T2:
for i in I:
if t in T[i]:
for j in J[i]:
if QS[i][i][j][m][t]. value () ==1 or QQS [i][i][j][m][t]. value ()
==1:
print " "+str(i)+" "+str(j)+" "+str(t)
MachineUsagePeriod ="1"
else :
continue
if MachineUsagePeriod =="":
print "*** Machine "+ repr (m)+" was not used AT ALL ***"
else :
MachineUsagePeriod = ""
print ""
OperatorUsagePeriod = ""
83
print "# OPERATOR USAGE PERIOD #"
for o in O:
print " **** Operator "+ repr (o)+" **** "
print " Job - step - period "
for t in T2:
for i in I:
if t in T[i]:
for j in J[i]:
if QW[i][i][j][o][t]. value () ==1:
print " "+str(i)+" "+str(j)+" "+str(t)
OperatorUsagePeriod ="1"
else :
continue
if OperatorUsagePeriod =="":
print "*** Operator "+ repr (o)+" was not used AT ALL ***"
else :
OperatorUsagePeriod = ""
## GanttChart ##
Identitylist =[]
numpylist =[]
for i in I:
for j in J[i]:
for t in T[i]:
if zz[i][i][j][t]. value () ==1:
steplist =[]
steplist . append (i +0.05* j)
steplist . append (j)
steplist . append (t -1)
steplist . append (t)
Identitylist . append (str (i)+"-"+str (j))
numpylist . append ( steplist )
84
else :
continue
# print 'numpylist ', numpylist
ganttchart =np. array ( numpylist )
np. savetxt (" ganttchart .csv ", ganttchart , delimiter =",")
np. savetxt (" numpylist .csv ", numpylist , delimiter =",")
file = open (" Identitylist .txt ", "w")
for item in Identitylist :
file . write ("%s\n" % item )
file . close ()
plt . ylim (0, max (I)+1)
color = ['r', 'b', 'g', 'k', 'm', 'c', 'y']
color_mapper = np. vectorize ( lambda x: {1: 'r', 2: 'b', 3: 'g',
4: 'm', 5: 'c', 6: 'y', 7:
'r', 8: 'b', 9: 'g', 10: 'k', 11: 'm', 12: 'c', 13: 'y' ,14: 'k'}. get (x)
)
plt . hlines ( ganttchart [: ,0] , ganttchart [: ,2] , ganttchart [: ,3] ,
colors = color_mapper
( ganttchart [: ,1]) ,linewidth =5)
plt . title ('Jobs vs. Time ')
plt . ylabel ('Jobs ')
if Process == 'Planning ':
plt . xlabel ('Time ( days )')
else :
plt . xlabel ('Time ( hours )')
85
#plt. locator_params (' both ',1)
plt . yticks ( range (0, max (I)+1) )
plt . minorticks_on ()
plt . tick_params ( axis = 'both ', which = 'major ', labelsize = 10)
#plt. set_major_formatter ( majorFormatter )
x1 =0
x2 =1
x3 =2
x4 =3
n=0
while n<len( numpylist ):
x5= float ( numpylist [n][ x3 ]+ numpylist [n][ x4 ]) /2
plt. text (x5 , numpylist [n][ x1], Identitylist [n])
n+=1
plt. show ()
###
Identitymachine =[]
numpymachine =[]
for m in M:
for i in I:
for j in J[i]:
for t in T[i]:
if QS[i][i][j][m][t]. value () ==1:
steplist =[]
steplist . append (i)
steplist . append (j)
steplist . append (m +0.05* i)
steplist . append (t -1)
steplist . append (t)
86
Identitymachine . append (str(i)+"-"+str(j))
numpymachine . append ( steplist )
else :
continue
# print 'numpymachine ', numpymachine
ganttchartm =np. array ( numpymachine )
np. savetxt (" ganttchartm .csv ", ganttchartm , delimiter =",")
np. savetxt (" numpymachine .csv ", numpymachine , delimiter =",")
file = open (" Identitymachine .txt ", "w")
for item in Identitymachine :
file . write ("%s\n" % item )
file . close ()
plt . yticks ( range (len (M)+1) )
plt . ylim (0, len (M)+2)
plt . hlines ( ganttchartm [: ,2] , ganttchartm [: ,3] , ganttchartm [: ,4] ,
linewidth =4, colors
= color_mapper ( ganttchartm [: ,1]))
plt . title ('Machine Utilization ')
plt . ylabel ('Machine ')
if Process == 'Planning ':
plt . xlabel ('Time ( days )')
else :
plt . xlabel ('Time ( hours )')
x1 =0
x2 =1
x3 =2
x4 =3
x5 =4
87
n=0
while n<len( numpymachine ):
x6= float ((( numpymachine [n][ x4 ]+ numpymachine [n][ x5 ]) /2) +0.05*
numpymachine [n][ x2 ])
plt . text (x6 , numpymachine [n][ x3], Identitymachine [n])
n+=1
plt . show ()
###
Identityoperator =[]
numpyoperator =[]
for o in O:
for i in I:
for j in J[i]:
for t in T[i]:
if QW[i][i][j][o][t]. value () ==1:
steplist =[]
steplist . append (i)
steplist . append (j)
steplist . append (o +0.05* i)
steplist . append (t -1)
steplist . append (t)
Identityoperator . append (str(i)+"-"+str(j))
numpyoperator . append ( steplist )
else :
continue
# print ' numpyoperator ', numpyoperator
ganttcharto =np. array ( numpyoperator )
np. savetxt (" ganttcharto .csv ", ganttcharto , delimiter =",")
np. savetxt (" numpyoperator .csv ", numpyoperator , delimiter =",")
88
file = open (" Identityoperator .txt ", "w")
for item in Identityoperator :
file . write ("%s\n" % item )
file . close ()
# color_mapper = np. vectorize ( lambda x: {1: 'red ', 2: 'blue ', 3:
'green '}. get (x))
plt . yticks ( range (len (O)+1) )
plt . ylim (0, len (O)+2)
plt . hlines ( ganttcharto [: ,2] , ganttcharto [: ,3] , ganttcharto [: ,4] ,
linewidth =4,
colors = color_mapper ( ganttcharto [: ,1]) )
plt . title ('Operator Utilization ')
plt . ylabel ('Operator ')
if Process == 'Planning ':
plt . xlabel ('Time ( days )')
else :
plt . xlabel ('Time ( hours )')
x1 =0
x2 =1
x3 =2
x4 =3
x5 =4
n=0
while n<len( numpyoperator ):
x6= float ((( numpyoperator [n][ x4 ]+ numpyoperator [n][ x5 ]) /2) +0.05*
numpyoperator [n][ x2 ])
plt . text (x6 , numpyoperator [n][ x3], Identityoperator [n])
n+=1
plt . show ()
##if Process ==' Planning ':
89
## BusyPeriods =[]
## SchedulingPeriod =[]
## for t in T2:
## SchedulingPeriod1 =[]
## for i in I:
## if t in T[i]:
## for j in J[i]:
## if zz[i][i][j][t]. value () ==1:
## if t not in BusyPeriods :
## BusyPeriods . append (t)
## Schedule =[]
## Schedule . append (str(i)+" -"+ str(j))
## SchedulingPeriod1 . append ( Schedule )
## SchedulingPeriod . append ( SchedulingPeriod1 )
prevName = 'datanew .xls '
if Process == 'Planning ':
newName = ' datanewPlanning .xls '
else :
newName = ' datanewScheduling .xls '
shutil . copyfile ( prevName , newName )
print 'Computation Time ', Time_Elapsed       