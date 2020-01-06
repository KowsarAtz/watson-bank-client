from kivy.uix.boxlayout import BoxLayout
from utility_functions import removeToken
from constants import LOGIN_SCREEN

class MenuScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.app = app

    def logoutCallback(self):
        tokenRemoved=removeToken()
        if tokenRemoved:
            self.app.screenManager.current = LOGIN_SCREEN
        else:
            pass  # to be completed . . . (not sure what exactly!)