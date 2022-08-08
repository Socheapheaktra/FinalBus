import requests

from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

import mysql.connector

Builder.load_file("register/register.kv")

class RegisterTextField(MDTextField):
    pass

class RegisterWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="bus_reservation"
        )
        self.mycursor = self.mydb.cursor()

        self.dialog = None

    def register(self, username, password, email):
        """ Insert User Information into Database """
        if username == "" or password == "" or email == "":
            self.dialog = MDDialog(
                title="Missing Requirement",
                text="Please input all field to continue",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            body = {
                "username": username,
                "password": password,
                "email": email
            }
            req = requests.request(
                "POST",
                "http://127.0.0.1:5000/registerUser",
                json=body
            )
            response = req.json()
            if response['status'] is False:
                self.dialog = MDDialog(
                    title="Somethings Wrong",
                    text=f"{response['message']}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
            else:
                self.ids.username_fld.text = ""
                self.ids.password_fld.text = ""
                self.ids.email_fld.text = ""
                self.dialog = MDDialog(
                    title="Success",
                    text=f"{response['message']}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

        # sql = 'SELECT user_name, email FROM users'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        # user_list = []
        # email_list = []
        # for x in result:
        #     user_list.append(x[0])
        #     email_list.append(x[1])
        # if username in user_list:
        #     self.ids.username_fld.error = True
        # elif password == "":
        #     self.ids.password_fld.error = True
        # elif email in email_list:
        #     self.ids.email_fld.error = True
        # else:
        #     self.ids.username_fld.error = False
        #     self.ids.password_fld.error = False
        #     self.ids.email_fld.error = False
        #     try:
        #         create_date = datetime.now().strftime("%Y-%m-%d")
        #         sql = 'INSERT INTO users (user_name, user_pass, email, created_date)' \
        #               'VALUEs (%s, %s, %s, %s)'
        #         values = [username, password, email, create_date, ]
        #         self.mycursor.execute(sql, values)
        #         self.mydb.commit()
        #     except:
        #         self.dialog = MDDialog(
        #             title="Error!",
        #             text="Please try again later!",
        #             buttons=[
        #                 MDFlatButton(
        #                     text="Close",
        #                     md_bg_color=(0, 0, 0, 0),
        #                     on_release=self.close_dialog()
        #                 )
        #             ]
        #         )
        #         self.dialog.open()
        #     else:
        #         self.ids.username_fld.text = ""
        #         self.ids.password_fld.text = ""
        #         self.ids.email_fld.text = ""
        #         self.dialog = MDDialog(
        #             title="Success!",
        #             text="Account created successfully!",
        #             buttons=[
        #                 MDFlatButton(
        #                     text="Close",
        #                     md_bg_color=(0, 0, 0, 0),
        #                     on_release=self.close_dialog
        #                 )
        #             ]
        #         )
        #         self.dialog.open()

    def goto_sign_in(self):
        """ Return to Sign In Page """
        self.parent.parent.transition.direction = "right"
        self.parent.parent.current = "scrn_login"
        self.ids.username_fld.text = ""
        self.ids.password_fld.text = ""
        self.ids.email_fld.text = ""
        self.ids.username_fld.error = False
        self.ids.password_fld.error = False
        self.ids.email_fld.error = False

    def close_dialog(self, *args):
        """ Close Active Dialog """
        self.dialog.dismiss(force=True)

