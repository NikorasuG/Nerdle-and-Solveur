from copy import deepcopy
from flask import Flask, abort, request
from numpy import arange
from modules.equations import checkeqs,loadAllEqus,compute_pattern,getColors
from modules.solveur import getListEqRestant,bestEq,loadEntropys
from flask_cors import CORS,cross_origin
from dotenv import load_dotenv
from os import getenv
from cryptography.fernet import Fernet
import jwt
from random import choice

app = Flask(__name__)
load_dotenv()
secret = getenv('SECRET')
key = Fernet.generate_key()
fernet = Fernet(key)
cors = CORS(app)


@app.route('/checkequ',methods=['POST'])
def checkequ():
    """this route is used to Check if the equation is valid and return the colors of the equation"""
    data = request.get_json()
    equ = decodeToken(data['token'])
    if data['equation'] == equ:
        return {'message':'success'}
    elif checkeqs(data['equation']):
        return getColors(compute_pattern(data['equation'],equ))
    else:
        return {'message':'invalid equation'}

@app.route('/getequ',methods=['GET'])
def getequ():
    """this route is used to get a random equation and return it as a token to secure it"""
    length = request.args.get('length')
    equDuJour = choice(loadAllEqus(length))
    print(equDuJour)
    equCrypted = fernet.encrypt(equDuJour.encode()) #encrypting the equation so the player can't see it
    payload = {'equation':equCrypted.decode()}
    
    token = jwt.encode(payload,secret,algorithm='HS256') #jwt token to secure the session
    return {"token":token}
@app.route('/gethelp',methods=['POST'])
def getHelp():
    """this route is used to get a hint for the equation"""
    data = request.get_json()
    eqs = data['equation']
    colors = data['colors']
    hint = getHints(eqs,colors)
    return {"hint":hint}
    
def decodeToken(token):
    """this function is used to decode the token and return the equation"""
    decoded = jwt.decode(token,secret,algorithms=['HS256'])
    decrypted = decoded['equation'].encode()
    decrypted = fernet.decrypt(decrypted).decode()
    return decrypted

def getHints(tries,colors):
    """this function loop through all the tries the player did before asking for a hint 
    and return the eq with the highest entropy from the remaining possible equations"""
    
    allEqs = deepcopy(loadAllEqus())
    idpossibleEqs = [i for i in range(len(allEqs))]
    entropys = deepcopy(loadEntropys())
    
    if len(tries) == 0: #exeption for the best start
        return bestEq(allEqs,entropys)
    else:
        for i in range(len(tries)): #looping through all the tries
            eq, pattern = tries[i], colors[i]
            idpossibleEqs,entropys = getListEqRestant(eq,pattern,allEqs,entropys,idpossibleEqs) #computing the remaining possible equations

        return bestEq(allEqs,entropys) #returning the best equation from the remaining possible equations
            