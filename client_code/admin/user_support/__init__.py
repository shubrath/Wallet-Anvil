from ._anvil_designer import user_supportTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class user_support(user_supportTemplate):
  def __init__(self,user=None, **properties):
    # Set Form properties and Data Bindings.
    self.user=user
    self.init_components(**properties)
    if user is not None:
      self.repeating_panel_1.items = app_tables.wallet_users_service.search()

    # Any code you write here will run before the form opens.
    #email = anvil.server.call('email')

    
    #self.text_box_1.text = {user['users_email']}

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin',user=self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.report_analysis', user= self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.transaction_monitoring',user=self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.audit_trail',user=self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.add_currency', user = self.user)

  def link_4_click(self, **event_args):
    open_form('admin.admin_add_user',user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.account_management',user=self.user)

  def link_8_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin',user=self.user)

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Login')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def link6_copy_click(self, **event_args):
    open_form("admin.transaction_monitoring",user = self.user)

  def link6_copy_2_click(self, **event_args):
    open_form("admin.create_admin",user = self.user)

  def link6_copy_3_click(self, **event_args):
    open_form("admin.user_support",user = self.user)

  def link6_copy_4_click(self, **event_args):
    open_form("admin.add_bank_account",user = self.user)
    
