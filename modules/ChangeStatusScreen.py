from kivy.uix.boxlayout import BoxLayout
from constants import *
from utility_functions import storeToken, readToken, removeToken
from api_functions import changeAccountStatus, BLOCKED, CLOSED
from Alert import Alert

class ChangeStatusScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(ChangeStatusScreen, self).__init__(**kwargs)
        self.app = app
        self.accountNumberTextInput = self.ids.accountNumberTextInput

    def closeAccountCallback(self):
        try:
            result = changeAccountStatus(readToken(), self.accountNumberTextInput.text.strip(), CLOSED)
            if result == None:
                raise Exception
            self.app.screenManager.current = MENU_SCREEN
            Alert(title="Success", text='Account Successfully Closed')
        except Exception:
            Alert(title="Input Error", text='Invalid Account Number! Try Again')

    def blockAccountCallback(self):
        try:
            result = changeAccountStatus(readToken(), self.accountNumberTextInput.text.strip(), BLOCKED)
            if result == None:
                raise Exception
            self.app.screenManager.current = MENU_SCREEN
            Alert(title="Success", text='Account Successfully Blocked')
        except Exception:
            Alert(title="Input Error", text='Invalid Account Number! Try Again')            

    def cancelCallback(self):
        self.app.screenManager.current = MENU_SCREEN