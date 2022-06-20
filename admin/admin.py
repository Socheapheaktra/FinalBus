from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField

from kivy.properties import StringProperty

import datetime
import mysql.connector

Builder.load_file("admin/admin.kv")

class BusStatusField(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = StringProperty()

class BusTypeField(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = StringProperty()

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
        self.dob_date = None

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

    def show_trip_table(self):
        self.ids.trip_table_content.clear_widgets()
        sql = 'SELECT trip.id, locations.loc_name, bus.price_per_seat, trip.seat, trip.departure_date ' \
              'FROM trip ' \
              'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
              'INNER JOIN bus ON trip.bus_id = bus.id'
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        if result:
            for x in result:
                self.ids.trip_table_content.add_widget(
                    MDLabel(
                        text=f"{x[0]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                self.ids.trip_table_content.add_widget(
                    MDLabel(
                        text=f"{x[1]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                self.ids.trip_table_content.add_widget(
                    MDLabel(
                        text=f"$ {x[2]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                self.ids.trip_table_content.add_widget(
                    MDLabel(
                        text=f"{x[3]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                self.ids.trip_table_content.add_widget(
                    MDLabel(
                        text=f"{x[4]}",
                        size_hint_y=None,
                        height=50
                    )
                )
        else:
            pass

    def show_bus_table(self):
        self.ids.bus_table_content.clear_widgets()
        sql = 'SELECT bus.id, bus.bus_name, bus_type.type_name, bus.bus_desc, ' \
              'bus.num_of_seat, bus.price_per_seat, bus.status ' \
              'FROM bus ' \
              'INNER JOIN bus_type ON bus.type_id = bus_type.id'
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        if result:
            for x in result:
                status = "Active"
                if x[6] == 0:
                    status = "Inactive"
                else:
                    status = "Active"
                self.ids.bus_table_content.add_widget(
                    MDLabel(
                        text=f"{x[0]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                self.ids.bus_table_content.add_widget(
                    MDLabel(
                        text=f"{x[1]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                self.ids.bus_table_content.add_widget(
                    MDLabel(
                        text=f"{x[2]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                self.ids.bus_table_content.add_widget(
                    MDLabel(
                        text=f"{x[3]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                self.ids.bus_table_content.add_widget(
                    MDLabel(
                        text=f"{x[4]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                self.ids.bus_table_content.add_widget(
                    MDLabel(
                        text=f"$ {x[5]}",
                        size_hint_y=None,
                        height=50
                    )
                )
                if status == "Active":
                    self.ids.bus_table_content.add_widget(
                        MDLabel(
                            text=f"{status}",
                            size_hint_y=None,
                            height=50,
                            theme_text_color="Custom",
                            text_color=(0, 1, 0, 1)
                        )
                    )
                else:
                    self.ids.bus_table_content.add_widget(
                        MDLabel(
                            text=f"{status}",
                            size_hint_y=None,
                            height=50,
                            theme_text_color="Custom",
                            text_color=(1, 0, 0, 1)
                        )
                    )
        else:
            pass

    #FIXME
    def add_user(self):
        pass

    #FIXME
    def update_user(self):
        pass

    #FIXME
    def remove_user(self):
        pass

    def add_bus(self, name, price, bus_type):
        bus_type_list = ["Express", "VIP"]
        if name == "" or price == "":
            self.ids.bus_name_fld.error = True
            self.ids.bus_price_fld.error = True
        elif bus_type not in bus_type_list:
            self.dialog = MDDialog(
                title="All Field Required!",
                text="Please Input All Field",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if bus_type == "Express":
                type_id = 1
            else:
                type_id = 2
            try:
                sql = 'INSERT INTO bus (bus_name, price_per_seat, type_id, created_date) ' \
                      'VALUES (%s,%s,%s,%s)'
                values = [name, float(price), type_id, str(date), ]
                self.mycursor.execute(sql, values)
                self.mydb.commit()
            except:
                self.dialog = MDDialog(
                    title="Error!",
                    text="Cannot Add New Bus!",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
            else:
                self.dialog = MDDialog(
                    title="Success!",
                    text="New Bus Added Successfully!",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

    def update_bus(self, bus_id, price, bus_status):
        status_list = ["Active", "Inactive"]
        id_list = []
        sql = 'SELECT id FROM bus'
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        for x in result:
            id_list.append(x[0])
        if bus_id == "" or price == "":
            self.ids.bus_id_fld.error = True
            self.ids.update_price_fld.error = True
        elif bus_id not in id_list:
            self.ids.bus_id_fld. error = True
        elif bus_status not in status_list:
            self.dialog = MDDialog(
                title="All Field Required!",
                text="Please input all field",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            if bus_status == "Inactive":
                status = 0
            else:
                status = 1
            try:
                sql = 'UPDATE bus SET price_per_seat=%s, status=%s ' \
                      'WHERE id=%s '
                values = [float(price), status, int(bus_id), ]
                self.mycursor.execute(sql, values)
                self.mydb.commit()
            except:
                self.dialog = MDDialog(
                    title="Error!",
                    text="Cannot Update Bus at the moment!",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
            else:
                self.ids.bus_id_fld.text = ""
                self.ids.update_price_fld.text = ""
                self.dialog = MDDialog(
                    title="Success!",
                    text="Updated Successfully!",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

    #FIXME
    def add_trip(self, location, price):
        pass

    #FIXME
    def update_trip(self):
        pass

    #FIXME (DONE)
    def update_password(self, old_pass, new_pass, confirm_pass):
        sql = 'SELECT user_pass FROM users WHERE user_name=%s'
        values = [self.ids.nav_drawer_header.text, ]
        self.mycursor.execute(sql, values)
        result = self.mycursor.fetchall()
        u_pass = result[0][0]
        print(u_pass)
        if old_pass == "" or new_pass == "" or confirm_pass == "":
            self.dialog = MDDialog(
                title="All Fields Required!",
                text="Please fill in all fields to continue",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            if old_pass != u_pass:
                self.ids.old_pass.error = True
            else:
                if new_pass != confirm_pass:
                    self.ids.confirm_pass.error = True
                else:
                    try:
                        sql = 'UPDATE users SET user_pass = %s WHERE user_name =%s'
                        values = [new_pass, self.ids.nav_drawer_header.text, ]
                        self.mycursor.execute(sql, values)
                        self.mydb.commit()
                    except:
                        self.dialog = MDDialog(
                            title="Error!",
                            text="Cannot Change Password!",
                            buttons=[
                                MDFlatButton(
                                    text="Close",
                                    on_release=self.close_dialog
                                )
                            ]
                        )
                        self.dialog.open()
                    else:
                        self.dialog = MDDialog(
                            title="Success!",
                            text="Your Password has been updated!",
                            buttons=[
                                MDFlatButton(
                                    text="Close",
                                    on_release=self.close_dialog
                                )
                            ]
                        )
                        self.dialog.open()

    #FIXME (DONE)
    def update_info(self, first_name, last_name, phone, email, dob):
        if first_name == "" or last_name == "":
            f_name = None
            l_name = None
        else:
            f_name = first_name
            l_name = last_name
        if phone == "":
            phone_num = None
        else:
            phone_num = phone

        if dob == "":
            u_dob = None
        else:
            u_dob = dob
        if email == "":
            self.ids.email_fld.error = True
        else:
            email_addr = email
            try:
                sql = 'UPDATE users SET ' \
                      'first_name = %s, ' \
                      'last_name = %s, ' \
                      'phone = %s, ' \
                      'email = %s, ' \
                      'date_of_birth = %s ' \
                      'WHERE user_name = %s '
                values = [f_name, l_name, phone_num, email_addr, u_dob, self.ids.nav_drawer_header.text, ]
                self.mycursor.execute(sql, values)
                self.mydb.commit()
            except:
                self.dialog = MDDialog(
                    title="Error!",
                    text="Cannot Update User",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
            else:
                self.dialog = MDDialog(
                    title="Success!",
                    text="User Info Updated Successfully!",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

    def dob_date_picker(self):
        self.dob_date = MDDatePicker(
            min_year=1950,
            max_year=2050,
            primary_color=(0, 0, 0, 1),
            selector_color=(0, 0, 0, 1),
            text_button_color=(0, 0, 0, 1),
            text_current_color=(0, 0, 0, 1),
            input_field_text_color=(0, 0, 0, 1)
        )
        self.dob_date.bind(on_save=self.save_dob_date, on_cancel=self.close_dob_date_picker)
        self.dob_date.open()

    def save_dob_date(self, instance, value, date_range):
        date = value.strftime("%d-%m-%Y")
        self.ids.dob_fld.text = str(date)

    def close_dob_date_picker(self, instance, value):
        self.dob_date.dismiss(force=True)

    def goto_main_screen(self):
        self.show_user_table()
        self.ids.scrn_mngr.transition.direction = "right"
        self.ids.scrn_mngr.current = "main_scrn"
        self.ids.toolbar.right_action_items = []

    def goto_edit_profile(self):
        sql = 'SELECT first_name, last_name, phone, email, date_of_birth ' \
              'FROM users WHERE user_name=%s'
        values = [self.ids.nav_drawer_header.text, ]
        self.mycursor.execute(sql, values)
        result = self.mycursor.fetchone()
        self.ids.first_name_fld.text = result[0] if result[0] else ""
        self.ids.last_name_fld.text = result[1] if result[1] else ""
        self.ids.phone_fld.text = result[2] if result[2] else ""
        self.ids.email_fld.text = result[3] if result[3] else ""
        self.ids.dob_fld.text = result[4] if result[4] else ""
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_edit_profile"

    def goto_settings(self):
        self.ids.old_pass.text = ""
        self.ids.new_pass.text = ""
        self.ids.confirm_pass.text = ""
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_settings"

    def goto_add_user(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_add_user"

    def goto_update_user(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_update_user"

    def goto_remove_user(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_remove_user"

    def goto_add_trip(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_add_trip"

    def goto_update_trip(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_update_trip"

    def goto_bus(self):
        self.show_bus_table()
        if self.ids.scrn_mngr.current == "scrn_add_bus" or self.ids.scrn_mngr.current == "scrn_update_bus":
            self.ids.scrn_mngr.transition.direction = "right"
        else:
            self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_bus"

        self.show_bus_table()

    def goto_add_bus(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_add_bus"

    def goto_update_bus(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_update_bus"

    def goto_transaction(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_transaction"

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
