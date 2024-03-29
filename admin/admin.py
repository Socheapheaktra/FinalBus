from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang.builder import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout

from kivy.properties import StringProperty

import datetime
import requests

Builder.load_file("admin/admin.kv")

selected_booking_id = 0
baseURL = "https://bus-api.vercel.app/"
localhost = "http://127.0.0.1:5000/"

class BusStatusField(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = StringProperty()

    def reset(self):
        self.ids.textfield.text = ""

class BusTypeField(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = StringProperty()

    def reset(self):
        self.ids.textfield.text = ""

class UserTypeField(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = StringProperty()

class NoData(MDFloatLayout):
    text = "No Data"
    icon = "database"

class Transaction(MDCard, FakeRectangularElevationBehavior):
    booking_id = StringProperty()
    trip_id = StringProperty()
    destination = StringProperty()
    booking_date = StringProperty()
    price = StringProperty()
    bus_name = StringProperty()
    seat = StringProperty()
    paid_status = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_release=lambda x: self.get_booking_id())

    def get_booking_id(self):
        global selected_booking_id
        selected_booking_id = int(self.booking_id)

class TransactionSummary(GridLayout):
    username = StringProperty()
    destination = StringProperty()
    departure_date = StringProperty()
    passenger = StringProperty("-")
    seat_no = StringProperty("-")
    unit_price = StringProperty()
    total_payment = StringProperty("0.00")
    paid_status = StringProperty()

class AdminWindow(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.mydb = mysql.connector.connect(
        #     host='localhost',
        #     database='bus_reservation',
        #     user='root',
        #     passwd='',
        # )
        # self.mycursor = self.mydb.cursor()

        self.dialog = None
        self.dob_date = None
        self.departure_date = None
        self.menu = None

        self.show_user_table()

    # API Done
    def show_user_table(self):
        self.ids.user_table_content.clear_widgets()
        # sql = 'SELECT user_id, user_name, user_pass, first_name, last_name, date_of_birth, ' \
        #       'email, phone, user_desc, status FROM users'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        try:
            req = requests.request("GET", f"{baseURL}showUserTable")
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is False:
                self.dialog = MDDialog(
                    title="Error!",
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
                for data in response['data']:
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['user_id'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['username'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['password'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['first_name'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['last_name'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['dob'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['email'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['phone'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['role'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.user_table_content.add_widget(
                        MDLabel(
                            text=data['status'],
                            size_hint_y=None,
                            height=dp(50),
                            theme_text_color="Custom",
                            text_color=(0, 1, 0, 1) if data['status'] == "Active" else (1, 0, 0, 1)
                        )
                    )

    # API Done
    def show_trip_table(self):
        self.ids.trip_table_content.clear_widgets()
        # sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, ' \
        #       'bus.price, trip.seat, trip.departure_date, ' \
        #       'trip.departure_time, trip.status ' \
        #       'FROM trip ' \
        #       'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
        #       'INNER JOIN bus ON trip.bus_id = bus.id'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        try:
            req = requests.request("GET", f"{baseURL}showTripTable")
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['data']:
                for data in response['data']:
                    self.ids.trip_table_content.add_widget(
                        MDLabel(
                            text=data['trip_id'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.trip_table_content.add_widget(
                        MDLabel(
                            text=data['bus_name'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.trip_table_content.add_widget(
                        MDLabel(
                            text=data['location'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.trip_table_content.add_widget(
                        MDLabel(
                            text=f"$ {data['price']}",
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.trip_table_content.add_widget(
                        MDLabel(
                            text=data['seat'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.trip_table_content.add_widget(
                        MDLabel(
                            text=data['departure_date'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.trip_table_content.add_widget(
                        MDLabel(
                            text=data['departure_time'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.trip_table_content.add_widget(
                        MDLabel(
                            text=data['status'],
                            theme_text_color="Custom",
                            text_color=(0, 1, 0, 1) if data['status'] == "Active" else (1, 0, 0, 1),
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
            else:
                pass

    # API Done
    def show_bus_table(self):
        # self.ids.bus_table_content.clear_widgets()
        # sql = 'SELECT bus.id, bus.bus_name, bus_type.type_name, bus.bus_desc, ' \
        #       'bus.num_of_seat, bus.price, bus.status ' \
        #       'FROM bus ' \
        #       'INNER JOIN bus_type ON bus.type_id = bus_type.id'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        try:
            req = requests.request("GET", f"{baseURL}showBusTable")
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['data']:
                for data in response['data']:
                    self.ids.bus_table_content.add_widget(
                        MDLabel(
                            text=data['bus_id'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.bus_table_content.add_widget(
                        MDLabel(
                            text=data['bus_name'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.bus_table_content.add_widget(
                        MDLabel(
                            text=data['bus_type'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.bus_table_content.add_widget(
                        MDLabel(
                            text=data['bus_desc'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.bus_table_content.add_widget(
                        MDLabel(
                            text=data['seat'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.bus_table_content.add_widget(
                        MDLabel(
                            text=data['price'],
                            size_hint_y=None,
                            height=dp(50)
                        )
                    )
                    self.ids.bus_table_content.add_widget(
                        MDLabel(
                            text=data['status'],
                            size_hint_y=None,
                            height=dp(50),
                            theme_text_color="Custom",
                            text_color=(0, 1, 0, 1) if data['status'] == "Active" else (1, 0, 0, 1)
                        )
                    )
            else:
                pass

    # API Done
    def search_transaction(self, user_id="", search=False):
        # sql = 'SELECT DISTINCT user_id FROM booking'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        # for x in result:
        #     uid_list.append(x[0])

        req = requests.request("GET",
                               f"{baseURL}getDistinctUserID")
        response = req.json()
        uid_list = response['data']

        def add_transaction_item(transaction_detail):
            self.ids.transaction.add_widget(transaction_detail)

        self.ids.transaction.clear_widgets()
        # for uid in uid_list:
        if search:
            if user_id == "":
                self.show_transaction()
            elif int(user_id) in uid_list:
                for uid in uid_list:
                    if int(user_id) == uid:
                        self.ids.transaction.clear_widgets()
                        body = {
                            "uid": uid
                        }
                        req = requests.request("POST",
                                               f"{baseURL}searchTransaction",
                                               json=body)

                        response = req.json()
                        # Get booking_id FROM booking
                        # booking = list()
                        # sql = 'SELECT id FROM booking ' \
                        #       'WHERE user_id = %s ' \
                        #       'ORDER BY booking_date DESC'
                        # values = [uid, ]
                        # self.mycursor.execute(sql, values)
                        # result = self.mycursor.fetchall()
                        # for x in result:
                        #     booking.append(x[0])
                        #
                        # # Get booking_date and price FROM booking
                        # for booking_id in booking:
                        #     sql = 'SELECT booking_date, payment, status FROM booking ' \
                        #           'WHERE id = %s'
                        #     values = [booking_id, ]
                        #     self.mycursor.execute(sql, values)
                        #     result = self.mycursor.fetchone()
                        #     booking_date = result[0]
                        #     price = result[1]
                        #     paid_status = "Paid" if result[2] == 1 else "Not Paid"
                        #
                        # # Get seat_name FROM booking
                        #     seat = list()
                        #     sql = 'SELECT seat_name FROM bus_seat ' \
                        #           'WHERE id IN (SELECT seat_id FROM booking_detail WHERE booking_id = %s)'
                        #     values = [booking_id, ]
                        #     self.mycursor.execute(sql, values)
                        #     result = self.mycursor.fetchall()
                        #     for x in result:
                        #         seat.append(x[0])
                        #
                        # # Get trip_id
                        #     sql = 'SELECT DISTINCT trip_id FROM booking_detail ' \
                        #           'WHERE booking_id = %s'
                        #     values = [booking_id, ]
                        #     self.mycursor.execute(sql, values)
                        #     result = self.mycursor.fetchone()
                        #     trip_id = result[0]

                        # Get destination and bus_name
                        #     sql = 'SELECT locations.loc_name, bus.bus_name ' \
                        #           'FROM trip ' \
                        #           'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
                        #           'INNER JOIN bus ON trip.bus_id = bus.id ' \
                        #           'WHERE trip.id = %s'
                        #     values = [trip_id, ]
                        #     self.mycursor.execute(sql, values)
                        #     result = self.mycursor.fetchone()
                        #     destination = result[0]
                        #     bus_name = result[1]
                        for data in response['data']:
                            tran = Transaction(
                                booking_id=data['booking_id'],
                                trip_id=data['trip_id'],
                                destination=data['destination'],
                                booking_date=data['booking_date'],
                                price=data['price'],
                                bus_name=data['bus_name'],
                                seat=data['seat'],
                                paid_status=data['paid_status'],
                                on_release=lambda a=Transaction: self.show_transaction_detail(a)
                            )
                            add_transaction_item(tran)
            else:
                self.ids.transaction.clear_widgets()
                self.ids.transaction.add_widget(
                    MDLabel(
                        text="Not Found",
                        halign="center",
                        font_style="H2",
                        bold=True
                    )
                )

    # API Done
    def show_transaction(self):
        self.ids.transaction.clear_widgets()
        # booking = list()
        # sql = 'SELECT id FROM booking ' \
        #       'ORDER BY booking_date DESC'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        try:
            req = requests.request("GET",
                                   f"{baseURL}showTransaction")
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if not response['data']:
                self.ids.transaction.add_widget(NoData())
            else:
                for data in response['data']:
                    self.ids.transaction.add_widget(
                        Transaction(
                            booking_id=str(data['booking_id']),
                            trip_id=str(data['trip_id']),
                            destination=data['destination'],
                            booking_date=str(data['booking_date']),
                            price=str(data['price']),
                            bus_name=data['bus_name'],
                            seat=data['seat'],
                            paid_status=data['paid_status'],
                            on_release=lambda a=Transaction: self.show_transaction_detail(a)
                        )
                    )
                self.ids.transaction.add_widget(
                    MDLabel(
                        text=""
                    )
                )

    # API Done
    def show_transaction_detail(self, booking):
        body = {
            'booking_id': booking.booking_id,
            "trip_id": booking.trip_id
        }

        req = requests.request("POST",
                               f"{baseURL}showTransactionDetail",
                               json=body)
        response = req.json()

        self.ids.transaction_summary.clear_widgets()
        self.ids.transaction_summary.add_widget(TransactionSummary(
            username=response['data']['username'],
            destination=response['data']['destination'],
            departure_date=response['data']['departure_date'],
            unit_price=response['data']['unit_price'],
            seat_no=booking.seat,
            total_payment=booking.price,
            passenger=str(len(booking.seat.split(","))),
            paid_status=booking.paid_status
        ))
        self.ids.btn_update_transaction.disabled = True if booking.paid_status == "Paid" else False

        self.goto_transaction_detail()

    def update_transaction(self):
        self.dialog = MDDialog(
            title="Confirm",
            text="Confirm update transaction status?",
            buttons=[
                MDFlatButton(
                    text="Yes",
                    on_release=lambda x: self.confirm_update_transaction(selected_booking_id)
                ),
                MDFlatButton(
                    text="No",
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()

    # API Done
    def confirm_update_transaction(self, booking_id):
        self.close_dialog()
        try:
            req = requests.request(
                "POST",
                f"{baseURL}updateTransaction",
                json={"booking_id": booking_id}
            )
            # sql = 'UPDATE booking, payment_offline ' \
            #       'SET booking.status = 1, payment_offline.pay_status = 1 ' \
            #       'WHERE booking.id = %s AND payment_offline.booking_id = %s'
            # values = [booking_id, booking_id, ]
            # self.mycursor.execute(sql, values)
            # self.mydb.commit()
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=lambda x:self.return_to_transaction()
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is True:
                self.dialog = MDDialog(
                    title="Success!",
                    text=f"{response['message']}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=lambda x:self.return_to_transaction()
                        )
                    ]
                )
                self.dialog.open()
            else:
                self.dialog = MDDialog(
                    title="Error!",
                    text=f"{response['message']}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=lambda x: self.return_to_transaction()
                        )
                    ]
                )

    def return_to_transaction(self):
        self.close_dialog()
        self.goto_transaction()
        self.show_transaction()

    # API Done
    def add_user(self, username, password, email):
        try:
            body = {
                "username": username,
                "password": password,
                "email": email
            }
            req = requests.request(
                "POST",
                f"{baseURL}admin/addUser",
                json=body
            )
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is False:
                self.dialog = MDDialog(
                    title="Error!",
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
                self.dialog = MDDialog(
                    title="Success!",
                    text=response['message'],
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

                self.ids.add_username_fld.text = ""
                self.ids.add_password_fld.text = ""
                self.ids.add_email_fld.text = ""
        # GET REGISTERED USERNAMES AND EMAILS
        # username_ls = []
        # email_ls = []
        # sql = 'SELECT user_name, email FROM users'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        # for x in result:
        #     username_ls.append(x[0])
        #     email_ls.append(x[1])
        # if username in username_ls:
        #     self.ids.add_username_fld.error = True
        # elif password == "":
        #     self.ids.add_password_fld.error = True
        # else:
        #     if email == "":
        #         self.ids.add_email_fld.helper_text = "Invalid Email"
        #         self.ids.add_email_fld.error = True
        #     elif email in email_ls:
        #         self.ids.add_email_fld.helper_text = "This Email has already been used"
        #         self.ids.add_email_fld.error = True
        #     else:
        #         try:
        #             sql = 'INSERT INTO users (user_name, user_pass, email) ' \
        #                   'VALUES (%s, %s, %s)'
        #             values = [username, password, email, ]
        #             self.mycursor.execute(sql, values)
        #             self.mydb.commit()
        #         except:
        #             self.dialog = MDDialog(
        #                 title="Error!",
        #                 text="Cannot add new account",
        #                 buttons=[
        #                     MDFlatButton(
        #                         text="Close",
        #                         on_release=self.close_dialog
        #                     )
        #                 ]
        #             )
        #             self.dialog.open()
        #         else:
        #             self.dialog = MDDialog(
        #                 title="Success!",
        #                 text="New account added successfully!",
        #                 buttons=[
        #                     MDFlatButton(
        #                         text="Close",
        #                         on_release=self.close_dialog
        #                     )
        #                 ]
        #             )
        #             self.dialog.open()

    # API Done
    def update_user(self, username, password, email, phone, role):
        body = {
            "username": username,
            "password": password,
            "email": email,
            "phone": phone,
            "role": role
        }
        try:
            req = requests.request(
                "POST",
                f"{baseURL}admin/updateUser",
                json=body
            )
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is False:
                self.dialog = MDDialog(
                    title="Error!",
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
                self.dialog = MDDialog(
                    title="Success!",
                    text=f"{response['message']}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
        # username_list = []
        # role_list = ['Admin', 'User']
        # sql = 'SELECT user_name FROM users'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        # for x in result:
        #     username_list.append(x[0])
        # if username not in username_list:
        #     self.ids.update_username_fld.error = True
        # else:
        #     if password != "":
        #         u_pass = password
        #     else:
        #         sql = 'SELECT user_pass FROM users WHERE user_name = %s'
        #         values = [username, ]
        #         self.mycursor.execute(sql, values)
        #         result = self.mycursor.fetchone()
        #         u_pass = result[0]
        #     if email != "":
        #         u_email = email
        #     else:
        #         sql = 'SELECT email FROM users WHERE user_name = %s'
        #         values = [username, ]
        #         self.mycursor.execute(sql, values)
        #         result = self.mycursor.fetchone()
        #         u_email = result[0]
        # if phone == "":
        #     u_phone = None
        # else:
        #     u_phone = phone
        # if role not in role_list:
        #     self.dialog = MDDialog(
        #         title="Please Select A Role!",
        #         buttons=[
        #             MDFlatButton(
        #                 text="Close",
        #                 on_release=self.close_dialog
        #             )
        #         ]
        #     )
        #     self.dialog.open()
        # else:
        #     u_role = role
        #     try:
        #         sql = 'UPDATE users SET user_pass=%s, email=%s, phone=%s, user_desc=%s ' \
        #               'WHERE user_name=%s'
        #         values = [u_pass, u_email, u_phone, u_role, username, ]
        #         self.mycursor.execute(sql, values)
        #         self.mydb.commit()
        #     except:
        #         self.dialog = MDDialog(
        #             title="Error!",
        #             text="Cannot Update User Info!",
        #             buttons=[
        #                 MDFlatButton(
        #                     text="Close",
        #                     on_release=self.close_dialog
        #                 )
        #             ]
        #         )
        #         self.dialog.open()
        #     else:
        #         self.dialog = MDDialog(
        #             title="Success!",
        #             text=f"User {username} has been updated successfully!",
        #             buttons=[
        #                 MDFlatButton(
        #                     text="Close",
        #                     on_release=self.close_dialog
        #                 )
        #             ]
        #         )
        #         self.dialog.open()

    # API Done
    def remove_user_dialog(self, username):
        # username_list = []
        # sql = 'SELECT user_name FROM users'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        # for x in result:
        #     username_list.append(x[0])
        try:
            req = requests.request("GET", f"{baseURL}admin/getUsername")
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is False:
                self.dialog = MDDialog(
                    title="Error!",
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
                if username not in response['data']:
                    self.ids.remove_username_fld.error = True
                else:
                    self.dialog = MDDialog(
                        title="Please Confirm!",
                        text=f"Are you sure you want to remove user {username}?",
                        buttons=[
                            MDFlatButton(
                                text="No",
                                on_release=self.close_dialog
                            ),
                            MDFlatButton(
                                text="Yes",
                                on_release=lambda x: self.remove_user(username)
                            )
                        ]
                    )
                    self.dialog.open()

    # API Done
    def remove_user(self, username):
        self.close_dialog()
        try:
            req = requests.request(
                "POST",
                f"{baseURL}admin/removeUser",
                json={"username": username}
            )
            # sql = 'DELETE FROM users WHERE user_name=%s'
            # values = [username, ]
            # self.mycursor.execute(sql, values)
            # self.mydb.commit()
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is False:
                self.dialog = MDDialog(
                    title="Error!",
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
                self.dialog = MDDialog(
                    title="Success!",
                    text=f"{response['message']}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

                self.ids.remove_username_fld.text = ""

    # API Done
    def add_bus(self, name, location, price, bus_type):
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        body = {
            "bus_name": str(name),
            "location": str(location),
            "price": str(price),
            "bus_type": str(bus_type),
            "created_date": str(date),
        }
        try:
            req = requests.request(
                "POST",
                f"{baseURL}admin/addBus",
                json=body
            )
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is False:
                self.dialog = MDDialog(
                    title="Error!",
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
                self.dialog = MDDialog(
                    title="Success!",
                    text=response['message'],
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
        # Get Location_id (Foreign Key)
        # sql = 'SELECT loc_id FROM locations ' \
        #       'WHERE loc_name = %s'
        # values = [location, ]
        # self.mycursor.execute(sql, values)
        # result = self.mycursor.fetchone()
        # loc_id = result[0]
        #
        # bus_type_list = ["Express", "VIP"]
        # if name == "" or price == "":
        #     self.ids.bus_name_fld.error = True
        #     self.ids.bus_price_fld.error = True
        # elif bus_type not in bus_type_list:
        #     self.dialog = MDDialog(
        #         title="All Field Required!",
        #         text="Please Input All Field",
        #         buttons=[
        #             MDFlatButton(
        #                 text="Close",
        #                 on_release=self.close_dialog
        #             )
        #         ]
        #     )
        #     self.dialog.open()
        # else:
        #     date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #     if bus_type == "Express":
        #         type_id = 1
        #     else:
        #         type_id = 2
        #     try:
        #         sql = 'INSERT INTO bus (bus_name, loc_id, price, type_id, created_date) ' \
        #               'VALUES (%s,%s,%s,%s)'
        #         values = [name, loc_id, float(price), type_id, str(date), ]
        #         self.mycursor.execute(sql, values)
        #         self.mydb.commit()
        #     except:
        #         self.dialog = MDDialog(
        #             title="Error!",
        #             text="Cannot Add New Bus!",
        #             buttons=[
        #                 MDFlatButton(
        #                     text="Close",
        #                     on_release=self.close_dialog
        #                 )
        #             ]
        #         )
        #         self.dialog.open()
        #     else:
        #         self.dialog = MDDialog(
        #             title="Success!",
        #             text="New Bus Added Successfully!",
        #             buttons=[
        #                 MDFlatButton(
        #                     text="Close",
        #                     on_release=self.close_dialog
        #                 )
        #             ]
        #         )
        #         self.dialog.open()

    # API Done
    def update_bus(self, bus_id, price, bus_status):
        body = {
            "bus_id": str(bus_id),
            "price": str(price),
            "status": str(bus_status)
        }
        try:
            req = requests.request(
                "POST",
                f"{baseURL}admin/updateBus",
                json=body
            )
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is False:
                self.dialog = MDDialog(
                    title="Error!",
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
                self.dialog = MDDialog(
                    title="Success!",
                    text=response['message'],
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

                self.ids.bus_id_fld.text = ""
                self.ids.update_price_fld.text = ""
                self.ids.bus_status_fld.text = ""

        # status_list = ["Active", "Inactive"]
        # id_list = []
        # sql = 'SELECT id FROM bus'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        # for x in result:
        #     id_list.append(x[0])
        # if bus_id == "" or price == "":
        #     self.ids.bus_id_fld.error = True
        #     self.ids.update_price_fld.error = True
        # elif bus_id not in id_list:
        #     self.ids.bus_id_fld. error = True
        # elif bus_status not in status_list:
        #     self.dialog = MDDialog(
        #         title="All Field Required!",
        #         text="Please input all field",
        #         buttons=[
        #             MDFlatButton(
        #                 text="Close",
        #                 on_release=self.close_dialog
        #             )
        #         ]
        #     )
        #     self.dialog.open()
        # else:
        #     if bus_status == "Inactive":
        #         status = 0
        #     else:
        #         status = 1
        #     try:
        #         sql = 'UPDATE bus SET price_per_seat=%s, status=%s ' \
        #               'WHERE id=%s '
        #         values = [float(price), status, int(bus_id), ]
        #         self.mycursor.execute(sql, values)
        #         self.mydb.commit()
        #     except:
        #         self.dialog = MDDialog(
        #             title="Error!",
        #             text="Cannot Update Bus at the moment!",
        #             buttons=[
        #                 MDFlatButton(
        #                     text="Close",
        #                     on_release=self.close_dialog
        #                 )
        #             ]
        #         )
        #         self.dialog.open()
        #     else:
        #         self.ids.bus_id_fld.text = ""
        #         self.ids.update_price_fld.text = ""
        #         self.dialog = MDDialog(
        #             title="Success!",
        #             text="Updated Successfully!",
        #             buttons=[
        #                 MDFlatButton(
        #                     text="Close",
        #                     on_release=self.close_dialog
        #                 )
        #             ]
        #         )
        #         self.dialog.open()

    # API Done
    def add_trip(self, location, bus, depart_date, depart_time):
        if location == "" or bus == "" or depart_date == "" or depart_time == "":
            self.dialog = MDDialog(
                title="All Field Required!",
                text="Please fill in all fields!",
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
                "location": str(location),
                "bus_name": str(bus),
                "depart_date": str(depart_date),
                "depart_time": str(depart_time)
            }
            try:
                req = requests.request(
                    "POST",
                    f"{baseURL}addTrip",
                    json=body
                )
            except Exception as e:
                self.dialog = MDDialog(
                    title="Error!",
                    text=f"{e}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
            else:
                response = req.json()
                if response['status'] is False:
                    self.dialog = MDDialog(
                        title="Error!",
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
                    self.dialog = MDDialog(
                        title="Success!",
                        text=response['message'],
                        buttons=[
                            MDFlatButton(
                                text="Close",
                                on_release=self.close_dialog
                            )
                        ]
                    )
                    self.dialog.open()

            # sql = 'SELECT loc_id FROM locations WHERE loc_name=%s'
            # values = [location, ]
            # self.mycursor.execute(sql, values)
            # result = self.mycursor.fetchone()
            # loc_id = result[0]
            #
            # sql = 'SELECT id FROM bus WHERE bus_name=%s'
            # values = [bus, ]
            # self.mycursor.execute(sql, values)
            # result = self.mycursor.fetchone()
            # bus_id = result[0]
            #
            # temp = depart_date.split("-")
            # temp.reverse()
            # date = "-".join(temp)
            #
            # time = f"{date} {depart_time}"
            #
            # created_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #
            # try:
            #     sql = 'INSERT INTO trip(loc_id, bus_id, departure_date, departure_time, created_at) ' \
            #           'VALUES (%s, %s, %s, %s, %s)'
            #     values = [loc_id, bus_id, date, time, created_date, ]
            #     self.mycursor.execute(sql, values)
            #     self.mydb.commit()
            # except:
            #     self.dialog = MDDialog(
            #         title="Error!",
            #         text="Cannot Add New Trip!",
            #         buttons=[
            #             MDFlatButton(
            #                 text="Close",
            #                 on_release=self.close_dialog
            #             )
            #         ]
            #     )
            #     self.dialog.open()
            # else:
            #     sql = 'UPDATE bus SET status=0 ' \
            #           'WHERE id=%s'
            #     values = [bus_id, ]
            #     self.mycursor.execute(sql, values)
            #     self.mydb.commit()
            #     self.dialog = MDDialog(
            #         title="Success!",
            #         text="New Trip Added Successfully!",
            #         buttons=[
            #             MDFlatButton(
            #                 text="Close",
            #                 on_release=self.close_dialog
            #             )
            #         ]
            #     )
            #     self.dialog.open()

    # API Done
    def open_location_menu(self):
        # sql = 'SELECT loc_name FROM locations'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        items = list()
        try:
            req = requests.request("GET", f"{baseURL}admin/getLocationNames")
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            for data in response['data']:
                items.append(
                    {
                        "text": f"{data}",
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=f"{data}": self.set_trip_location(x)
                    }
                )
            if self.ids.scrn_mngr.current == "scrn_add_trip":
                self.menu = MDDropdownMenu(
                    caller=self.ids.add_trip_location_fld,
                    items=items,
                    width_mult=4,
                    ver_growth="down",
                    hor_growth="right",
                )
            elif self.ids.scrn_mngr.current == "scrn_add_bus":
                self.menu = MDDropdownMenu(
                    caller=self.ids.bus_location_fld,
                    items=items,
                    width_mult=4,
                    ver_growth="down",
                    hor_growth="right",
                )
            self.menu.open()

    def set_trip_location(self, location):
        if self.ids.scrn_mngr.current == "scrn_add_trip":
            self.ids.add_trip_location_fld.text = location
            self.ids.add_trip_location_fld.focus = False
            self.ids.add_trip_bus_fld.text = ""
        elif self.ids.scrn_mngr.current == "scrn_add_bus":
            self.ids.bus_location_fld.text = location
            self.ids.bus_location_fld.focus = False
        self.menu.dismiss()

    # API Done
    def open_bus_menu(self):
        # sql = 'SELECT loc_name FROM locations'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        # location_list = list()
        # items = list()
        # for location in result:
        #     location_list.append(location[0])
        # for location in location_list:
        #     if self.ids.add_trip_location_fld.text == location:
        #         sql = 'SELECT bus.bus_name FROM bus ' \
        #               'INNER JOIN locations ON bus.loc_id = locations.loc_id ' \
        #               'WHERE locations.loc_name = %s AND bus.status = 1'
        #         values = [location, ]
        #         self.mycursor.execute(sql, values)
        #         result = self.mycursor.fetchall()
        #         if not result:
        #             items.append(
        #                 {
        #                     "text": "No Bus Available",
        #                     "viewclass": "OneLineListItem"
        #                 }
        #             )
        #         else:
        #             for x in result:
        #                 items.append(
        #                     {
        #                         "text": f"{x[0]}",
        #                         "viewclass": "OneLineListItem",
        #                         "on_release": lambda a=f"{x[0]}": self.set_trip_bus(a)
        #                     }
        #                 )
        #     elif self.ids.add_trip_location_fld.text == "":
        #         sql = 'SELECT bus_name FROM bus WHERE status = 1'
        #         self.mycursor.execute(sql)
        #         result = self.mycursor.fetchall()
        #         if not result:
        #             items.append(
        #                 {
        #                     "text": "No Bus Available",
        #                     "viewclass": "OneLineListItem"
        #                 }
        #             )
        #         else:
        #             for x in result:
        #                 items.append(
        #                     {
        #                         "text": f"{x[0]}",
        #                         "viewclass": "OneLineListItem",
        #                         "on_release": lambda a=f"{x[0]}": self.set_trip_bus(a)
        #                     }
        #                 )
        items = list()
        location = self.ids.add_trip_location_fld.text
        try:
            req = requests.request(
                "POST",
                f"{baseURL}getActiveBus",
                json={'location': location}
            )
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is True:
                if not response['data']:
                    items.append(
                        {
                            "text": f"{response['message']}",
                            "viewclass": "OneLineListItem"
                        }
                    )
                else:
                    for bus in response['data']:
                        items.append(
                            {
                                "text": f"{bus}",
                                "viewclass": "OneLineListItem",
                                "on_release": lambda a=f"{bus}": self.set_trip_bus(a)
                            }
                        )
            self.menu = MDDropdownMenu(
                caller=self.ids.add_trip_bus_fld,
                items=items,
                width_mult=4,
                ver_growth="down",
                hor_growth="right",
            )
            self.menu.open()

    def set_trip_bus(self, bus):
        self.ids.add_trip_bus_fld.text = bus
        self.ids.add_trip_bus_fld.focus = False
        self.menu.dismiss()

    def open_departure_time_menu(self):
        time_list = ['8:00:00', '14:00:00', "17:00:00"]
        items = list()
        for time in time_list:
            items.append(
                {
                    "text": f"{time}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"{time}": self.set_trip_departure_time(x)
                }
            )
        if self.ids.scrn_mngr.current == "scrn_add_trip":
            self.menu = MDDropdownMenu(
                caller=self.ids.add_trip_departure_time_fld,
                items=items,
                width_mult=4,
                ver_growth="down",
                hor_growth="right",
            )
        elif self.ids.scrn_mngr.current == "scrn_update_trip":
            self.menu = MDDropdownMenu(
                caller=self.ids.update_trip_departure_time_fld,
                items=items,
                width_mult=4,
                ver_growth="down",
                hor_growth="right",
            )
        self.menu.open()

    def set_trip_departure_time(self, time):
        if self.ids.scrn_mngr.current == "scrn_add_trip":
            self.ids.add_trip_departure_time_fld.text = time
            self.ids.add_trip_departure_time_fld.focus = False
        elif self.ids.scrn_mngr.current == "scrn_update_trip":
            self.ids.update_trip_departure_time_fld.text = time
            self.ids.update_trip_departure_time_fld.focus = False
        self.menu.dismiss()

    # API Done
    def update_trip(self, trip_id, depart_date, depart_time):
        # Check if user has input in all field
        if trip_id == "" or depart_date == "" or depart_time == "":
            self.dialog = MDDialog(
                title="All Fields Required!",
                text="Please fill in all field!",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            temp = depart_date.split("-")
            temp.reverse()
            date = "-".join(temp)
            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # sql = 'UPDATE trip SET departure_date=%s, departure_time=%s, updated_at=%s ' \
                #       'WHERE id=%s'
                # values = [date, depart_time, update_time, trip_id, ]
                # self.mycursor.execute(sql, values)
                # self.mydb.commit()
                body = {
                    "trip_id": trip_id,
                    "departure_date": date,
                    "departure_time": depart_time,
                    "update_at": update_time
                }
                req = requests.request(
                    "POST",
                    f"{baseURL}updateTrip",
                    json=body
                )
            except Exception as e:
                self.dialog = MDDialog(
                    title="Error!",
                    text=f"{e}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
            else:
                response = req.json()
                if response['status'] is True:
                    self.dialog = MDDialog(
                        title="Success!",
                        text=response['message'],
                        buttons=[
                            MDFlatButton(
                                text="Close",
                                on_release=self.close_dialog
                            )
                        ]
                    )
                    self.dialog.open()
                    self.set_trip_detail(trip_id)
                    self.ids.update_trip_departure_date_fld.secondary_text = "Add Departure Date"
                    self.ids.update_trip_departure_time_fld.text = ""
                else:
                    self.dialog = MDDialog(
                        title="Error!",
                        text=response['message'],
                        buttons=[
                            MDFlatButton(
                                text="Close",
                                on_release=self.close_dialog
                            )
                        ]
                    )
                    self.dialog.open()

    def end_trip(self, trip_id):
        """ SET Trip Status to False and Bus Status to True """
        if trip_id == "":
            self.dialog = MDDialog(
                title="Missing Requirement!",
                text="Please select a trip id",
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
                title="Are you sure to end this trip?",
                buttons=[
                    MDFlatButton(
                        text="Yes",
                        on_release=lambda x: self.confirm_end_trip(trip_id)
                    ),
                    MDFlatButton(
                        text="No",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()

    # API Done
    def confirm_end_trip(self, trip_id):
        self.close_dialog()
        try:
            req = requests.request(
                "POST",
                f"{baseURL}endTrip",
                json={"trip_id": trip_id}
            )
            # sql = 'UPDATE trip, bus, bus_seat ' \
            #       'SET trip.status = 0, bus.status = 1, bus_seat.status = 1 ' \
            #       'WHERE trip.id = %s AND trip.bus_id = bus.id AND trip.bus_id = bus_seat.bus_id'
            # values = [trip_id, ]
            # self.mycursor.execute(sql, values)
            # self.mydb.commit()
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is True:
                self.dialog = MDDialog(
                    title="Success!",
                    text=f"{response['message']}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

                self.ids.update_trip_detail.clear_widgets()
                self.ids.update_trip_id_fld.text = ""
                self.ids.update_trip_departure_date_fld.secondary_text = "Add Departure Date"
                self.ids.update_trip_departure_time_fld.text = ""
            else:
                self.dialog = MDDialog(
                    title="Error!",
                    text=f"{response['message']}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

    # API Done
    def open_trip_menu(self):
        # sql = 'SELECT id FROM trip WHERE status = 1'
        # self.mycursor.execute(sql)
        # result = self.mycursor.fetchall()
        items = list()
        try:
            req = requests.request("GET", f"{baseURL}getActiveTrip")
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if not response['data']:
                items.append(
                    {
                        "text": "No Trip Available",
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x: self.menu.dismiss()
                    }
                )
            for trip_id in response['data']:
                items.append(
                    {
                        "text": f"{trip_id}",
                        "viewclass": "OneLineListItem",
                        "on_release": lambda a=f"{trip_id}": self.set_trip_detail(a)
                    }
                )
            self.menu = MDDropdownMenu(
                caller=self.ids.update_trip_id_fld,
                items=items,
                width_mult=4,
                ver_growth="down",
                hor_growth="right",
            )
            self.menu.open()

    # API Done
    def set_trip_detail(self, trip_id):
        self.ids.update_trip_detail.clear_widgets()
        self.ids.update_trip_id_fld.text = trip_id

        # sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, trip.departure_date, trip.departure_time ' \
        #       'FROM trip ' \
        #       'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
        #       'INNER JOIN bus ON trip.bus_id = bus.id ' \
        #       'WHERE trip.id=%s'
        # values = [trip_id, ]
        # self.mycursor.execute(sql, values)
        # result = self.mycursor.fetchall()
        try:
            req = requests.request(
                "POST",
                f"{baseURL}getTripDetail",
                json={"trip_id": trip_id}
            )
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            data = response['data']
        # for x in result:
            self.ids.update_trip_detail.add_widget(
                MDLabel(
                    text=data['trip_id'],
                    size_hint_y=None,
                    height=50
                )
            )
            self.ids.update_trip_detail.add_widget(
                MDLabel(
                    text=data['bus_name'],
                    size_hint_y=None,
                    height=50
                )
            )
            self.ids.update_trip_detail.add_widget(
                MDLabel(
                    text=data['location'],
                    size_hint_y=None,
                    height=50
                )
            )
            self.ids.update_trip_detail.add_widget(
                MDLabel(
                    text=data['departure_date'],
                    size_hint_y=None,
                    height=50
                )
            )
            self.ids.update_trip_detail.add_widget(
                MDLabel(
                    text=data['departure_time'],
                    size_hint_y=None,
                    height=50
                )
            )

        self.menu.dismiss()

    # API Done
    def update_password(self, old_pass, new_pass, confirm_pass):
        # sql = 'SELECT user_pass FROM users WHERE user_name=%s'
        # values = [self.ids.nav_drawer_header.text, ]
        # self.mycursor.execute(sql, values)
        # result = self.mycursor.fetchall()
        # u_pass = result[0][0]
        username = self.ids.nav_drawer_header.text
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
            try:
                body = {
                    "username": username,
                    "old_pass": old_pass,
                    "new_pass": new_pass,
                    "confirm_pass": confirm_pass
                }
                req = requests.request(
                    "POST",
                    f"{baseURL}updateAdminPassword",
                    json=body
                )
            except Exception as e:
                self.dialog = MDDialog(
                    title="Error!",
                    text=f"{e}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
            else:
                response = req.json()
                if response['status'] is True:
                    self.dialog = MDDialog(
                        title="Success!",
                        text=f"{response['message']}",
                        buttons=[
                            MDFlatButton(
                                text="Close",
                                on_release=self.close_dialog
                            )
                        ]
                    )
                    self.dialog.open()

                    self.ids.old_pass.text = ""
                    self.ids.new_pass.text = ""
                    self.ids.confirm_pass.text = ""
                else:
                    self.dialog = MDDialog(
                        title="Error!",
                        text=f"{response['message']}",
                        buttons=[
                            MDFlatButton(
                                text="Close",
                                on_release=self.close_dialog
                            )
                        ]
                    )
                    self.dialog.open()

            # if old_pass != u_pass:
            #     self.ids.old_pass.error = True
            # else:
            #     if new_pass != confirm_pass:
            #         self.ids.confirm_pass.error = True
            #     else:
            #         try:
            #             sql = 'UPDATE users SET user_pass = %s WHERE user_name =%s'
            #             values = [new_pass, self.ids.nav_drawer_header.text, ]
            #             self.mycursor.execute(sql, values)
            #             self.mydb.commit()
            #         except:
            #             self.dialog = MDDialog(
            #                 title="Error!",
            #                 text="Cannot Change Password!",
            #                 buttons=[
            #                     MDFlatButton(
            #                         text="Close",
            #                         on_release=self.close_dialog
            #                     )
            #                 ]
            #             )
            #             self.dialog.open()
            #         else:
            #             self.dialog = MDDialog(
            #                 title="Success!",
            #                 text="Your Password has been updated!",
            #                 buttons=[
            #                     MDFlatButton(
            #                         text="Close",
            #                         on_release=self.close_dialog
            #                     )
            #                 ]
            #             )
            #             self.dialog.open()

    # API Done
    def update_info(self, first_name, last_name, phone, email, dob):
        username = self.ids.nav_drawer_header.text
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
                # sql = 'UPDATE users SET ' \
                #       'first_name = %s, ' \
                #       'last_name = %s, ' \
                #       'phone = %s, ' \
                #       'email = %s, ' \
                #       'date_of_birth = %s ' \
                #       'WHERE user_name = %s '
                # values = [f_name, l_name, phone_num, email_addr, u_dob, self.ids.nav_drawer_header.text, ]
                # self.mycursor.execute(sql, values)
                # self.mydb.commit()

                body = {
                    "username": username,
                    "first_name": f_name,
                    "last_name": l_name,
                    "phone": phone_num,
                    "email": email_addr,
                    "dob": u_dob
                }

                req = requests.request(
                    "POST",
                    f"{baseURL}updateAdminInfo",
                    json=body
                )

            except Exception as e:
                self.dialog = MDDialog(
                    title="Error!",
                    text=f"{e}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()
            else:
                response = req.json()
                if response['status'] is False:
                    self.dialog = MDDialog(
                        title="Error!",
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
                    self.goto_edit_profile()
                    self.dialog = MDDialog(
                        title="Success",
                        text="Your information has been updated!",
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

    def departure_date_picker(self):
        self.departure_date = MDDatePicker(
            primary_color=(0, 0, 0, 1),
            selector_color=(0, 0, 0, 1),
            text_button_color=(0, 0, 0, 1),
            text_current_color=(0, 0, 0, 1)
        )
        self.departure_date.bind(on_save=self.save_departure_date, on_cancel=self.close_departure_date_picker)
        self.departure_date.open()

    def save_departure_date(self, instance, value, date_range):
        date = value.strftime("%d-%m-%Y")
        if self.ids.scrn_mngr.current == "scrn_add_trip":
            self.ids.add_trip_departure_date_fld.secondary_text = str(date)
        elif self.ids.scrn_mngr.current == "scrn_update_trip":
            self.ids.update_trip_departure_date_fld.secondary_text = str(date)

    def close_departure_date_picker(self, instance, value):
        self.departure_date.dismiss(force=True)

    def goto_main_screen(self):
        self.show_user_table()
        self.show_trip_table()
        self.ids.scrn_mngr.transition.direction = "right"
        self.ids.scrn_mngr.current = "main_scrn"
        self.ids.toolbar.right_action_items = []

    # API Done
    def goto_edit_profile(self):
        # sql = 'SELECT first_name, last_name, phone, email, date_of_birth ' \
        #       'FROM users WHERE user_name=%s'
        # values = [self.ids.nav_drawer_header.text, ]
        # self.mycursor.execute(sql, values)
        # result = self.mycursor.fetchone()
        # self.ids.first_name_fld.text = result[0] if result[0] else ""
        # self.ids.last_name_fld.text = result[1] if result[1] else ""
        # self.ids.phone_fld.text = result[2] if result[2] else ""
        # self.ids.email_fld.text = result[3] if result[3] else ""
        # self.ids.dob_fld.text = result[4] if result[4] else ""

        username = self.ids.nav_drawer_header.text
        try:
            req = requests.request(
                "POST",
                f"{baseURL}getAdminInfo",
                json={"username": username}
            )
        except Exception as e:
            self.dialog = MDDialog(
                title="Error!",
                text=f"{e}",
                buttons=[
                    MDFlatButton(
                        text="Close",
                        on_release=self.close_dialog
                    )
                ]
            )
            self.dialog.open()
        else:
            response = req.json()
            if response['status'] is True:
                data = response['data']
                self.ids.first_name_fld.text = data['first_name'] if data['first_name'] else ""
                self.ids.last_name_fld.text = data['last_name'] if data['last_name'] else ""
                self.ids.phone_fld.text = data['phone'] if data['phone'] else ""
                self.ids.email_fld.text = data['email'] if data['email'] else ""
                self.ids.dob_fld.text = data['dob'] if data['dob'] else ""

                self.ids.scrn_mngr.transition.direction = "left"
                self.ids.scrn_mngr.current = "scrn_edit_profile"
            else:
                self.dialog = MDDialog(
                    title="Error!",
                    text=f"{response['message']}",
                    buttons=[
                        MDFlatButton(
                            text="Close",
                            on_release=self.close_dialog
                        )
                    ]
                )
                self.dialog.open()

    def goto_settings(self):
        self.ids.old_pass.text = ""
        self.ids.new_pass.text = ""
        self.ids.confirm_pass.text = ""
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_settings"

    def goto_add_user(self):
        self.ids.add_username_fld.text = ""
        self.ids.add_password_fld.text = ""
        self.ids.add_email_fld.text = ""
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_add_user"

    def goto_update_user(self):
        self.ids.update_username_fld.text = ""
        self.ids.update_password_fld.text = ""
        self.ids.update_email_fld.text = ""
        self.ids.update_phone_fld.text = ""
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_update_user"

    def goto_remove_user(self):
        self.ids.remove_username_fld.text = ""
        self.ids.remove_username_fld.error = False
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_remove_user"

    def goto_add_trip(self):
        self.ids.add_trip_location_fld.text = ""
        self.ids.add_trip_bus_fld.text = ""
        self.ids.add_trip_departure_date_fld.secondary_text = "Add Departure Date"
        self.ids.add_trip_departure_time_fld.text = ""
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_add_trip"

    def goto_update_trip(self):
        self.ids.update_trip_detail.clear_widgets()
        self.ids.update_trip_id_fld.text = ""
        self.ids.update_trip_departure_date_fld.secondary_text = "Add Departure Date"
        self.ids.update_trip_departure_time_fld.text = ""
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_update_trip"

    def goto_bus(self):
        self.show_bus_table()
        if self.ids.scrn_mngr.current == "scrn_add_bus" or self.ids.scrn_mngr.current == "scrn_update_bus":
            self.ids.scrn_mngr.transition.direction = "right"
        else:
            self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_bus"

    def goto_add_bus(self):
        self.ids.bus_name_fld.text = ""
        self.ids.bus_price_fld.text = ""
        self.ids.bus_type_fld.reset()
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_add_bus"

    def goto_update_bus(self):
        self.ids.bus_id_fld.text = ""
        self.ids.update_price_fld.text = ""
        self.ids.bus_status_fld.reset()
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_update_bus"

    def goto_transaction(self):
        # self.show_transaction()
        if self.ids.scrn_mngr.current == "scrn_transaction_detail":
            self.ids.scrn_mngr.transition.direction = "right"
        else:
            self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_transaction"

    def goto_transaction_detail(self):
        self.ids.scrn_mngr.transition.direction = "left"
        self.ids.scrn_mngr.current = "scrn_transaction_detail"

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