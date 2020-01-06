from kivy.lang import Builder
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from utility_functions import readToken
from constants import *
from LoginScreen import LoginScreen
from MenuScreen import MenuScreen
# Window.clearcolor = utils.get_color_from_hex("#0c1632")
Config.set('graphics', 'resizable', FALSE)
# Config.set('graphics', 'width', '300')
# Config.set('graphics', 'height', '300')
root = Builder.load_file(LOGIN_SCREEN_KV)
root = Builder.load_file(MENU_SCREEN_KV)


class MyApp(App):
    def build(self):
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

        return self.screenManager

if __name__ == '__main__':
    MyApp().run()