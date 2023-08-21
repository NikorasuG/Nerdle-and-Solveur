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
    length = request.args.get('length')
    equDuJour = choice(loadAllEqus(length))
    print(equDuJour)
    equCrypted = fernet.encrypt(equDuJour.encode())
    payload = {'equation':equCrypted.decode()}
    
    decrypted = payload['equation'].encode()
    decrypted = fernet.decrypt(decrypted).decode()
    
    token = jwt.encode(payload,secret,algorithm='HS256')
    return {"token":token}
@app.route('/gethelp',methods=['POST'])
def getHelp():
    data = request.get_json()
    eqs = data['equation']
    colors = data['colors']
    hint = getHints(eqs,colors)
    return {"hint":hint}
    
def decodeToken(token):
    decoded = jwt.decode(token,secret,algorithms=['HS256'])
    decrypted = decoded['equation'].encode()
    decrypted = fernet.decrypt(decrypted).decode()
    return decrypted

def getHints(tries,colors):
    allEqs = deepcopy(loadAllEqus())
    idpossibleEqs = [i for i in range(len(allEqs))]
    entropys = deepcopy(loadEntropys())
    if len(tries) == 0:
        return bestEq(allEqs,entropys)
    else:
        for i in range(len(tries)):
            eq, pattern = tries[i], colors[i]
            idpossibleEqs,entropys = getListEqRestant(eq,pattern,allEqs,entropys,idpossibleEqs)

        return bestEq(allEqs,entropys)
            