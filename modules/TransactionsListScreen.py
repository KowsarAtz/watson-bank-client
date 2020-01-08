from random import sample
from string import ascii_lowercase
from kivy.uix.boxlayout import BoxLayout
from api_functions import getAllTransactions
from utility_functions import readToken, removeToken
from Alert import Alert
from constants import *

class TransactionsListScreen(BoxLayout):

    def __init__(self, app, **kwargs):
        super(TransactionsListScreen, self).__init__(**kwargs)
        self.app = app
        self.ids.rv.data = []
        result = getAllTransactions(readToken())
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
        index = 0
        for item in self.allResults:  
            if not item['fromAccountNumber'] == None and not searchText in item['fromAccountNumber'] and \
                not item['toAccountNumber'] == None and not searchText in item['toAccountNumber'] and \
                    not searchText in str(item['id']):
                    continue
            fromAccountNumber = '-'
            if not item['fromAccountNumber'] == None:
                 fromAccountNumber = item['fromAccountNumber']
            toAccountNumber = '-'
            if not item['toAccountNumber'] == None:
                 toAccountNumber = item['toAccountNumber']
            type_ = 'Credit'
            if item['cash'] == True:
                type_ = 'Cash'
            rvData += [{
                'index': str(index),
                'transactionID': str(item['id']),
                'fromAccountNumber': fromAccountNumber,
                'toAccountNumber': toAccountNumber,
                'amount': str(item['amount']),
                'type': type_,
                'describtion': item['definition']
            }]
            index += 1
        self.ids.rv.data = rvData

    def showDescribtionCallback(self, text):
        text = text.strip()
        if len(text) == 0:
            text = '-- No Describtion --'
        Alert(title="Transaction Describtion", text=text, time=3, linesNumber=1)

    def backToMenuCallback(self):
        self.app.screenManager.current = MENU_SCREEN