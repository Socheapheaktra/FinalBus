from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from login.login import LoginWindow
from user.user import UserWindow
from admin.admin import AdminWindow
from register.register import RegisterWindow

Window.maximize()

class MainWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.scrn_mngr.current = "scrn_login"
        self.ids.scrn_login.add_widget(LoginWindow())
        self.ids.scrn_user.add_widget(UserWindow())
        self.ids.scrn_admin.add_widget(AdminWindow())
        self.ids.scrn_register.add_widget(RegisterWindow())

class MainApp(MDApp):
    def build(self):
        self.title = "Online Bus Ticket Booking"
        return MainWindow()

if __name__ == '__main__':
    MainApp().run()