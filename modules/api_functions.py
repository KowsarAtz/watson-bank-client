import requests

# BASE_URL = 'http://localhost:8000/api/'
BASE_URL = 'http://176.9.164.222:2211/api/'
BLOCKED = 'B'
OPEN = 'O'
CLOSED = 'C'

def signUp(token, username, password):
    url = BASE_URL + 'accounts/User/SignUp'
    data = {'username': username,'password': password}
    response = requests.post(url, json=data, headers={'Authorization': 'JWT ' + token})    
    return response.status_code #201: Success , 400: Duplicate Username , 401: Invalid Token Perhaps

def getToken(username, password):
    url = BASE_URL + 'Login'
    data = {'username': username,'password': password}
    response = requests.post(url, json=data).json()
    if 'token' in response:
        return response['token']
    return None

def createAccount(token, firstName, lastName, phoneNumber, nationalCode):
    url = BASE_URL + 'accounts/BankAccountListCreate'
    data = {'accountOwner': {'firstName': firstName, 'lastName': lastName,
                         'phoneNumber': phoneNumber, 'nationalCode': nationalCode}}
    response = requests.post(url, json=data, headers={'Authorization': 'JWT ' + token})
    # if response.status_code == 201: #201: Success , 400: Duplicate National ID , 401: Invalid Token Perhaps
    #     return response.json()
    # return None
    return response.status_code

def getAccountOwner(token, nationalCode):
    url = BASE_URL + 'accounts/AccountOwnerRetrieve/' + nationalCode
    response = requests.get(url, headers={'Authorization': 'JWT ' + token})
    if response.status_code == 200: #200: Success , 404: Not Found, 401: Invalid Token Perhaps
        return response.json()
    return None

def getAccount(token, accountNumber):
    url = BASE_URL + 'accounts/BankAccountRetrieve/' + accountNumber
    response = requests.get(url, headers={'Authorization': 'JWT ' + token})
    if response.status_code == 200: #200: Success , 404: Not Found, 401: Invalid Token Perhaps
        return response.json()
    return None

def getAllAccounts(token):
    url = BASE_URL + 'accounts/BankAccountListCreate'
    response = requests.get(url, headers={'Authorization': 'JWT ' + token})
    if response.status_code == 200: #200: Success , 401: Invalid Token Perhaps
        return response.json()
    return None

def getAccountLogs(token, accountNumber):
    url = BASE_URL + 'accounts/GetBankAccountLogs'
    data = {'accountNumber': accountNumber}
    response = requests.post(url, json=data, headers={'Authorization': 'JWT ' + token})
    if response.status_code == 200: #200: Success , 401: Invalid Token Perhaps
        return response.json()
    return None

def addAccount(token, nationalCode):
    url = BASE_URL + 'accounts/AddAccountToAccountOwner'
    data = {'nationalCode': nationalCode}
    response = requests.post(url, json=data, headers={'Authorization': 'JWT ' + token})
    if response.status_code == 200: #200: Success , 401: Invalid Token Perhaps
        return response.json()
    return None

def changeAccountStatus(token, accountNumber, newStatus):
    url = BASE_URL
    if newStatus == BLOCKED:
        url += 'accounts/BlockAccount'
    elif newStatus == CLOSED:
        url += 'accounts/CloseAccount'
    else:
        return False #Invalid Status
    data = {'accountNumber': accountNumber}
    response = requests.post(url, json=data, headers={'Authorization': 'JWT ' + token})
    if response.status_code == 200: #200: Success , 401: Invalid Token Perhaps, 404: Not Found
        return True
    return False
    # also it will return 200 if the account has been blocked/closed already!, to be completed . . . 

def getAllTransactions(token):
    url = BASE_URL + 'transaction/TransactionListCreate'
    response = requests.get(url, headers={'Authorization': 'JWT ' + token})
    if response.status_code == 200: #200: Success , 401: Invalid Token Perhaps
        return response.json()
    return None

def createTransaction(token, amount, fromAccount, toAccount, info = '', cash = False):
    url = BASE_URL + 'transaction/TransactionListCreate'
    data = {}

    data['amount'] = amount
    data['definition'] = info
    data['cash'] = cash
    if not toAccount == None:
        data['toAccount'] = toAccount
    if not fromAccount == None:
        data['fromAccount'] = fromAccount

    response = requests.post(url, json=data, headers={'Authorization': 'JWT ' + token})
    if response.status_code == 201: #201: Success , 400: sth not valid , 401: Invalid Token Perhaps
        return response.json()
    elif response.status_code == 400:
        msg = ''
        d = response.json()
        for key in d:
            for str_ in d[key]:
                msg += str_.upper() + ' ; '
        return msg[:-2]
    return None