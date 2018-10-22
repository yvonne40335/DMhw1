import time
start_time = time.time()
L=[]
support={}

class Node(object):
    def __init__(self, data, par):
        self.data = data
        self.parent = par
        self.children = []
        self.link = None

    def add_child(self,data,par):
        self.children.append(Node(data,par))

        
def connect(now,node):
    while(now.link!=None):
        now = now.link
    now.link = node

    
def suffixpat(node,suffix):
    count = node.data[1]
    tmp=[]
    while node.parent.data[0] != -1:
        tmp.insert(0,[node.parent.data[0],count])
        node = node.parent
    suffix.append(tmp)

    
def FPtree(suffix):   
    #build FP-tree
    cheadertable = {}
    for tid in suffix:
        for citem in tid:
            if cheadertable.get(citem[0],0)!=0:
                cheadertable[citem[0]][0]=citem[1]+cheadertable.get(citem[0],0)[0]
            else:
                cheadertable[citem[0]]=[citem[1],None]
    
    for k, v in list(cheadertable.items()):
        if v[0] < minsup:
            del cheadertable[k]
    
    croot = Node([-1,-1],None)

    for tid in suffix:
        parent = croot
        for citem in tid:
            if cheadertable.get(citem[0]) != None:
                exist = 0
                for child in parent.children:
                    if child.data[0]==citem[0]:
                        child.data[1]=child.data[1]+citem[1]
                        parent = child
                        exist = 1
                        break
                if exist == 0:
                    parent.add_child(citem,parent)
                    node = parent.children[len(parent.children)-1]
                    if cheadertable[citem[0]][1]==None:
                        cheadertable[citem[0]][1] = node
                    else:
                        connect(cheadertable[citem[0]][1],node)
                    parent = node

    return croot, cheadertable
    
def minetree(headertable,prefix):    
    table = [v[0] for v in sorted(headertable.items(), key=lambda d: d[1][0])]

    for item in table:
        found = prefix[:]
        found.append(item)
        L.append(found)
        support[tuple(found)]=headertable[item][0]

        suffix=[]
        node = headertable[item][1]
        while node!=None:
            suffixpat(node,suffix)
            node = node.link

        tree, header = FPtree(suffix)

        if header!=None:
            minetree(header,found)
            
def rulesGenerator(frequentPatterns, minConf, rules,support):
    for frequentset in frequentPatterns:
        if(len(frequentset) > 1):
            getRules(frequentset,frequentset, rules, support, minConf)

def getRules(frequentset,currentset, rules, support, minConf):
    for frequentElem in currentset:
        subSet=[o for o in currentset if o not in set([frequentElem])]
        #subSet = set(currentset).difference([frequentElem]) #removeStr(currentset, frequentElem)
        confidence = support[tuple(frequentset)] / support[tuple(subSet)]
        if (confidence >= minConf):
            flag = False
            for rule in rules:
                if(rule[0] == subSet and rule[1] == set(frequentset).difference(subSet)):
                    flag = True
            if(flag == False):
                rules.append((subSet, set(frequentset).difference(subSet), confidence))
                #print( subSet, '-->', set(frequentset).difference(subSet), 'conf:', confidence)     ############print rules            
 
            if(len(subSet) >= 2):
                getRules(frequentset, subSet, rules, support, minConf)

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
minsup = 10
headertable = {}
L1 = []
C1 = {}
for tid in dataset:
    for item in tid:
        if item not in C1:
            C1[item] = 1
        else:
            C1[item] = C1[item]+1
#sort descending
sorted_d = sorted(C1.items(), key=lambda x: x[1], reverse=True)

for item, sup in sorted_d:
    if sup >= minsup:
        L1.append(item) ##delete?
        headertable[item]=[sup,None]


transaction = []
for itemset in dataset:
    tmp = []
    for item in L1:
        if item in itemset:
            tmp.append(item)
    transaction.append(tmp)


#build FP-tree
root = Node([-1,-1],None)

for tid in transaction:
    parent = root
    for item in tid:
        exist = 0
        for child in parent.children:
            if child.data[0]==item:
                child.data[1]=child.data[1]+1
                parent = child
                exist = 1
                break
        if exist == 0:
            parent.add_child([item,1],parent)
            node = parent.children[len(parent.children)-1]
            if headertable[item][1]==None:
                headertable[item][1] = node
            else:
                connect(headertable[item][1],node)
            parent = node          
  
largeitem = []
minetree(headertable,largeitem)            
print(L) ##########print frequent itemsets

rules=[]            
rulesGenerator(L,0.7,rules,support)
print('number of frequent itemsets =',len(L))
print(rules)
print('number of rules =',len(rules))
print("--- %s seconds ---" % (time.time() - start_time))
