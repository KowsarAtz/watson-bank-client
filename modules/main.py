from constants import *

from kivy.config import Config
Config.set('graphics', 'resizable', FALSE)
# Config.set('graphics', 'width', '900')
# Config.set('graphics', 'height', '900')

from kivy.core.window import Window
# Window.size = (1200, 600)
Window.size = (1366,710)

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from utility_functions import readToken
from LoginScreen import LoginScreen
from MenuScreen import MenuScreen
from SignUpScreen import SignUpScreen
from AccountsListScreen import AccountsListScreen
from TransactionsListScreen import TransactionsListScreen
from LogsScreen import LogsScreen

root = Builder.load_file(LOGIN_SCREEN_KV)
root = Builder.load_file(MENU_SCREEN_KV)
root = Builder.load_file(SIGNUP_SCREEN_KV)
root = Builder.load_file(ALL_ACCOUNTS_SCREEN_KV)
root = Builder.load_file(ALL_TRANSACTIONS_SCREEN_KV)
root = Builder.load_file(LOGS_SCREEN_KV)


class MyApp(App):
    def build(self):
        self.title = 'Watson Bank Client'
        self.screenManager = ScreenManager()

        self.loginScreen = LoginScreen(self)
        screenLogin = Screen(name=LOGIN_SCREEN)
        screenLogin.add_widget(self.loginScreen)

        self.menuScreen = MenuScreen(self)
        screenMenu = Screen(name=MENU_SCREEN)
        screenMenu.add_widget(self.menuScreen)

        if not readToken() == None:
            self.screenManager.add_widget(screenMenu)
            self.screenManager.add_widget(screenLogin)
            self.afterLoginCallback()
        else:
            self.screenManager.add_widget(screenLogin)
            self.screenManager.add_widget(screenMenu)

        self.signupScreen = SignUpScreen(self)
        screen = Screen(name=SIGNUP_SCREEN)
        screen.add_widget(self.signupScreen)
        self.screenManager.add_widget(screen)

        return self.screenManager
    
    def afterLoginCallback(self):
        self.allAccountsScreen = AccountsListScreen(self)
        screen = Screen(name=ALL_ACCOUNTS_SCREEN)
        screen.add_widget(self.allAccountsScreen)
        self.screenManager.add_widget(screen)

        self.allTransactionsScreen = TransactionsListScreen(self)
        screen = Screen(name=ALL_TRANSACTIONS_SCREEN)
        screen.add_widget(self.allTransactionsScreen)
        self.screenManager.add_widget(screen)

        self.logsScreen = None
        self.logsScreenChild = None

    def loadLogScreenCallback(self):
        if not self.logsScreen == None:
            self.screenManager.remove_widget(self.logsScreen)
        self.logsScreenChild = LogsScreen(self)
        self.logsScreen = Screen(name=LOGS_SCREEN)
        self.logsScreen.add_widget(self.logsScreenChild)
        self.screenManager.add_widget(self.logsScreen)

if __name__ == '__main__':
    MyApp().run()