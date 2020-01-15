from random import sample
from string import ascii_lowercase
from kivy.uix.boxlayout import BoxLayout
from api_functions import getAllAccounts, getAccountLogs, BLOCKED, OPEN, CLOSED
from utility_functions import readToken, removeToken
from LogsScreen import PageButton
from Alert import Alert
from math import ceil
from constants import *

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

        self.app.loadLogScreenCallback()
        self.app.logsScreenChild.logs = logs
        self.app.logsScreenChild.createLogsChart(logs, currentCredit)

        totalPages = ceil(len(logs)/TRANSACTION_PER_PAGE)
        firstPageTransationCount = len(logs) - (totalPages - 1)*TRANSACTION_PER_PAGE

        pageButton = PageButton(self.app, 0, '%d-%d'%(1, firstPageTransationCount))
        self.app.logsScreenChild.pageButtons += [pageButton]
        self.app.logsScreenChild.ids.pageButtonsLayout.add_widget(pageButton)

        base = firstPageTransationCount + 1
        for i in range(1,totalPages):
            pageButton = PageButton(self.app, i, '%d-%d'%(base, base + (TRANSACTION_PER_PAGE - 1)))
            self.app.logsScreenChild.pageButtons += [pageButton]
            self.app.logsScreenChild.ids.pageButtonsLayout.add_widget(pageButton)
            base += TRANSACTION_PER_PAGE
        
        self.app.logsScreenChild.pageButtons[totalPages-1].pageClickCallback(totalPages-1)
        self.app.logsScreenChild.ids.ChartLabel.text = 'Account ID: ' + accountID +'\nOwner Name: ' + ownerName

        self.app.screenManager.current = LOGS_SCREEN

    def createTransactionCallback(self, accountID, transactionType):
        self.app.createTransactionScreenCallback()
        if transactionType == '+':
            self.app.transactionScreenChild.ids.toAccountTextInput.text = accountID
        elif transactionType == '-':
            self.app.transactionScreenChild.ids.fromAccountTextInput.text = accountID
        self.app.screenManager.current = CREATE_TRANSACTION_SCREEN