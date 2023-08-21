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
    """this function will generate all equations of length"""
    yield from itertools.product(characters, repeat=length) #product generates all permutations of the characters
    
def checkeqs(eq):
    """this function will check if the equation is valid for python"""
    if eq.count('=') != 1:
        return False
    eq = eq.replace('=', '==')
    try:    
        return eval(eq)
    except:
        return False

def restricteq(eq):
    """this function will take a valid equation and add it to the list of valid restricted equations if it corresponds to the restrictions
    the restrictions are made so the equations are writen in a more human way"""

    if (eq[-3]=='=' or eq[-2]=='=' or eq[-4]=='=') and eq[0]!='0' and eq[0] not in '+-*/0' and eq[-2] not in '+-*/0' and [e for e in invalid if e in eq] == []:
        valRestrict.append(eq)

def genfile():
    """this function will generate all the equations of length and write them in a txt file"""
    counter = 0
    for i in generateAllEqs(characters):
        eq = ''.join(i)
        if checkeqs(eq):
            restricteq(eq)
        counter += 1
        if counter%10000000 == 0: #print the progress and remaining time
            elapsed = perf_counter()-start
            print(counter/max*100,"Time spent/remaining:",elapsed,elapsed*(max-counter)/counter)
    print(perf_counter()-start)
    print(valRestrict)
    with open('NerdleApp/back/Solveur/listEqu/nerdle'+str(length)+'.txt', 'w') as f:
        for x in valRestrict:
            f.write(x+"\n")

def loadAllEqus(length = '8'):
    """this function is used to load all the equations of a given length from the txt file"""
    valEqs = []
    with open('modules/listEqu/nerdle'+str(length)+'.txt', 'r') as f:
        for line in f:
            valEqs.append(line[:-1])
    return valEqs

def compute_pattern(tentative, truth):
    """this function is used to compute the pattern between two equations comparing the tentative equation to the truth equation
    its done in two times first we check if the symbol is at the right place if its the case we code it green 
    then we check if the symbol is in the equation if its the case we code it yellow to avoid case where a symbol correspond to green and orange"""
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

def getColors(pattern):
    """this function is used to convert the pattern to a list of colors for the front end"""
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
