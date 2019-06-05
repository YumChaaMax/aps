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
            if Duration[i-1][j-1] <>0:
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

def EFP (n,j) :
Templl = Arrival [n][j] + DurationPortion [n][j]
for k in range (P[n +1]) :
if Precedence [n][j][k ]==1:
temp = EFP(n,k) - DurationPortion [n][k] + ( DurationPortion [n][k
]/
Batch [n][k]) + DurationPortion [n][j]
tempp = EFP(n,k) + DurationPortion [n][j]/ Batch [n][j]
if temp > Templl :
Templl = temp
if tempp > Templl : Templl = tempp
else :
if tempp > Templl :
69
Templl = tempp
return Templl
n = 0
l= [[] for x in xrange (len(P) )]
while n<len(P):
for j in range (P[n +1]) :
l[n]. append (int( round (EFP(n,j) +0.4999) ) )
n+=1
for i in I:
deletlist =[]
for j in range ( Project [i -1]) :
if RS[i -1][ j ]==0:
for k in range ( Project [i -1]) :
Precedence [i -1][ k][j]=0
for z in range ( Project [i -1]) :
Precedence [i -1][ j][z]=0
if Process == ’ Planning ’:
EFP (i -1 ,k)
l[i -1][ k]= int( round (EFP(i -1 ,k) +0.4999) )
LFP (i -1 ,k)
u[i -1][ k]= int( round (LFP(i -1 ,k) +0.4999) )
else :
EF(i -1 ,k)
l[i -1][ k]= int( round (EF(i -1 ,k) +0.4999) )
LF(i -1 ,k)
u[i -1][ k]= int( round (LF(i -1 ,k) +0.4999) )
deletlist . append (j+1)
else :
continue
for x in deletlist :
J[i]. remove (x)
70
# print ’ Latest Finish ’
# print u
# print ’ Earliest Finish ’
# print l
for i in I:
if len (J[i]) <=P[i]:
P[i]= len(J[i])
else :
continue
deletjob =[]
for i in I:
if not J[i]:
deletjob . append (i)
for x in deletjob :
I. remove (x)
if Process == ’ Planning ’:
for i in I:
for j in J[i]:
if LFC [i -1][j -1] >0:
LFC [i -1][j -1]= round (LFC [i -1][j -1]/8+0.4999)
if LFC [i -1][j -1] <=u[i -1][j -1]:
u[i -1][j -1]= int(LFC[i -1][j -1])
if Process <>’ Planning ’:
for i in I:
for j in J[i]:
if LF(i -1 ,j -1) >0:
if LF(i -1 ,j -1) <=u[i -1][j -1]:
u[i -1][j -1]= int(LF(i -1 ,j -1) )
ADD =[]
for i in I:
ADD . append ( AbsoluteDueDate [i -1])
71
print ’* DATA ARE IMPORTED ... ’
# earliest possible period in which project i could be completed
ee =[]
for i in I:
x=[]
for j in J[i]:
x. append (l[i -1][j -1])
eee =max (x)
ee. append (eee )
e= dict (zip(I,ee))
# priority of project i
w= dict (zip(I, Weight ))
# time interval 1
T= dict (zip(I ,( range (min( Arrival [i -1]) , AbsoluteDueDate [i -1]+1)
for i in I)) )
# time interval 2
T2= range (0 , max (ADD ) +1)
# time interval 3
T3= {}
for i in I:
for j in J[i]: T3[i,j]= range (l[i -1][j -1] ,u[i -1][j -1]+1)
# time interval 4
T4 ={}
for i in I:
72
for j in J[i]: T4[i,j]= range (l[i -1][j -1] , AbsoluteDueDate [i
-1]+1)
# time interval 5
T5 ={}
for i in I:
for j in J[i]: T5[i,j]= range (l[i -1][j -1] ,u[i -1][j -1]+1)
# time interval 6
TeG ={}
for i in I: TeG [i]= range (e[i] , AbsoluteDueDate [i -1]+1)
# time interval 7
Tal ={}
for i in I:
for j in J[i]: Tal [i,j]= range ( Arrival [i -1][j -1] ,l[i -1][j -1])
# time interval 8
TuG ={}
for i in I:
for j in J[i]: TuG [i,j]= range (u[i -1][j -1]+1 , AbsoluteDueDate [i
-1]+1)
# time interval 9
T1e = dict (zip (I ,( range (min ( Arrival [i -1]) ,e[i]) for i in I)) )
R={}
for m in M:
for t in T2: R[m,t]=1
V={}
for o in O:
for t in T2: V[o,t]=1
73
# desired due date for project i
g= dict (zip(I ,(( DesiredDueDate [i -1]) for i in I) ))
# a variavle which is 1 if job j in project i is completed in
period t ,
0 otherwise
x={}
for i in I: x[i] = LpVariable . dicts (’x ’ ,(N[i -1] ,J[i] ,T[i]) ,0 ,1 ,
LpInteger )
# a variable which is 1 in period t if all jobs of project i
have been
comlpeted , 0 otherwise
h={}
for i in I: h[i] = LpVariable . dicts (’h ’ ,(N[i -1] , TeG[i]) ,0 ,1 ,
LpInteger )
# a varibale which is 1 within a duration of job j in project i
zz ={}
for i in I: zz[i] = LpVariable . dicts (’ zz ’ ,(N[i -1] ,J[i],T[i])
,0 ,1 , LpInteger )
# a variable which is 1 if mach
74
for i in I: W[i] = LpVariable . dicts (’W ’ ,(N[i -1] ,J[i] ,O) ,0 ,1 ,
LpInteger )
# a variable which is used to assisst constraint 5
QS ={}
for i in I: QS[i] = LpVariable . dicts (’ QS ’ ,(N[i -1] ,J[i] ,M,T[i])
,0 ,1 , LpInteger )
# a variable which is used to assisst constraint 6
QW ={}
for i in I: QW[i] = LpVariable . dicts (’ QW ’ ,(N[i -1] ,J[i] ,O,T[i])
,0 ,1 ,
LpInteger )
# a variable which is 1 during the period that a setup for a
step is
completed but the processing has not been
started yet - This is only used for machine utilization
zzs ={}
for i in I: zzs[i] = LpVariable . dicts (’ zzs ’ ,(N[i -1] ,J[i] ,T[i])
,0 ,1
,LpInteger )
# a variable which is 1 if a machine is utilized during a period
defined for zzs
QQS ={}
for i in I: QQS[i] = LpVariable . dicts (’ QQS ’ ,(N[i -1] ,J[i] ,M,T[i])
,0 ,1 , LpInteger )
Time_Start = time . clock ()
print ’* VARIABLES ARE GENERATED , THE MODEL IS BEING PROCESSED ...
’,’ ## ’,Process ,’ ## ’