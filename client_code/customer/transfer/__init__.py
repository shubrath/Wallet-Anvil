from ._anvil_designer import transferTemplate
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

class transfer(transferTemplate):
    def __init__(self, user=None, **properties):
        # Initialize self.user as a dictionary 
        self.init_components(**properties) 
        self.user = user
        self.timer_1.interval = 3
        self.timer_1.enabled = False
        # Set Form properties and Data Bindings.
        username = anvil.server.call('get_username', self.user['users_phone'])
        #self.label_1.text = f"Welcome to Green Gate Financial, {username}"
        currencies=anvil.server.call('get_user_currency',self.user['users_phone'])
        self.drop_down_2.items= [str(row['users_balance_currency_type']) for row in currencies]
        self.display()
        self.populate_balances()
    def populate_balances(self):
      try:
          # Retrieve balances for the current user
          user_phone = self.user['users_phone']
          user_balances = app_tables.wallet_users_balance.search(users_balance_phone=user_phone)
  
          # Print the retrieved data
          print("Retrieved balances:", user_balances)
  
          # Initialize index for card and components
          card_index = 1
          label_index = 1  # Start from label_1
          country_label_index = 50  # Start from label_50 for country
          image_index = 1
  
          # Iterate over user balances and update card components
          for balance in user_balances:
              currency_type = balance['users_balance_currency_type']
              balance_amount = round(balance['users_balance'], 2)  # Round to 2 decimal places
  
              # Lookup the currency icon, symbol, and country in the wallet_currency table
              currency_record = app_tables.wallet_admins_add_currency.get(admins_add_currency_code=currency_type)
              currency_icon = currency_record['admins_add_currency_icon'] if currency_record else None
              country = currency_record['admins_add_currency_country'] if currency_record else None
  
              # Get card and components for the current index
              card = getattr(self, f'card_{card_index}', None)
              label_curr_type = getattr(self, f'label_{label_index}', None)
              label_balance = getattr(self, f'label_{label_index + 1}', None)
              label_country = getattr(self, f'label_{country_label_index}', None)
              image_icon = getattr(self, f'image_icon_{image_index}', None)
  
              if card and label_curr_type and label_balance and image_icon and label_country:
                  # Update card components with balance data
                  label_curr_type.text = currency_type
                  label_balance.text = f"{balance_amount:.2f}"  # Format to 2 decimal places
                  label_balance.icon = f"fa:{currency_type.lower()}"
                  label_country.text = country
                  image_icon.source = currency_icon
  
                  # Align icon and text closer together if possible
                  # Adjust layout properties depending on your framework
                  # Example: label_balance.icon_style = "margin-right: 5px;"  # Adjust as needed
  
                  # Set card visibility to True
                  card.visible = True
  
                  # Increment indices for the next iteration
                  card_index += 1
                  label_index += 2
                  country_label_index += 1
                  image_index += 1
  
          # Set visibility of remaining cards to False if no data
          while card_index <= 12:
              card = getattr(self, f'card_{card_index}', None)
              if card:
                  card.visible = False
              card_index += 1
  
      except Exception as e:
          # Print any exception that occurs during the process
          print("Error occurred during population of balances:", e)
     

    def drop_down_1_change(self, **event_args):
      self.display()

    def display(self, **event_args):
      acc = self.drop_down_2.selected_value

    def button_1_click(self, **event_args):
      current_datetime = datetime.now()
      receiver_phone_number = float(self.text_box_2.text)
      transfer_amount = float(self.text_box_3.text)
      cur = self.drop_down_2.selected_value
      depositor_phone_number = self.user['users_phone']
      
      
      
      # Use the entered phone number to identify the receiver's account
      receiver_balance = app_tables.wallet_users_balance.get(users_balance_phone=receiver_phone_number, users_balance_currency_type=cur)
      depositor_balance = app_tables.wallet_users_balance.get(users_balance_phone=depositor_phone_number, users_balance_currency_type=cur)
      if trasfer_amount >0:
        if depositor_balance:
            depositor = app_tables.wallet_users.get(users_phone=depositor_phone_number)
            
            users_daily_limit = depositor['users_daily_limit']
            users_user_limit = depositor['users_user_limit']
            
            if transfer_amount > users_daily_limit:
                anvil.alert("Daily limit exceeded.")
            elif transfer_amount > users_user_limit:
                anvil.alert("Monthly limit exceeded.")
            else:
                money_value = transfer_amount if transfer_amount else 0.0
                if depositor_balance['users_balance'] >= money_value:
                    if receiver_balance:
                        depositor_balance['users_balance'] -= money_value
                        receiver_balance['users_balance'] += money_value
                    else:
                        receiver = app_tables.wallet_users.get(users_phone=receiver_phone_number)
                        if receiver:
                            depositor_balance['users_balance'] -= money_value
                            app_tables.wallet_users_balance.add_row(
                                users_balance_currency_type=cur,
                                users_balance=money_value,
                                users_balance_phone=receiver_phone_number
                            )
                        else:
                            anvil.alert("User does not exist")
                            return
                    
                    # new_transaction = app_tables.wallet_users_transaction.add_row(
                    #     users_transaction_phone=depositor_phone_number,
                    #     users_transaction_fund=money_value,
                    #     users_transaction_currency=cur,
                    #     users_transaction_date=current_datetime,
                    #     users_transaction_type="Debit",
                    #     users_transaction_status="transferred-to",
                    #     users_transaction_receiver_phone=receiver_phone_number
                    # )
                    # new_transaction = app_tables.wallet_users_transaction.add_row(
                    #     users_transaction_phone=receiver_phone_number,
                    #     users_transaction_fund=money_value,
                    #     users_transaction_currency=cur,
                    #     users_transaction_date=current_datetime,
                    #     users_transaction_type="Credit",
                    #     users_transaction_status="received-from",
                    #     users_transaction_receiver_phone=depositor_phone_number
                    # )
  
                    new_transaction = app_tables.wallet_users_transaction.add_row(
                        users_transaction_phone=depositor_phone_number,
                        users_transaction_fund=money_value,
                        users_transaction_currency=cur,
                        users_transaction_date=current_datetime,
                        users_transaction_type="Debit",
                        users_transaction_receiver_type="Credit",
                        users_transaction_status="transferred-to",
                        users_transaction_receiver_phone=receiver_phone_number,
                    )
          
                    users_text=f"You have received **{self.drop_down_2.selected_value} {self.text_box_3.text}**from {self.user['users_username']}"
                    anvil.server.call('notify',users_text,current_datetime,self.text_box_2.text,self.user['users_phone'])
                  
                    # Update the limits after successful transaction
                    depositor['users_daily_limit'] -= money_value
                    depositor['users_user_limit'] -= money_value
    
                    #self.label_4.text = "Money transferred successfully to the account"
                    alert("Money transferred successfully to the account")
                    self.populate_balances()
                else:
                    anvil.alert("Insufficient balance. Please add funds")
        else:
            #self.label_4.text = "Error: No matching accounts found for the user or invalid account number"
            alert("Error: No matching accounts found for the user or invalid account number")
    
        open_form('customer.transfer', user=self.user)
      else:
        alert(f"payment amount must be atleast 1 {cur}")
    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.wallet",user=self.user)

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.deposit",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transactions",user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transfer",user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.service",user=self.user)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer",user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

    def link_10_click(self, **event_args):
      open_form('customer.deposit',user=self.user)

    def link_5_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.withdraw',user=self.user)

    def link_6_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.auto_topup',user=self.user)

    def text_box_2_pressed_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      pass

    def link_8_copy_2_click(self, **event_args):
      open_form("customer.settings",user =self.user)

    def link_help_click(self, **event_args):
      open_form("help",user = self.user)

  

    def text_box_3_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.timer_1.enabled = True
        user_input = self.text_box_3.text
        processed_value = self.process_input(user_input)
        self.text_box_3.text = processed_value
  
    
    def process_input(self, user_input):
      try:
        if user_input == None: # Convert the input to a float
          formatted_value = ''
        else:
          value = float(user_input)
          # Check if the value is an integer or a float with significant digits
          if value.is_integer():
              # If it's an integer, format without decimals
              formatted_value = '{:.0f}'.format(value)
          else:
              # If it's a float, format with significant digits
              formatted_value = '{:.15g}'.format(value)
          
        
        return formatted_value
      except ValueError:
        return user_input 
  
    def timer_1_tick(self, **event_args):
      """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
      pass




