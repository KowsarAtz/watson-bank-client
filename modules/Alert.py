from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup    
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock


class Alert(Popup):
    def __init__(self, title, text, time = None, linesNumber = None):
        super(Alert, self).__init__()
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')
        content.add_widget(
            Label(text=text, halign='left', valign='top')
        )

        if linesNumber == None:
            linesNumber = 1

        popup = Popup(
            title=title,
            content=content,
            size_hint=(max(len(title), len(text))*0.012, 0.2 * linesNumber),
            auto_dismiss=True,
        )
        popup.open()
        if time == None:
            Clock.schedule_once(popup.dismiss, 1.7)
        else:
            Clock.schedule_once(popup.dismiss, time)