from kivy.uix.boxlayout import BoxLayout
from utility_functions import removeToken
from constants import *

class MenuScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.app = app

    def logoutCallback(self):
        removeToken()
        self.app.screenManager.current = LOGIN_SCREEN
        
    def signUpClerkCallback(self):
        self.app.screenManager.current = SIGNUP_SCREEN

    def getAllAccountsCallback(self):
        self.app.screenManager.current = ALL_ACCOUNTS_SCREEN