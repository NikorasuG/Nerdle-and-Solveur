#this file is used to generate all possible equations with a given set of characters and a given length
import itertools
from time import perf_counter

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
    with open('Solveur/listEqu/nerdle'+str(length)+'.txt', 'r') as f:
        for line in f:
            valEqs.append(line[:-1])
    return valEqs

def compareSolution(eq,sol):
    responseCode=[]
    dup = ''
    if len(eq)==len(sol):
        for i in range(len(eq)):
            if eq[i]==sol[i]:
                responseCode.append('correct')

            elif eq[i] in sol and eq[i] not in dup:
                responseCode.append('misplaced')
                dup+=eq[i]
            else:
                responseCode.append('incorrect')

        return {'message':responseCode}
    return {'message':'error not the same length'}


