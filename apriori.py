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
dataset.append(itemset)
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

def rulesGenerator(frequentPatterns, minConf, rules,support):
    for i in range(1, len(frequentPatterns)):
        for frequentset in L[i]:
            if(len(frequentset) > 1):
                getRules(frequentset,frequentset, rules, support, minConf)

def getRules(frequentset,currentset, rules, support, minConf):
    for frequentElem in currentset:
        subSet=[o for o in currentset if o not in set([frequentElem])]
        confidence = support[tuple(frequentset)] / support[tuple(subSet)]
        if (confidence >= minConf):
            flag = False
            for rule in rules:
                if(rule[0] == subSet and rule[1] == set(frequentset).difference(subSet)):
                    flag = True
            if(flag == False):
                rules.append((subSet, set(frequentset).difference(subSet), confidence))
                #print( subSet, '-->', set(frequentset).difference(subSet), 'conf:', confidence) ########print rules                
 
            if(len(subSet) >= 2):
                getRules(frequentset, subSet, rules, support, minConf)

Lcount=0
#generate frequent-1 itemset
minsup = 10
L = []
support = {}
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
        tmp=[]
        L1.append(item)
        tmp.append(item)
        support[tuple(tmp)]=C1[item]

L1.sort()
L.append(L1)
Lcount = len(L1)

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
            support[item]=Ck.get(tuple(item))
    Lk.sort()
    L.append(Lk)
    Lcount = Lcount+len(Lk)
    Lkpre = Lk
    k = k+1
print(L) ########itemset 

rules=[]            
rulesGenerator(L,0.7,rules,support)
print('number of frequent itemsets =',Lcount)
print(rules)
print('number of rules =',len(rules))
print("--- %s seconds ---" % (time.time() - start_time))
