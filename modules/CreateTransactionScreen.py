from kivy.uix.boxlayout import BoxLayout
from constants import *
from utility_functions import storeToken, readToken, removeToken
from api_functions import createTransaction
from Alert import Alert

class CreateTransactionScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(CreateTransactionScreen, self).__init__(**kwargs)
        self.app = app
        self.fromAccountTextInput = self.ids.fromAccountTextInput
        self.toAccountTextInput = self.ids.toAccountTextInput
        self.transactionDescribtionTextInput = self.ids.transactionDescribtionTextInput
        self.transactionAmountTextInput = self.ids.transactionAmountTextInput

    def createTransactionCallback(self):
        fromAccount = self.fromAccountTextInput.text.strip()
        toAccount = self.toAccountTextInput.text.strip()
        if len(fromAccount) == 0 and len(toAccount) == 0:
            Alert(title="Input Error", text='Both Account Fields can not be Empty')
            return
        if fromAccount == '':
            fromAccount = None
        if toAccount == '':
            toAccount = None

        amount = self.transactionAmountTextInput.text.strip() 
        if len(amount) == 0:
            Alert(title="Input Error", text='Amount Field can not be Empty')
            return
        
        cash = False
        if fromAccount == None or toAccount == None:
            cash = True

        try:
            result = createTransaction(readToken(), float(amount), fromAccount, toAccount, self.transactionDescribtionTextInput.text.strip(), cash)
            if type(result) == str:
                Alert(title="Input Error(s)", text=result, time=3)
                return
            if result == None:
                removeToken()
                self.app.screenManager.current = LOGIN_SCREEN
                Alert(title="Authentication Error", text='Please Login Again')
                return

            self.app.screenManager.current = MENU_SCREEN
            Alert(title="Success", text='Transaction Successfully Created With ID: '+str(result['id']), time=3)
            
        except Exception:
            Alert(title="Connection Error", text='Connection Error, Try Again Later')
        
        
    def cancelTransactionCallback(self):
        self.app.screenManager.current = MENU_SCREEN