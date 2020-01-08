from kivy.uix.boxlayout import BoxLayout
from constants import *
from utility_functions import storeToken, readToken, removeToken
from api_functions import signUp
from Alert import Alert

class SignUpScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        self.app = app
        self.usernameTextInput = self.ids.chosenUsernameTextInput
        self.passwordTextInput = self.ids.chosenPasswordTextInput

    def signUpCallback(self):
        if len(self.usernameTextInput.text.strip()) == 0 or len(self.passwordTextInput.text.strip()) == 0:
            Alert(title="Input Error", text='Empty Fields are not Allowed Here! Try Again')
            return
        try:
            resultCode = signUp(readToken(), 
                            self.usernameTextInput.text.strip(), 
                            self.passwordTextInput.text.strip())
            if resultCode == INVALID_TOKEN_CODE:
                removeToken()
                self.app.screenManager.current = LOGIN_SCREEN
                Alert(title="Authentication Error", text='Please Login Again')
            elif resultCode == INVALID_CODE:
                Alert(title="Input Error", text='User with this Username Already Exists!')
            elif resultCode == POST_SUCCESS_CODE:
                self.app.screenManager.current = MENU_SCREEN
                Alert(title="Success", text='New Clerk Successfully Registered')
            else:
                self.app.screenManager.current = MENU_SCREEN
                Alert(title="Register Error", text='Please Try Again Later')
        except Exception:
            Alert(title="Connection Error", text='Connection Error, Try Again Later')
            

    def cancelSignUpCallback(self):
        self.app.screenManager.current = MENU_SCREEN