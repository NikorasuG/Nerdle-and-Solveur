from flask import Flask, abort, request
from modules.equations import checkeqs,loadAllEqus,compute_pattern,getColors
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
allEqs = loadAllEqus()
cors = CORS(app)
equDuJour = choice(allEqs)
print(equDuJour)


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

def decodeToken(token):
    decoded = jwt.decode(token,secret,algorithms=['HS256'])
    decrypted = decoded['equation'].encode()
    decrypted = fernet.decrypt(decrypted).decode()
    return decrypted
