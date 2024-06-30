from ._anvil_designer import create_adminTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import re

class create_admin(create_adminTemplate):
  def __init__(self, user=None, **properties):
    self.init_components(**properties)
    self.user = user
    self.label_12.text = datetime.now().strftime('%d %b %Y')
    self.which_admin_created_account = user['users_username']
    print(self.which_admin_created_account)

  def button_1_click(self, **event_args): 
        date_of_admins_account_created = datetime.now().date()
        existing_admin = anvil.server.call('get_admin_by_phone', str(self.text_box_4.text).strip())

        if existing_admin:
            alert('You have already signed up with this phone number.')
        else:
          count=0
          phone_number = str(self.text_box_4.text).strip()
          if self.validate_phone_number(phone_number):
              count=count+1
              self.label_13.text ="Phone number is correct"
          else:
              self.label_13.text ="Please check the entered phone number"
              self.text_box_4.text=''
              self.text_box_4.focus()
          if self.text_box_5.text != '':
            if self.text_box_5.text != self.text_box_6.text:
              self.label_9.text = "Passwords doesn't match"
              self.text_box_5.text =''
              self.text_box_5.focus()
              self.text_box_6.text =''
              self.text_box_6.focus()
            elif self.text_box_5.text == self.text_box_6.text:
              self.label_9.text = "Password matches"  
        
              if count==1:
                
                anvil.server.call(
                  'add_admins_info',  
                  self.text_box_1.text, 
                  self.text_box_2.text,
                  self.text_box_4.text,
                  self.text_box_5.text,
                )
                print('Admin credentials stored for login')
                app_tables.wallet_admins_create_admin_account.add_row(
                    admins_username=self.text_box_1.text,
                    admins_email=self.text_box_2.text,
                    admins_phone=self.text_box_4.text,
                    admins_password=self.text_box_5.text,
                    admins_date_of_birth=self.date_picker_1.date,
                    admins_gender=self.drop_down_1.selected_value,
                    which_admin_created_account=f'Admin - {self.which_admin_created_account}',
                    date_of_admins_account_created=date_of_admins_account_created,
                    #usertype='admin',
                    admins_last_login=datetime.now()
                  )
                alert (self.text_box_1.text + ' added')
                open_form('admin')

  def validate_button_click(self, **event_args):
    phone_number = str(self.text_box_6.text).strip()  

  def validate_phone_number(self, phone_number):
      pattern = r'^[6-9]\d{9}$'
      if re.match(pattern, str(phone_number)):
          return True  
      else:
          return False  

  def link_8_copy_click(self, **event_args):
    open_form('admin', user=self.user)

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin',user=self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.report_analysis',user=self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.account_management',user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.transaction_monitoring',user=self.user)

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.add_currency',user=self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.audit_trail',user=self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_5_copy_2_click(self, **event_args):
   open_form("admin.admin_add_user",user = self.user)

  def link_5_copy_3_click(self, **event_args):
    open_form("admin.create_admin",user = self.user)

  def link_5_copy_4_click(self, **event_args):
    open_form("admin.user_support",user = self.user)

  def link_5_copy_5_click(self, **event_args):
    open_form("admin.add_bank_account",user = self.user)
