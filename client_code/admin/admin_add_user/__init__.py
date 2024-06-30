from ._anvil_designer import admin_add_userTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class admin_add_user(admin_add_userTemplate):
    def __init__(self, user=None, **properties):
        self.user = user
        self.init_components(**properties)
      
    def text_box_4_change(self, **event_args):
        # Convert the text in text_box_8 to uppercase as user types
        self.text_box_8.text = self.text_box_8.text.upper()
    def button_1_click(self, **event_args): 
        count = 0
        if self.text_box_3.text != '':
            if self.text_box_3.text != self.text_box_7.text:
                self.label_17.text = "Passwords don't match"
                self.text_box_3.text = ''
                self.text_box_3.focus()
                self.text_box_7.text = ''
                self.text_box_7.focus()
            else:
                self.label_17.text = "Password matches"
                count += 1

            if self.is_pan_card_detail(self.text_box_4.text):
                self.label_14.text = "Pan card is valid"
                count += 1
            else:
                self.label_14.text = "Please check the entered pan card details"
                self.text_box_4.text = ''
                self.text_box_4.focus()

            if self.validate_phone_number(self.text_box_6.text):
                self.label_15.text = "Phone number is correct"
                count += 1
            else:
                self.label_15.text = "Please check the entered phone number"
                self.text_box_6.text = ''
                self.text_box_6.focus()

            aadhar = str(self.text_box_8.text)
            if len(aadhar) == 12 and aadhar.isdigit():
                self.label_16.text = "Aadhar details correct"
                count += 1
            else:
                self.label_16.text = "Please check the entered Aadhar details"
                self.text_box_8.text = ''
                self.text_box_8.focus()

        if count == 4:
            try:
                anvil.server.call(
                    'add_info',
                    self.text_box_1.text,
                    self.text_box_2.text,
                    self.text_box_5.text,
                    self.text_box_6.text,
                    self.text_box_8.text,
                    self.text_box_4.text,
                    self.text_box_3.text
                )
                alert(self.text_box_2.text + ' added')
                open_form('login')
            except Exception as e:
                alert(f"Error adding user: {str(e)}")

    def text_box_4_change(self, **event_args):
        self.text_box_4.text = self.text_box_4.text.upper()

    def is_pan_card_detail(self, text):
        return len(text) == 10 and text[:5].isalpha() and text[5:9].isdigit() and text[9].isalpha()

    # def validate_phone_number(self, phone_number):
    #     return re.match(r'^[6-9]\d{9}$', phone_number) is not None

    def validate_phone_number(self, phone_number):
        if phone_number is None:
            phone_number = ""
        return re.match(r'^[6-9]\d{9}$', str(phone_number)) is not None

    def link_1_click(self, **event_args):
        open_form('admin.report_analysis')

    def link_8_click(self, **event_args):
        open_form('admin', user=self.user)

    def link_8_copy_click(self, **event_args):
        open_form('admin', user=self.user)

    def link_10_copy_click(self, **event_args):
        open_form('admin.user_support', user=self.user)

    def button_8_click(self, **event_args):
        open_form('Login')

    def button_3_click(self, **event_args):
        open_form('admin.show_users', user=self.user)

    def link_2_click(self, **event_args):
        open_form('admin.account_management', user=self.user)

    def link_7_click(self, **event_args):
        open_form('admin.transaction_monitoring', user=self.user)

    def link_6_click(self, **event_args):
        open_form('admin.create_admin', user=self.user)

    def link_5_click(self, **event_args):
        open_form('admin.audit_trail', user=self.user)

    def link_4_click(self, **event_args):
        serves_data = app_tables.wallet_users_service.search()
        user_support_form = open_form('admin.user_support', serves_data=serves_data)

    def link_3_click(self, **event_args):
        #show_users_form = open_form('admin.show_users', user=self.user)
        open_form('admin.transaction_monitoring',user=self.user)

    def link_10_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.add_currency',user=self.user)

    def link_6_copy_4_click(self, **event_args):
      open_form("admin.add_bank_account",user=self.user)

    def link_6_copy_2_click(self, **event_args):
      open_form("admin.admin_add_user",user=self.user)
