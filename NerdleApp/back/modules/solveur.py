import pickle
import threading
import numpy as np
import concurrent.futures
from itertools import product
from math import log2
from time import perf_counter
from progress.bar import IncrementalBar
import os

def createAllPatterns(length = '8'):
    allPatterns = []
    for i in product('012',repeat = int(length)):
        allPatterns.append(''.join(i))
    return allPatterns
def loadAllEqus(length = '8'):
    allEqs = []
    with open('NerdleApp/back/modules/listEqu/nerdle'+str(length)+'.txt', 'r') as f:
        for line in f:
            allEqs.append(line[:-1])
    return allEqs
def checkPattern(eq1,eq2,pattern):
    tested=[]
    for i in range(len(eq1)):
        if pattern[i] == '2':
            if eq1[i] != eq2[i]:
                return False
            else:
                tested.append(eq1[i])
            
    for i in range(len(eq1)):
        if pattern[i] == '1':
            if eq1[i] not in eq2 or eq1[i] == eq2[i] :
                return False
            else:
                tested.append(eq1[i])
    for i in range(len(eq1)):
        if pattern[i] == '0':
            if eq1[i] in eq2 and eq1[i] not in tested:
                return False
    return True

def findPattern(eq1,eq2):
    pattern=0
    for i in range(len(eq1)):
        if eq1[i] == eq2[i]:
            pattern+=2*3**i
        elif eq1[i] in eq2:
            pattern+=1*3**i
        else:
            pattern+=0*3**i
    return pattern

def StringToPattern(s):
    res = 0
    for k in range(len(s)):
        res += int(s[k])*3**k
    return res

def PatternToString(pattern, K):
    res = ""
    current = pattern
    for k in range(K):
        res += str(current%3)
        current = current//3
    return res

def PatternToMatrix(allEqs):
    length = len(allEqs)
    res = np.zeros((length,length),dtype = int)
    start=perf_counter()
    with IncrementalBar('Processing', max=len(allEqs)) as bar:
        for i in range(length):
            for j in range(length):
                res[i][j] = findPattern(allEqs[i],allEqs[j])
            bar.next()
    with open('matrix.npy', 'wb') as f:
        np.save(f, res)
    return res

def loadMatrix():
    
    with open('matrix.npy', 'rb') as f:
        res = np.load(f)
    return res

def entropy(row):
    counts = []
    tested = []
    for i in row:
        if i not in tested:
            counts.append(list(row).count(i))
            tested.append(i)
    entropy = 0
    for i in counts:
        p = i/len(row)
        entropy += p*log2(1/p)
    return entropy

def NbPossible(eqs,eq,pattern):
    counter = 0
    for i in eqs:
        if checkPattern(eq,i,pattern):
            counter += 1
    return counter
def NbPossibleAll(eqs,eq,patterns):
    counters = []
    for i in patterns:
        counters.append(NbPossible(eqs,eq,i))
    return counters

def listEntropy():
    scores = []
    allEqs = loadAllEqus()
    allPatterns = createAllPatterns()
    start = perf_counter()

    threads = []
    mat = loadMatrix()
    def worker(row):
        score = entropy(row)
        scores.append(score)


    with IncrementalBar('Processing', max=len(allEqs)) as bar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            futures = [executor.submit(worker, row) for row in mat]
            for future in concurrent.futures.as_completed(futures):
                bar.next()
    
    with open('entropy.txt', 'w') as f:
        for x in scores:
            f.write(str(x) + "\n")
    
    return scores[0]

def listEntropy2():
    entropys = dict()
    with open('entropy.txt', 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            entropys[i] = float(lines[i].strip("\n"))
    #save to pkl
    with open('entropy.pkl', 'wb') as f:
        pickle.dump(entropys, f, pickle.HIGHEST_PROTOCOL)
    return entropys

def bestStart():
    with open('entropy.pkl', 'rb') as f:
        entropys = pickle.load(f)
    return max(entropys, key=entropys.get)

def getListEqRestant(eq,pattern,listEq,entropys):
    newListEq = []
    for i in range(len(listEq)):
        if checkPattern(eq,listEq[i],pattern):
            newListEq.append(listEq[i])
        else:
            entropys.pop(i)
    print(len(newListEq))
    print(len(entropys))
    return listEq,entropys
def bestEq(listEq,eq,pattern,entropys):
    
    listEq,entropys=getListEqRestant(eq,pattern,listEq,entropys)
    idbest=max(entropys, key=entropys.get)
    return listEq[idbest]

with open('entropy.pkl', 'rb') as f:
    entropys = pickle.load(f)

print(bestEq(loadAllEqus(), '48-34=14', '00000100', entropys))