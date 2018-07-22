import os
import glob
import time
import sys
import math
import csv
import operator
import numpy

print("reading")

task_number=100;

task_skill = [(line.rstrip('\n')).split(',') for line in open('100tasks.csv')]
task_eta =[line.rstrip('\n') for line in open('task-eta100.csv')]
skill_level=[(line.rstrip('\n')).split(',') for line in open('100people.csv')]


best=[[0 for x in range(100)] for y in range(task_number)] 
r=[[0 for x in range(100)] for y in range(task_number)] 

etas=[[0 for x in range(100)] for y in range(task_number)] 

print("started first skills")

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

print("started simple allocations")

eta_num=0
eta_sum_free=0
fast_free=[[0 for x in range(100)] for y in range(task_number)] 

best_fast=[[0 for x in range(100)] for y in range(task_number)] 
i=0
for p, e in zip(r,etas):
    if (eta_sum_free==0):
        chosen1,value1=max(enumerate([1/e[j] for j in range(len(p))]), key=operator.itemgetter(1))
    else :
        chosen1, value1=max(enumerate([1/(e[j]*(sum(row[j] for row in fast_free) if sum(row[j] for row in fast_free)>0 else 1 )/(eta_sum_free/eta_num)) for j in range(len(p))]), key=operator.itemgetter(1))
    fast_free[i][chosen1]=etas[i][chosen1]
    eta_sum_free+=etas[i][chosen1]
    eta_num+=1 
    i+=1


i=0
aux=[[0 for x in range(task_number)] for y in range(100)] 
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

print("started skill adapted allocations")
eta_num=0
eta_sum_free=0
fast_free=[[0 for x in range(100)] for y in range(task_number)] 

best_fast=[[0 for x in range(100)] for y in range(task_number)] 
i=0
for p, e in zip(r,etas):
    if (eta_sum_free==0):
        chosen1,value1=max(enumerate([1/e[j] for j in range(len(p))]), key=operator.itemgetter(1))
    else :
        chosen1, value1=max(enumerate([1/(e[j]*(sum(row[j] for row in fast_free) if sum(row[j] for row in fast_free)>0 else 1 )/(eta_sum_free/eta_num)) for j in range(len(p))]), key=operator.itemgetter(1))
       

    fast_free[i][chosen1]=etas[i][chosen1]
    eta_sum_free+=etas[i][chosen1]
    
  
    
    #start skill adjustment
    for skill_index, current_skill in enumerate(skill_level[chosen1]):
        skill_level[chosen1][skill_index]=max(
            skill_level[chosen1][skill_index],
            task_skill[i][skill_index])
    task_count=0
    for ts in task_skill :
        #sqsum_ts=sum( [int(ts[i])*int(ts[i]) for i in range(len(ts))] )
        sl=skill_level[chosen1]
        extra_eta=0
        for t, s in zip(ts, sl) :
            if (int(t)>int(s)) :
                extra_eta += (int(t)-int(s))/int(s)
        etas[task_count][chosen1]=int(task_eta[task_count])+int(extra_eta)
        task_count+=1
    #finish skill adjustment
    eta_num+=1 
    i+=1


i=0
aux=[[0 for x in range(task_number)] for y in range(100)] 
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