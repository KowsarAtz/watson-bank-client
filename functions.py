from os import remove as removeFile
from api_functions import getToken

TOKEN_FILE = './token'

def storeToken(username, password):
    token = getToken(username, password)
    if token == None:
        return False
    with open(TOKEN_FILE, 'w') as file:
        file.write(token)
    return True

def readToken():
    try:
        f = open(TOKEN_FILE, 'r')
        token = f.readline().strip()
        f.close() 
        return token
    except IOError:
        return None

def removeToken():
    try:
        removeFile(TOKEN_FILE)
        return True
    except Exception:
        return False