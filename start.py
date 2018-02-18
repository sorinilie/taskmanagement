import os
import glob
import time
import sys
import math
import csv
import operator
import numpy

task_skill = [(line.rstrip('\n')).split(',') for line in open('2000tasks.csv')]
task_eta =[line.rstrip('\n') for line in open('task-eta.csv')]
skill_level=[(line.rstrip('\n')).split(',') for line in open('100people.csv')]


best=[[0 for x in range(100)] for y in range(2000)] 
r=[[0 for x in range(100)] for y in range(2000)] 

etas=[[0 for x in range(100)] for y in range(2000)] 


task_count=0
for ts in task_skill :
    sqsum_ts=sum( [int(ts[i])*int(ts[i]) for i in range(len(ts))] )
    skill_count=0
    for sl in skill_level :
        dot=sum( [int(sl[i])*int(ts[i]) for i in range(len(sl))] )
        sqsum_sl=sum( [int(sl[i])*int(sl[i]) for i in range(len(sl))] )
        r[task_count][skill_count]=dot/(math.sqrt(sqsum_sl)*math.sqrt(sqsum_ts))
        best[task_count][skill_count]=dot
        
        
        extra_eta=0
        for t, s in zip(ts, sl) :
            if (int(t)>int(s)) :
                extra_eta += (int(t)-int(s))/int(s)
            
        etas[task_count][skill_count]=int(task_eta[task_count])+int(extra_eta)
        skill_count+=1
    
    
    task_count+=1




# with open('best.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     writer.writerows(best)
    
# with open('r.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     writer.writerows(r)
    
# with open('etas.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     writer.writerows(etas)


i=0
aux=[[0 for x in range(2000)] for y in range(100)] 
for b in best :
    index, value = max(enumerate(b), key=operator.itemgetter(1))
    aux[index][i]=etas[i][index]
    i+=1
print("best:  ")
print(max([sum(a) for a in aux]))
print("total")
print(sum([sum(a) for a in aux])) 
null_count=0
for a in aux :
    if (sum(a)==0):
        null_count+=1
print("unused resources")
print(null_count)

i=0
aux=[[0 for x in range(2000)] for y in range(100)] 
for b in r :
    index, value = max(enumerate(b), key=operator.itemgetter(1))
    aux[index][i]=etas[i][index]
    i+=1
print("most suited:  ")
print(max([sum(a) for a in aux]))
print("total")
print(sum([sum(a) for a in aux])) 
null_count=0
for a in aux :
    if (sum(a)==0):
        null_count+=1
print("unused resources")
print(null_count)

i=0
aux=[[0 for x in range(2000)] for y in range(100)] 
for b in etas :
    index, value = min(enumerate(b), key=operator.itemgetter(1))
    aux[index][i]=etas[i][index]
    i+=1
print("fastest:  ")
print(max([sum(a) for a in aux]))
print("total")
print(sum([sum(a) for a in aux])) 
null_count=0
for a in aux :
    if (sum(a)==0):
        null_count+=1
print("unused resources")
print(null_count)
    
eta_sum=0
eta_num=0
eta_sum_free=0
best_free=[[0 for x in range(100)] for y in range(2000)] 
fast_free=[[0 for x in range(100)] for y in range(2000)] 

best_fast=[[0 for x in range(100)] for y in range(2000)] 
i=0
for p, e in zip(r,etas):
    if (eta_sum==0):
        chosen,value=max(enumerate([p[j]/e[j] for j in range(len(p))]), key=operator.itemgetter(1))
        chosen1,value1=max(enumerate([1/e[j] for j in range(len(p))]), key=operator.itemgetter(1))
    else :
        chosen, value=max(enumerate([p[j]/(e[j]*(sum(row[j] for row in best_fast) if sum(row[j] for row in best_fast)>0 else 1 )/(eta_sum/eta_num)) for j in range(len(p))]), key=operator.itemgetter(1))
        chosen1, value1=max(enumerate([1/(e[j]*(sum(row[j] for row in fast_free) if sum(row[j] for row in fast_free)>0 else 1 )/(eta_sum_free/eta_num)) for j in range(len(p))]), key=operator.itemgetter(1))
       
    best_fast[i][chosen]=etas[i][chosen]
    fast_free[i][chosen1]=etas[i][chosen1]
    eta_sum_free+=etas[i][chosen1]
    eta_sum+=etas[i][chosen]
    eta_num+=1 
    i+=1

i=0
aux=[[0 for x in range(2000)] for y in range(100)] 
for b in best_fast :
    index, value = max(enumerate(b), key=operator.itemgetter(1))
    aux[index][i]=etas[i][index]
    i+=1
print("most suited free:  ")
print(max([sum(a) for a in aux])) 
print("total")
print(sum([sum(a) for a in aux])) 
null_count=0
for a in aux :
    if (sum(a)==0):
        null_count+=1
print("unused resources")
print(null_count)


i=0
aux=[[0 for x in range(2000)] for y in range(100)] 
for b in fast_free :
    index, value = max(enumerate(b), key=operator.itemgetter(1))
    aux[index][i]=etas[i][index]
    i+=1
print("fastest free:  ")
print(max([sum(a) for a in aux])) 
print("total")
print(sum([sum(a) for a in aux])) 
null_count=0
for a in aux :
    if (sum(a)==0):
        null_count+=1
print("unused resources")
print(null_count)