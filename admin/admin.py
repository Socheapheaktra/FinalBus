from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextFieldRect
import mysql.connector

Builder.load_file("admin/admin.kv")

class AdminWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mydb = mysql.connector.connect(
            host='localhost',
            database='bus_reservation',
            user='root',
            passwd=''
        )
        self.mycursor = self.mydb.cursor()

        self.dialog = None

        self.show_user_table()

    def show_user_table(self):
        self.ids.user_table_content.clear_widgets()
        sql = 'SELECT user_id, user_name, user_pass, first_name, last_name, date_of_birth, ' \
              'email, phone, user_desc, status FROM users'
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        for x in result:
            for i in x:
                self.ids.user_table_content.add_widget(
                    MDLabel(
                        text=f"{i}",
                        size_hint_y=None,
                        height=50
                    )
                )

    def add_trip(self, location, price):
        pass

    def update_password(self, old_pass, new_pass, confirm_pass):
        pass

    def update_info(self, first_name, last_name, phone, email, dob):
        pass

    def goto_main_screen(self):
        self.ids.scrn_mngr.transition.direction = "right"
        self.ids.scrn_mngr.current = "main_scrn"
        self.ids.toolbar.right_action_items = []

    def goto_edit_profile(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_edit_profile"

    def goto_settings(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_settings"

    def close_dialog(self, *args):
        self.dialog.dismiss(force=True)

    def show_logout_dialog(self):
        self.dialog = MDDialog(
            title="Are you sure you want to logout?",
            buttons=[
                MDFlatButton(
                    text="Yes",
                    on_release=lambda x: self.logout()
                ),
                MDFlatButton(
                    text="No",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()

    def logout(self):
        self.parent.parent.current = "scrn_login"
        self.close_dialog()
