from kivy.uix.boxlayout import BoxLayout
from constants import MENU_SCREEN
from utility_functions import storeToken 

class LoginScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app = app
        self.usernameTextInput = self.ids.usernameTextInput
        self.passwordTextInput = self.ids.passwordTextInput

    def loginCallback(self):
        tokenStored = False
        try:
            tokenStored = storeToken(self.usernameTextInput.text.strip(), self.passwordTextInput.text.strip())
        except:
            pass #to be completed . . .
        if tokenStored:
            self.app.screenManager.current = MENU_SCREEN
            return
        #to be completed . . .