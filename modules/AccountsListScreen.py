from random import sample
from string import ascii_lowercase
from kivy.uix.boxlayout import BoxLayout
from api_functions import getAllAccounts, BLOCKED, OPEN, CLOSED
from utility_functions import readToken, removeToken
from Alert import Alert
from constants import *

class AccountsListScreen(BoxLayout):

    def __init__(self, app, **kwargs):
        super(AccountsListScreen, self).__init__(**kwargs)
        self.app = app
        self.ids.rv.data = []
        result = getAllAccounts(readToken())
        self.allResults = result[:]
        if result == None:
            removeToken()
            self.app.screenManager.current = LOGIN_SCREEN
            Alert(title="Authentication Error", text='Please Login Again')
        else:
            rvData = []
            for item in result:
                status = item['status']
                if status == BLOCKED:
                    status = 'blocked'
                elif status == CLOSED:
                    status = 'closed'
                elif status == OPEN:
                    status = 'open'
                rvData += [{
                    'accountNumber': item['accountNumber'],
                    'ownerName': item['accountOwner']['firstName']+' '+item['accountOwner']['lastName'],
                    'ownerID': item['accountOwner']['nationalCode'],
                    'credit': str(item['credit']),
                    'status': status
                }]
            self.ids.rv.data = rvData

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