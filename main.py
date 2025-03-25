#fix window size
from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '550')
Config.set('graphics', 'height', '700')

#kivy imports
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

#sql server connection

import mysql.connector

pinkTab = mysql.connector.connect(host="localhost", user="root", password="", database="pink_tab", autocommit=True)

cursor = pinkTab.cursor()

# main file

Window.clearcolor = "#fccce7"

class PinkTabInventory(App):
    """Main app builder"""
    def build(self):
        Builder.load_file('PinkTabInventory.kv')

class Navigator(ScreenManager):
    """For switching screens"""
    pass

class LogInPage(BoxLayout, Screen):
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

# get current user's id

def getEmpId():
        """Get Employee Information of current session. 1 to retrieve ID, 2 for first name."""
        cursor.execute("SELECT employee_id FROM access_log WHERE id = (SELECT MAX(id) FROM access_log)")
        results = cursor.fetchall()[0][0]
        return results

# main screens

class HomePage(Screen):
    """Home naviagtion page"""
    def endApp(self, *args):
        """Closes the app"""
        PinkTabInventory.stop()
        Window.close()

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
                        popup = Popup(title='Invalid Date', content=Label(text='Please use the YYYY-MM-DD format.'), size_hint=(None, None), size=(400, 200))
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

class EditRecord(Screen):
    """Screen for editing selected inventory"""

    # itemId = (self.itemId.text).upper()
    # name = self.item_name.text
    # quantity = self.quantity.text
    # exp_date = self.exp_date.text
    # price = self.price.text

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
                popup = Popup(title='Invalid Date', content=Label(text='Please use the YYYY-MM-DD format.'), size_hint=(None, None), size=(400, 200))
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
                
        
PinkTabInventory().run()
# close db
pinkTab.close
