from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
import requests, mysql.connector

Builder.load_file("login/login.kv")

class LoginWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def validate_user(self, username, password):
        body = {
            "username": username,
            "password": password,
        }
        req = requests.request(
            "POST",
            "http://127.0.0.1:5000/validateUser",
            json=body
        )

        response = req.json()
        if response['status'] is False:
            self.dialog = MDDialog(
                title='Error!',
                text=response['message'],
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            if response['data']['role'] == "Admin":
                self.parent.parent.transition.direction = "left"
                self.parent.parent.current = "scrn_admin"
                self.parent.parent.parent.ids.scrn_admin.children[0] \
                    .ids.nav_drawer_header.text = response['data']['username']
            else:
                self.parent.parent.transition.direction = "left"
                self.parent.parent.current = "scrn_user"
                self.parent.parent.parent.ids.scrn_user.children[0] \
                    .ids.nav_drawer_header.text = response['data']['username']
            self.ids.username_fld.text = ""
            self.ids.password_fld.text = ""
            toast(f"Welcome back {response['data']['username']}")

    # def validate_user(self, username, password):
    #     sql = 'SELECT users.user_name, users.user_pass, role.role_name ' \
    #           'FROM users ' \
    #           'INNER JOIN role ON users.role_id = role.id ' \
    #           'WHERE users.user_name=%s'
    #     values = [username, ]
    #     self.mycursor.execute(sql, values)
    #     target_user = self.mycursor.fetchall()
    #     if not target_user:
    #         self.ids.username_fld.error = True
    #     else:
    #         self.ids.username_fld.error = False
    #         if target_user[0][1] != password:
    #             self.ids.password_fld.error = True
    #         else:
    #             self.ids.password_fld.error = False
    #             if target_user[0][2] == "User":
    #                 self.parent.parent.transition.direction = "left"
    #                 self.parent.parent.current = "scrn_user"
    #                 self.parent.parent.parent.ids.scrn_user.children[0] \
    #                     .ids.nav_drawer_header.text = username
    #                 self.ids.username_fld.text = ""
    #                 self.ids.password_fld.text = ""
    #                 toast(f"Logged in as {username}!")
    #             else:
    #                 self.parent.parent.transition.direction = "left"
    #                 self.parent.parent.current = "scrn_admin"
    #                 self.parent.parent.parent.ids.scrn_admin.children[0] \
    #                     .ids.nav_drawer_header.text = username
    #                 self.ids.password_fld.text = ""
    #                 self.ids.username_fld.text = ""
    #                 toast(f"Logged in as {username}!")
    def goto_register(self):
        self.parent.parent.transition.direction = "left"
        self.parent.parent.current = "scrn_register"
        self.ids.username_fld.text = ""
        self.ids.password_fld.text = ""

    def close_dialog(self, *args):
        self.dialog.dismiss(force=True)
