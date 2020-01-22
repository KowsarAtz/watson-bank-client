from kivy.uix.boxlayout import BoxLayout
from constants import *
from utility_functions import storeToken, readToken, removeToken
from api_functions import addAccount
from Alert import Alert

class AddAccountScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(AddAccountScreen, self).__init__(**kwargs)
        self.app = app
        self.nationalCodeTextInput = self.ids.nationalCodeTextInput

    def addAccountCallback(self):
        if len(self.nationalCodeTextInput.text.strip()) == 0:
            Alert(title="Input Error", text='Empty Field! Try Again')
            return
        try:
            result = addAccount(readToken(), self.nationalCodeTextInput.text.strip())
            if result == None:
                raise Exception
            self.app.screenManager.current = MENU_SCREEN
            Alert(title="Success", text='Account<%s> Successfully Created' % result['accountNumber'])
        except Exception:
            Alert(title="Input Error", text='Invalid National Code! Try Again')   

    def cancelCallback(self):
        self.app.screenManager.current = MENU_SCREEN