from kivy.uix.boxlayout import BoxLayout
from constants import *
from utility_functions import storeToken, readToken, removeToken
from api_functions import createAccount
from Alert import Alert

class CreateAccountScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(CreateAccountScreen, self).__init__(**kwargs)
        self.app = app
        self.firstNameTextInput = self.ids.firstNameTextInput
        self.lastNameTextInput = self.ids.lastNameTextInput
        self.phoneNumberTextInput = self.ids.phoneNumberTextInput
        self.nationalCodeTextInput = self.ids.nationalCodeTextInput

    def createAccountCallback(self):
        if len(self.firstNameTextInput.text.strip()) == 0 \
            or len(self.lastNameTextInput.text.strip()) == 0\
                or len(self.phoneNumberTextInput.text.strip()) == 0\
                    or len(self.nationalCodeTextInput.text.strip()) == 0:
            Alert(title="Input Error", text='Empty Fields are not Allowed Here! Try Again')
            return
        try:
            resultCode = createAccount(readToken(), \
                self.firstNameTextInput.text.strip(), \
                    self.lastNameTextInput.text.strip(), \
                        self.phoneNumberTextInput.text.strip(), \
                            self.nationalCodeTextInput.text.strip())
            if resultCode == INVALID_TOKEN_CODE:
                removeToken()
                self.app.screenManager.current = LOGIN_SCREEN
                Alert(title="Authentication Error", text='Please Login Again')
            elif resultCode == DUPLICATE_CODE:
                Alert(title="Input Error", text='Owner with this ID Already Exists!')
            elif resultCode == POST_SUCCESS_CODE:
                self.app.screenManager.current = MENU_SCREEN
                Alert(title="Success", text='New Account Successfully Created')
            else:
                self.app.screenManager.current = MENU_SCREEN
                Alert(title="Create Account Error", text='Please Try Again Later')
        except Exception:
            Alert(title="Connection Error", text='Connection Error, Try Again Later')
            

    def cancelCreateAccountCallback(self):
        self.app.screenManager.current = MENU_SCREEN