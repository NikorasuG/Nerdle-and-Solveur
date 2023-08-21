#this file is used to generate all possible equations with a given set of characters and a given length
import itertools
from time import perf_counter
import os

characters = '0123456789+-*/='
length = 7
allEqs = []
valEqs = []
valRestrict = []
invalid = ['++','--','**','//','+-','+*','+/','-+','-*','-/','*+', '*-', '*-', '*-', '/+', '/-', '/-','+0','-0','*0','/0','=+', '=-', '=*', '=/', '==']
           
counter = 0
max = len(characters)**length
start = perf_counter()
def generateAllEqs(characters):
    #this function will generate all equations of length
    yield from itertools.product(characters, repeat=length)
    
def checkeqs(eq):
    #this function will check if the equation is valid
    if eq.count('=') != 1:
        return False
    eq = eq.replace('=', '==')
    try:    
        return eval(eq)
    except:
        return False

def restricteq(eq):
    #this function will take a valid equation and add it to the list of valid restricted equations if it corresponds to the restrictions
    #only numbers after equal sign
    if (eq[-3]=='=' or eq[-2]=='=' or eq[-4]=='=') and eq[0]!='0' and eq[0] not in '+-*/0' and eq[-2] not in '+-*/0' and [e for e in invalid if e in eq] == []:
        valRestrict.append(eq)

def genfile():
    counter = 0
    for i in generateAllEqs(characters):
        eq = ''.join(i)
        if checkeqs(eq):
            restricteq(eq)
        counter += 1
        if counter%10000000 == 0:
            elapsed = perf_counter()-start
            print(counter/max*100,"Time spent/remaining:",elapsed,elapsed*(max-counter)/counter)
    print(perf_counter()-start)
    print(valRestrict)
    with open('NerdleApp/back/Solveur/listEqu/nerdle'+str(length)+'.txt', 'w') as f:
        for x in valRestrict:
            f.write(x+"\n")

def loadAllEqus(length = '8'):
    print(os.getcwd())
    valEqs = []
    with open('modules/listEqu/nerdle'+str(length)+'.txt', 'r') as f:
        for line in f:
            valEqs.append(line[:-1])
    return valEqs

def compute_pattern(tentative, truth):
    result = [0 for i in range(len(tentative))]
    truth_list = list(truth)

    for k in range(len(tentative)):
        if tentative[k] == truth[k]:
            result[k] = 2  # Green coded by 2
            truth_list[k] = '_'

    for k in range(len(tentative)):
        if result[k] != 0:
            continue
        
        fnd = False
        for k2 in range(len(tentative)):
            # If found elsewhere and that elsewhere is not already green
            if tentative[k] == truth_list[k2]:
                fnd = True
                truth_list[k2] = '_'
                break
        if fnd:
            result[k] = 1  # Yellow coded by 1
    return result
print(compute_pattern("48-34=14","440/5=88"))
def getColors(pattern):
    responseCode=[]
    dup = ''
    for i in pattern:
        if i==2:
            responseCode.append('correct')
        elif i==1:
            responseCode.append('misplaced')
        else:
            responseCode.append('incorrect')
    return {'message':responseCode}
