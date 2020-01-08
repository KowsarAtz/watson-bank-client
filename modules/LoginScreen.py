from kivy.uix.boxlayout import BoxLayout
from constants import MENU_SCREEN
from utility_functions import storeToken 
from Alert import Alert

class LoginScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app = app
        self.usernameTextInput = self.ids.usernameTextInput
        self.passwordTextInput = self.ids.passwordTextInput

    def loginCallback(self):
        if len(self.usernameTextInput.text.strip()) == 0 or len(self.passwordTextInput.text.strip()) == 0:
            Alert(title="Input Error", text='Empty Fields are not Allowed Here! Try Again')
            return
        tokenStored = False
        try:
            tokenStored = storeToken(self.usernameTextInput.text.strip(), self.passwordTextInput.text.strip())
        except:
            Alert(title="Connection Error", text='Connection Error, Try Again Later')
            return
        if tokenStored:
            self.app.afterLoginCallback()
            self.app.screenManager.current = MENU_SCREEN
            return
        Alert(title="Auhthentication Error", text='Invalid Username or Password, Try Again')