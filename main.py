#fix window size
from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '550')
Config.set('graphics', 'height', '700')

#kivy imports
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable

from kivy.metrics import dp

# general imports

import mysql.connector
import datetime as dt
from sys import exit

#sql server connection
pinkTab = mysql.connector.connect(host="localhost", user="root", password="", database="pink_tab", autocommit=True)
cursor = pinkTab.cursor()

# main process

# general functions
def getEmpId():
    """Get Employee Information of current session. 1 to retrieve ID, 2 for first name."""
    cursor.execute("SELECT employee_id FROM access_log WHERE id = (SELECT MAX(id) FROM access_log)")
    results = cursor.fetchall()[0][0]
    return results

def getInventory():
    """Get the data of the inventory table"""
    cursor.execute("SELECT * FROM inventory")
    results = cursor.fetchall()
    return results

# App
class PinkTabInventory(MDApp):
    """Main app builder"""
    def build(self):
        Builder.load_file('PinkTabInventory.kv')
        self.theme_cls.primary_palette = "Teal"

class Navigator(ScreenManager):
    """For switching screens"""
    pass

# main screens

class LogInPage(Screen):
    """User log in screen"""
    emp_id = ObjectProperty(None)
    password = ObjectProperty(None)

    def validateUser(self):
        """Checks if the user is a valid employee."""
        emp_id = self.emp_id.text
        password = self.password.text
        cursor.execute("SELECT id FROM employee")
        users = [x for i in cursor.fetchall() for x in i]
        
        if emp_id in users:
            cursor.execute(f"SELECT emp_pass FROM employee WHERE id={emp_id}")
            user_pass = ''.join([str(x) for i in cursor.fetchall() for x in i])

            if password == user_pass:
                #add to access log
                cursor.execute(f"INSERT INTO access_log(employee_id) VALUES({emp_id})")
                #move to home screen
                self.manager.transition.direction = "left"
                self.manager.current = "home"

class HomePage(Screen):
    """Home naviagtion page"""
    def endApp(self):
        """Closes the app"""
        exit(0)

class AddRecord(Screen):
    """Screen for adding a new inventory record"""
    def addNewInventory(self):
        """adds new item to the database"""
        itemId = (self.itemId.text).upper()
        name = self.item_name.text
        quantity = self.quantity.text
        exp_date = self.exp_date.text
        price = self.price.text

        try:
            self.idError(itemId)
        except:
            popup = Popup(title='Invalid Item ID', content=Label(text='ID must be exactly five letters.'), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            try: #checks if quantity is a number
                int(quantity)
            except ValueError:
                popup = Popup(title='Incorrect Quantity', content=Label(text='Please input a whole number.'), size_hint=(None, None), size=(400, 200))
                popup.open()
            else:
                try: #checks if price is a float
                    float(price)
                except ValueError:
                    popup = Popup(title='Invalid Price', content=Label(text='Please input an whole or decimal number.'), size_hint=(None, None), size=(400, 200))
                    popup.open()
                else:
                    try: #checks if date is valid
                        self.dateError(exp_date)
                    except:
                        popup = Popup(title='Invalid Date', content=Label(text='Please enter a valid date (YYYY-MM-DD).'), size_hint=(None, None), size=(400, 200))
                        popup.open()
                    else:
                        #insert into inventory
                        cursor.execute(f"INSERT INTO inventory(id, name, quantity, exp_date, price) VALUES ('{itemId.upper()}', '{name}', {quantity}, '{exp_date}', {price});")

                        #insert to changelog
                        cursor.execute(f"SELECT max(id) FROM inventory")
                        new_item = cursor.fetchall()[0][0]

                        cursor.execute(f"INSERT INTO change_log(employee_id, change_info) VALUES('{getEmpId()}', 'ADDED INVENTORY {new_item} - {name}')")

                        # sucess popup
                        popup = Popup(title='Success!', content=Label(text='The item has been added to the database.'), size_hint=(None, None), size=(400, 200))
                        popup.open()
    
    def idError(self, item_id):
        if len(item_id) != 5:
            raise Exception()
        if not item_id.isalpha():
            raise Exception()
    
    def dateError(self, date):
        """Tests if date string is valid"""
        testDate = date.split('-')
        if len(testDate) != 3:
            raise Exception()
        else:
            if len(testDate[0]) != 4:
                raise Exception()
            
            if not(int(testDate[1]) in range(1, 13)):
                raise Exception()
            
            if not(int(testDate[2]) in range(1, 32)):
                raise Exception()
            elif int(testDate[2]) == 31 and int(testDate[1]) in [2, 4, 6, 9, 11]:
                raise Exception()

class EditRecord(Screen):
    """Screen for editing selected inventory"""

    def editName(self):
        """Edit selected inventory's name"""
        itemId = (self.itemId.text).upper()
        name = self.item_name.text

        try:
            self.validateItemID(itemId)
        except:
            popup = Popup(title='Invalid Item ID', content=Label(text='Please input a valid item ID.'), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            #update record
            cursor.execute(f"UPDATE inventory SET name = '{name}' WHERE id = '{itemId}'")

            #add to change log
            cursor.execute(f"SELECT name FROM inventory where id = '{itemId}'")
            editedName = cursor.fetchall()[0][0]
            
            cursor.execute(f"INSERT INTO change_log(employee_id, change_info) VALUES('{getEmpId()}', 'EDITED INVENTORY {itemId} NAME TO {editedName}')")

            #success popup
            popup = Popup(title='Success!', content=Label(text="The item's name has been updated."), size_hint=(None, None), size=(400, 200))
            popup.open()

    def editQuantity(self):
            """Edit selected inventory's quantity"""
            itemId = (self.itemId.text).upper()
            quantity = self.quantity.text

            try:
                self.validateItemID(itemId)
            except:
                popup = Popup(title='Invalid Item ID', content=Label(text='Please input a valid item ID.'), size_hint=(None, None), size=(400, 200))
                popup.open()
            else:
                try: #checks if quantity is a number
                    int(quantity)
                except ValueError:
                    popup = Popup(title='Incorrect Quantity', content=Label(text='Please input a whole number.'), size_hint=(None, None), size=(400, 200))
                    popup.open()
                else:
                    #update record
                    cursor.execute(f"UPDATE inventory SET quantity = {quantity} WHERE id = '{itemId}'")

                    #add to change log
                    cursor.execute(f"SELECT quantity FROM inventory where id = '{itemId}'")
                    editedQuant = cursor.fetchall()[0][0]
                    
                    cursor.execute(f"INSERT INTO change_log(employee_id, change_info) VALUES('{getEmpId()}', 'EDITED INVENTORY {itemId} QUANTITY TO {editedQuant}')")

                    #success popup
                    popup = Popup(title='Success!', content=Label(text="The item's quantity has been updated."), size_hint=(None, None), size=(400, 200))
                    popup.open()
    
    def editExpDate(self):
        """Edit selected inventory's expiration date"""
        itemId = (self.itemId.text).upper()
        exp_date = self.exp_date.text

        try:
            self.validateItemID(itemId)
        except:
            popup = Popup(title='Invalid Item ID', content=Label(text='Please input a valid item ID.'), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            try: #checks if date is valid
                self.dateError(exp_date)
            except:
                popup = Popup(title='Invalid Date', content=Label(text='Please enter a valid date (YYYY-MM-DD).'), size_hint=(None, None), size=(400, 200))
                popup.open()
            else:
                #update record
                cursor.execute(f"UPDATE inventory SET exp_date = '{exp_date}' WHERE id = '{itemId}'")

                #add to change log
                cursor.execute(f"SELECT exp_date FROM inventory where id = '{itemId}'")
                editedExpDate = cursor.fetchall()[0][0]
                
                cursor.execute(f"INSERT INTO change_log(employee_id, change_info) VALUES('{getEmpId()}', 'EDITED INVENTORY {itemId} EXPIRATION DATE TO {editedExpDate}')")

                #success popup
                popup = Popup(title='Success!', content=Label(text="The item's expiration date has been updated."), size_hint=(None, None), size=(400, 200))
                popup.open()

    def editPrice(self):
        """Edit selected inventory's price"""
        itemId = (self.itemId.text).upper()
        price = self.price.text

        try:
            self.validateItemID(itemId)
        except:
            popup = Popup(title='Invalid Item ID', content=Label(text='Please input a valid item ID.'), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            try: #checks if price is a float
                float(price)
            except ValueError:
                popup = Popup(title='Invalid Price', content=Label(text='Please input an whole or decimal number.'), size_hint=(None, None), size=(400, 200))
                popup.open()
            else:
                #update record
                cursor.execute(f"UPDATE inventory SET price = {price} WHERE id = '{itemId}'")

                #add to change log
                cursor.execute(f"SELECT price FROM inventory where id = '{itemId}'")
                editedPrice = cursor.fetchall()[0][0]
                
                cursor.execute(f"INSERT INTO change_log(employee_id, change_info) VALUES('{getEmpId()}', 'EDITED INVENTORY {itemId} PRICE TO {editedPrice}')")

                #success popup
                popup = Popup(title='Success!', content=Label(text="The item's price has been updated."), size_hint=(None, None), size=(400, 200))
                popup.open()

    def validateItemID(self, item_id):
        """Validate if Item ID exist"""
        cursor.execute(f"SELECT * from inventory where id = '{item_id}'")
        result = cursor.fetchall()
        print(result)
        if len(result) == 0:
            raise Exception()

    def dateError(self, date):
        """Tests if date string is valid"""
        testDate = date.split('-')
        if len(testDate) != 3:
            raise Exception()
        else:
            if len(testDate[0]) != 4:
                raise Exception()
            
            if not(int(testDate[1]) in range(1, 13)):
                raise Exception()
            
            if not(int(testDate[2]) in range(1, 32)):
                raise Exception()
            
            elif int(testDate[2]) == 31 and int(testDate[1]) in [2, 4, 6, 9, 11]:
                raise Exception()

class DeleteRecord(Screen):
    """Screen for deleting inventory records"""
    def deleteInventory(self):
        """Delete selected inventory item"""
        itemId = (self.itemId.text).upper()

        try:
            self.validateItemID(itemId)
        except:
            popup = Popup(title='Invalid Item ID', content=Label(text='Please input a valid item ID.'), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            #insert to changelog
            cursor.execute(f"SELECT name FROM inventory where id = '{itemId}'")
            deletedName = cursor.fetchall()[0][0]
            
            cursor.execute(f"INSERT INTO change_log(employee_id, change_info) VALUES('{getEmpId()}', 'DELETED INVENTORY {itemId} - {deletedName}')")

            #insert into inventory
            cursor.execute(f"DELETE FROM inventory WHERE id = '{itemId}';")

            popup = Popup(title='Success!', content=Label(text='The item has been deleted from the database.'), size_hint=(None, None), size=(400, 200))
            popup.open()

    def validateItemID(self, item_id):
        cursor.execute(f"SELECT * from inventory where id = '{item_id}'")
        result = cursor.fetchall()
        print(result)
        if len(result) == 0:
            raise Exception()
            
class ShowReport(Screen):
    """Screen for showing report of inventory"""
    def __init__(self, **kw):
        super().__init__(**kw)
        # get current date
        results = getInventory()
        self.inventory = Inventory()
    
    def display(self):
        """Display widgets to screen"""
        updatedDatabase = self.inventory.formatData()
        print(updatedDatabase)

        self.inventory.update_row_data(instance_data_table=self.inventory, data=updatedDatabase)

        #calculate total quantity
        totalQuantity = 0
        quantities = [i[2] for i in updatedDatabase]
        for i in quantities:
            totalQuantity += i

        backButton = RoundedButton(
            text = "Back",
            color = "#fccce7",
            size_hint = (None, None),
            size = (170, 50),
            pos_hint = {"center_x": .5, "center_y": .5},
            font_size = 30,
            on_press = lambda x:self.goHome()
        )
        
        self.invHolder.add_widget(CustomLabel(text=f"Total Inventory: {totalQuantity}", font_size=30))
        self.invHolder.add_widget(self.inventory)
        self.invHolder.add_widget(backButton)
    
    def goHome(self):
        """Return to home screen"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
        self.invHolder.clear_widgets()

#assets

class Inventory(MDDataTable):
    """Widget for showing database's inventoyr table"""
    today = dt.date.today()

    def checkExpiry(current, item_expd):
        """Check if item is expired"""
        if current>=item_expd:
            status = "Expired"
        elif (item_expd-current).days < 60:
            status = "Near expiry"
        else:
            status = "Safe"
        
        return status

    def checkRestock(item_qnt):
        """Check if item needs to be restocked"""
        if item_qnt < 100:
            neededStock = 100 - item_qnt
            status = f"Restock {neededStock}"
        else:
            status = "Stocked"
        
        return status

    def formatData(self):
        """For reformating data when updating the table"""
        newTableData = []
        invTable = getInventory()
        for i in invTable:
            if i[2] < 100:
                neededStock = 100 - i[2]
                stockStatus = f"Restock {neededStock}"
            else:
                stockStatus = "Stocked"

            current = dt.date.today()

            if current>=i[3]:
                expStatus = "Expired"
            elif (i[3]-current).days < 60:
                expStatus = "Near expiry"
            else:
                expStatus = "Safe"


            newRecord=(i[0], i[1], i[2], stockStatus, i[3], expStatus, i[4])
            newTableData.append(newRecord)
        
        return newTableData

    
    # design settings
    size_hint = (.90, .55)
    pos_hint = {"center_y": 0.5, "center_x": 0.5}
    use_pagination = True
    rows_num = 5

    # table columns and data
    column_data = [
        ("Item ID", dp(20)),
        ("Item Name", dp(50)),
        ("Quantity", dp(20)),
        ("Restock Status", dp(30)),
        ("Expiration Date", dp(30)),
        ("Expiry Status", dp(30)),
        ("Price", dp(20)),
    ]

    invData = getInventory()
    row_data = []
    for i in invData:
        stockStatus = checkRestock(i[2])
        expStatus = checkExpiry(today, i[3])
        newRecord=(i[0], i[1], i[2], stockStatus, i[3], expStatus, i[4])
        row_data.append(newRecord)

class RoundedButton(Button):
    """For custom rounded buttons"""
    pass # design settings in .kv file

class CustomLabel(Label):
    """For custom labels"""
    pass # design settings in .kv file

PinkTabInventory().run()

# close db
pinkTab.close()
