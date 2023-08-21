import pickle
import numpy as np
import concurrent.futures
from itertools import product
from math import log2
from time import perf_counter
from progress.bar import IncrementalBar
import os

def createAllPatterns(length = '8'):
    """this function is used to create all the possible patterns for a given length"""
    allPatterns = []
    for i in product('012',repeat = int(length)): #loop through all the possible combinations of 0,1,2
        allPatterns.append(''.join(i))
    return allPatterns

def loadAllEqus(length = '8'):
    """this function is used to load all the equations of a given length from the txt file"""
    allEqs = []
    with open('NerdleApp/back/modules/listEqu/nerdle'+str(length)+'.txt', 'r') as f:
        for line in f:
            allEqs.append(line[:-1])
    return allEqs

def checkPattern(eq1,eq2,pattern):
    """this function is used to check if the equation eq2 correspond to the pattern given the equation eq1"""
    tested=[]
    for i in range(len(eq1)): #we do the three test separately to avoid case where a symbol correspond to green and orange
        if pattern[i] == '2':
            if eq1[i] != eq2[i]:
                return False
            else:
                tested.append(eq1[i])
                
    for i in range(len(eq1)):

        if pattern[i] == '1':
            if eq1[i] not in eq2 or eq1[i] == eq2[i] : #most tricky test: if the symbol is at the right place its already green so its false
                return False
            else:
                tested.append(eq1[i])

    for i in range(len(eq1)):
        if pattern[i] == '0':
            if eq1[i] in eq2 and eq1[i] not in tested:
                return False

    return True

def findPattern(eq1,eq2):
    """this function is used to find the pattern between two equations it return a number that represent the pattern in base 3"""
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
    """this function is used to convert a string to a number in base 3"""
    res = 0
    for k in range(len(s)):
        res += int(s[k])*3**k
    return res

def PatternToString(pattern, K):
    """this function is used to convert a number in base 3 to a string"""
    res = ""
    current = pattern
    for k in range(K):
        res += str(current%3)
        current = current//3
    return res

def PatternToMatrix(allEqs):
    """this function is used to create the matrix of all the patterns between all the equations
    its a matrice n*n where n is the number of equations for i,j in [0,n] the value of the matrice[i][j] 
    is the pattern resulting of trying the equation i for the solution j
    !!! be carefull this function can take a lot of time to run  and the matrice can be huge!!!"""
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
    """this function is used to load the matrix from the file"""""
    with open('matrix.npy', 'rb') as f:
        res = np.load(f)
    return res

def entropy(row):
    """this function is used to compute the entropy of an equation of the matrix
    given a certain row i corresponding to the equation i all the patterns on this row correpond to another word
    by counting the number of time each pattern appear we can calculate the amount of information we can get from this equation"""
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

def listEntropy():
    """this function is used to compute the entropy of all the equations of the matrix
    !!! this function is pure no reflexion brute force it will take a really long time even with multithreading !!!"""
    scores = []
    allEqs = loadAllEqus()
    allPatterns = createAllPatterns()
    start = perf_counter()

    threads = []
    mat = loadMatrix()
    def worker(row): #worker function for multithreading calling entropy on each row
        score = entropy(row)
        scores.append(score)


    with IncrementalBar('Processing', max=len(allEqs)) as bar: #progress bar
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor: #multithreading to increase speed
            futures = [executor.submit(worker, row) for row in mat]
            for future in concurrent.futures.as_completed(futures):
                bar.next()
    
    with open('entropy.txt', 'w') as f: #save to txt
        for x in scores:
            f.write(str(x) + "\n")
    
    return scores[0]

def listEntropy2():
    """this function to create a dictionnary of all the entropys of the equations with the id of the equation as key"""
    entropys = dict()

    with open('modules/entropy.txt', 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            entropys[i] = float(lines[i].strip("\n"))
    #save to pkl
    with open('entropy.pkl', 'wb') as f:
        pickle.dump(entropys, f, pickle.HIGHEST_PROTOCOL)
    return entropys

def bestStart():
    """this function is used to find the best equation to start the game return the id of the equation giving the most information"""
    with open('entropy.pkl', 'rb') as f:
        entropys = pickle.load(f)
    return max(entropys, key=entropys.get)

def getListEqRestant(eq,pattern,listEq,entropys,idpossibleEqs):
    """this function is used to get the list of the remaining possible equations given the equation and the pattern 
    it test if a eq could be solution by checking if the eq could result of this pattern for this equation
    if the eq can't be solution we remove it from the list of possible equations and remove its entropy from the dictionnary"""
    newListEq = []
    
    for i in idpossibleEqs:
        if checkPattern(eq,listEq[i],pattern):
            newListEq.append(i)
        else:
            entropys.pop(i)
    return newListEq,entropys

def bestEq(listEq,entropys):
    """this function is used to find the best equation given en list of entropys and a list of equations"""
    idbest=max(entropys, key=entropys.get)
    return listEq[idbest]

def loadEntropys():
    """this function is used to load the dictionnary of entropys from the file"""
    with open('modules/entropys.pkl', 'rb') as f:
        entropys = pickle.load(f)
    return entropys