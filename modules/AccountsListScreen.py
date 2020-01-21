from random import sample
from string import ascii_lowercase
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from api_functions import getAllAccounts, getAccountLogs, BLOCKED, OPEN, CLOSED
from utility_functions import readToken, removeToken
from Alert import Alert
from math import ceil
from kivy.core.window import Window
from constants import *

class ShowLogsPopUp(BoxLayout):
    def __init__(self, logs, currentCredit, accountID, ownerName, **kwargs):
        super(ShowLogsPopUp, self).__init__(**kwargs)
        self.accountID = accountID
        self.ownerName = ownerName
        self.logs = logs
        self.bars = {
            'names': None, 
            'baseBar': None, 
            'greenBar': None, 
            'redBar': None,
            'y': None
        }
        self.createLogsChart(logs, currentCredit)

    def createLogsChart(self, logs, currentCredit):
        all_ = logs[:]
        greenBar = []
        redBar = []
        baseBar = []
        names = []
        sum_ = 0
        for log in all_:
            if log['logType'] == '+':
                t = float(log['amount'])
                greenBar += [t]
                redBar += [0]
                baseBar += [t]
                sum_ += t
            elif log['logType'] == '-':
                t = float(log['amount'])
                redBar += [t]
                greenBar += [0]
                baseBar += [-t]
                sum_ += (-t)
            names += [str(log['id']) + ' , ' + log['date'][11:16] + '\n' + log['date'][:10]]
        
        baseCredit = currentCredit - sum_
        for i in range(len(baseBar)):
            baseBar[i] += baseCredit
            baseCredit = baseBar[i]
        y = baseBar[:]
        for i in range(len(baseBar)):
            baseBar[i] -= greenBar[i]

        self.bars['names'] = names
        self.bars['baseBar'] = baseBar
        self.bars['greenBar'] = greenBar
        self.bars['redBar'] = redBar
        self.bars['y'] = y

class AccountsListScreen(BoxLayout):

    def __init__(self, app, **kwargs):
        super(AccountsListScreen, self).__init__(**kwargs)
        self.app = app
        self.ids.rv.data = []
        result = getAllAccounts(readToken())
        self.allResults = []
        if result == None:
            removeToken()
            self.app.screenManager.current = LOGIN_SCREEN
            Alert(title="Authentication Error", text='Please Login Again')
        else:
            self.allResults = result[:]

    def searchCallback(self, text):
        searchText = text.strip().lower()
        rvData = []
        for item in self.allResults:
            nationalCode = item['accountOwner']['nationalCode']
            accountNumber = item['accountNumber']
            ownerName = item['accountOwner']['firstName']+' '+item['accountOwner']['lastName']
            if not searchText in nationalCode and \
                not searchText in ownerName.lower() and \
                    not searchText in accountNumber:
                    continue
            status = item['status']
            if status == BLOCKED:
                status = 'blocked'
            elif status == CLOSED:
                status = 'closed'
            elif status == OPEN:
                status = 'open'
            rvData += [{
                'accountNumber': accountNumber,
                'ownerName': ownerName,
                'ownerID': nationalCode,
                'credit': str(item['credit']),
                'status': status
            }]
        self.ids.rv.data = rvData

    def backToMenuCallback(self):
        self.app.screenManager.current = MENU_SCREEN

    def showLogsCallback(self, accountID, ownerName):
        logs = getAccountLogs(readToken(), int(accountID))
        if logs == None:
            removeToken()
            self.app.screenManager.current = LOGIN_SCREEN
            Alert(title="Authentication Error", text='Please Login Again')
            return
        currentCredit = logs['currentCredit']
        logs = logs['logs']

        if len(logs) == 0:
            Alert(title="Account Logs", text='There are no logs to show!', time=3, linesNumber=1)
            return

        logsPopup = ShowLogsPopUp(logs, currentCredit, accountID, ownerName)
        popUpWindow = Popup(title="Logs", content=logsPopup, size_hint = (None, None), size=(400,400))
        popUpWindow.open()
        return

    def createTransactionCallback(self, accountID, transactionType):
        self.app.createTransactionScreenCallback()
        if transactionType == '+':
            self.app.transactionScreenChild.ids.toAccountTextInput.text = accountID
        elif transactionType == '-':
            self.app.transactionScreenChild.ids.fromAccountTextInput.text = accountID
        self.app.screenManager.current = CREATE_TRANSACTION_SCREEN