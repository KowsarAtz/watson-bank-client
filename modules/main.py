from constants import *

from kivy.config import Config
# Config.set('graphics', 'fullscreen', 'auto')

from kivy.lang import Builder
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from utility_functions import readToken
from LoginScreen import LoginScreen
from MenuScreen import MenuScreen
from SignUpScreen import SignUpScreen
from AccountsListScreen import AccountsListScreen
from TransactionsListScreen import TransactionsListScreen
from CreateTransactionScreen import CreateTransactionScreen
from CreateAccountScreen import CreateAccountScreen
from ChangeStatusScreen import ChangeStatusScreen
from AddAccountScreen import AddAccountScreen

LabelBase.register('MyRegularFont', './assets/fonts/Rubik-Regular.ttf')
LabelBase.register('MyBoldFont', './assets/fonts/Rubik-Bold.ttf')
LabelBase.register('MyItalicFont', './assets/fonts/Rubik-Italic.ttf')


root = Builder.load_file(MY_WIDGETS_KV)
root = Builder.load_file(LOGIN_SCREEN_KV)
root = Builder.load_file(MENU_SCREEN_KV)
root = Builder.load_file(SIGNUP_SCREEN_KV)
root = Builder.load_file(ALL_ACCOUNTS_SCREEN_KV)
root = Builder.load_file(ALL_TRANSACTIONS_SCREEN_KV)
root = Builder.load_file(CREATE_TRANSACTION_SCREEN_KV)
root = Builder.load_file(CREATE_ACCOUNT_SCREEN_KV)
root = Builder.load_file(ADD_ACCOUNT_SCREEN_KV)
root = Builder.load_file(SHOW_LOGS_POPUP_KV)
root = Builder.load_file(CHANGE_ACCOUNT_STATUS_KV)

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
        else:
            self.screenManager.add_widget(screenLogin)
            self.screenManager.add_widget(screenMenu)

        self.signupScreen = SignUpScreen(self)
        screen = Screen(name=SIGNUP_SCREEN)
        screen.add_widget(self.signupScreen)
        self.screenManager.add_widget(screen)

        self.createAccountScreen = CreateAccountScreen(self)
        screen = Screen(name=CREATE_ACCOUNT_SCREEN)
        screen.add_widget(self.createAccountScreen)
        self.screenManager.add_widget(screen)

        self.addAccountScreen = AddAccountScreen(self)
        screen = Screen(name=ADD_ACCOUNT_SCREEN)
        screen.add_widget(self.addAccountScreen)
        self.screenManager.add_widget(screen)

        self.changeAccountStatus = ChangeStatusScreen(self)
        screen = Screen(name=CHANGE_ACCOUNT_STATUS)
        screen.add_widget(self.changeAccountStatus)
        self.screenManager.add_widget(screen)

        self.allTransactionsScreen = None
        self.allTransactionsScreenChild = None

        self.allAccountsScreen = None
        self.allAccountsScreenChild = None

        self.transactionScreen = None
        self.transactionScreenChild = None

        return self.screenManager    

    def allAccountsScreenCallback(self):
        if not self.allAccountsScreen == None:
            self.screenManager.remove_widget(self.allAccountsScreen)
        self.allAccountsScreenChild = AccountsListScreen(self)
        self.allAccountsScreen = Screen(name=ALL_ACCOUNTS_SCREEN)
        self.allAccountsScreen.add_widget(self.allAccountsScreenChild)
        self.screenManager.add_widget(self.allAccountsScreen)

    def allTransactionsScreenCallback(self):
        if not self.allTransactionsScreen == None:
            self.screenManager.remove_widget(self.allTransactionsScreen)
        self.allTransactionsScreenChild = TransactionsListScreen(self)
        self.allTransactionsScreen = Screen(name=ALL_TRANSACTIONS_SCREEN)
        self.allTransactionsScreen.add_widget(self.allTransactionsScreenChild)
        self.screenManager.add_widget(self.allTransactionsScreen)

    def createTransactionScreenCallback(self):
        if not self.transactionScreen == None:
            self.screenManager.remove_widget(self.transactionScreen)
        self.transactionScreenChild = CreateTransactionScreen(self)
        self.transactionScreen = Screen(name=CREATE_TRANSACTION_SCREEN)
        self.transactionScreen.add_widget(self.transactionScreenChild)
        self.screenManager.add_widget(self.transactionScreen)

if __name__ == '__main__':
    MyApp().run()