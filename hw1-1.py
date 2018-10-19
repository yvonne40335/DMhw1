#!/usr/bin/env python
# coding: utf-8

# In[2]:


import itertools
import time
start_time = time.time()

def findsubsets(S,m):
    return set(itertools.combinations(S,m))

#read data file
with open("data.ntrans_1.nitems_0.1.txt") as f:
    content = f.readlines()
content = [x.strip() for x in content]
    
dataset = []
itemset = []
tmp = '1'
count = 0
for i in range(len(content)):
    content[i] = content[i].split()

    if content[i][0] == tmp:
        itemset.append(content[i][2])
    else:
        dataset.append(itemset)
        itemset = []
        itemset.append(content[i][2])
        tmp = str(content[i][0])

#generate candidate itemset
def apriori_gen(L, k):
    Lk = []
    for p in range(len(L)):
        for q in range(p+1,len(L)):
            if k==2:
                tmp = []
                tmp.append(L[p])
                tmp.append(L[q])
                Lk.append(tmp)
            else:
                if L[p][:k-2] == L[q][:k-2]:
                    tmp = []
                    for i in range(0,k-2):
                        tmp.append(L[p][i])
                    tmp.append(L[p][k-2])
                    tmp.append(L[q][k-2])
                    Lk.append(tmp)

    if k>2:
        tmpLk = []
        for item in Lk:
            remove = 0
            subsets = findsubsets(item,k-1)
            for sets in subsets:
                if sets not in L:
                    remove = 1
                    break
            if remove == 0:
                tmpLk.append(item)
        Lk = tmpLk
    return Lk       

#generate frequent-1 itemset
minsup = 10
L1 = []
C1 = {}
for tid in dataset:
    for item in tid:
        if item not in C1:
            C1[item] = 1
        else:
            C1[item] = C1[item]+1

for item, sup in list(C1.items()):
    if sup >= minsup:
        L1.append(item)
L1.sort()
print(L1)

#generate frequent-k itemset
Lkpre = L1
k = 2
while(len(Lkpre)>0):
    Lk = apriori_gen(Lkpre,k)
    #scan and count itemset support
    Ck = {}
    for tid in dataset:
        for item in Lk:
            if set(item).issubset(tid):
                Ck[tuple(item)]=Ck.get(tuple(item),0)+1

    #compare to minsup and output Ck
    Lk.clear()
    for item in Ck:
        if Ck.get(tuple(item)) >= minsup:
            Lk.append(item)
    Lk.sort()
    print(Lk)
    Lkpre = Lk
    k = k+1
    

print("--- %s seconds ---" % (time.time() - start_time))


# In[47]:


import itertools
def findsubsets(S,m):
    return set(itertools.combinations(S,m))

def apriori_gen(L, k):
    Lk = []
    for p in range(len(L)):
        for q in range(p+1,len(L)):
            if k==2:
                tmp = []
                tmp.append(L[p])
                tmp.append(L[q])
                Lk.append(tmp)
            else:
                if L[p][:k-2] == L[q][:k-2]:
                    tmp = []
                    for i in range(0,k-2):
                        tmp.append(L[p][i])
                    tmp.append(L[p][k-2])
                    tmp.append(L[q][k-2])
                    Lk.append(tmp)

    if k>2:
        tmpLk = []
        for item in Lk:
            remove = 0
            subsets = findsubsets(item,k-1)
            for sets in subsets:
                if sets not in L:
                    remove = 1
                    break
            if remove == 0:
                tmpLk.append(item)
        Lk = tmpLk
    return Lk
            

dataset = [['milk', 'bread', 'beer'],['bread', 'coffee'],['bread', 'egg'],['milk', 'bread', 'coffee'],['milk', 'egg'],['bread', 'egg'],['milk', 'egg'],['milk', 'bread', 'egg', 'beer'],['milk', 'bread', 'egg']]
minsup = 2
L1 = []
C1 = {}
for tid in dataset:
    for item in tid:
        if item not in C1:
            C1[item] = 1
        else:
            C1[item] = C1[item]+1
print(C1)

for item, sup in list(C1.items()):
    if sup >= minsup:
        L1.append(item)
L1.sort()
print(L1)

Lkpre = L1
k = 2
while(len(Lkpre)>0):
    Lk = apriori_gen(Lkpre,k)
    print('Lk=')
    print(Lk)
    Ck = {}
    for tid in dataset:
        for item in Lk:
            if set(item).issubset(tid):
                Ck[tuple(item)]=Ck.get(tuple(item),0)+1
    print('Ck=')
    print(Ck)
    Lk.clear()
    for item in Ck:
        if Ck.get(tuple(item)) >= minsup:
            Lk.append(item)
    Lk.sort()
    print('Lk=')
    print(Lk)
    Lkpre = Lk
    k = k+1
    



    


# In[23]:


with open("pat.ntrans_1.nitems_0.1.pat.txt") as f:
    dataset = f.readlines()
dataset = [x.strip() for x in dataset]
for i in range(0,13):
    del dataset[0]
    
for i in range(len(dataset)):
    print(dataset[i].split())
    
print(dataset)


# In[ ]:


L2 = apriori_gen(L1,2)
print('L2=')
print(L2)
C2 = {}
for tid in dataset:
    for item in L2:
        if set(item).issubset(tid):
            C2[tuple(item)]=C2.get(tuple(item),0)+1
print('C2=')
print(C2)
L2.clear()
for item in C2:
    if C2.get(tuple(item)) >= minsup:
        L2.append(item)
L2.sort()
print('L2=')
print(L2)

L3 = apriori_gen(L2,3)
print('L3=')
print(L3)
C3 = {}
for tid in dataset:
    for item in L3:
        if set(item).issubset(tid):
            C3[tuple(item)]=C3.get(tuple(item),0)+1
print('C3=')
print(C3)
L3.clear()
for item in C3:
    if C3.get(tuple(item)) >= minsup:
        L3.append(item)
L3.sort()
print('L3=')
print(L3)


# In[8]:


#load csvfile
minsup = 1000
import csv
with open('mushrooms_poison.csv', newline='') as csvfile:
    rows = csv.DictReader(csvfile)
    
   # for row in rows:
      #  print(row['class'],row['cap-shape'],row['cap-surface'],row['cap-color'],row['bruises'],row['odor'],row['gill-attachment'],row['gill-spacing'],row['gill-size'],row['gill-color'],row['stalk-shape'],row['stalk-root'],row['stalk-surface-above-ring'],row['stalk-surface-below-ring'],row['veil-type'],row['veil-color'],row['ring-number'],row['ring-type'],row['spore-print-color'],row['population'],row['habitat'])
        
    #frquent 1-itemset
    C1 =[]
    count = 0
    for row in rows:
        item = 
        if not in C1:
            C1.append('')
    print(count)
        

