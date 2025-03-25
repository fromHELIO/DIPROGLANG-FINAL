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
        """Closes the"""
        PinkTabInventory.stop()
        Window.close()

class AddRecord(Screen):
    """Screen for adding a new inventory item"""
    def addNewInventory(self):
        """adds new item to the database"""
        name = self.item_name.text
        quantity = self.quantity.text
        exp_date = self.exp_date.text
        price = self.price.text

        try: #checks if quantity is a number
            int(quantity)
        except ValueError:
            popup = Popup(
                title='Incorrect Quantity',
                content=Label(text='Please input a whole number.'),
                size_hint=(None, None), 
                size=(400, 200)
                )
            
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
                    cursor.execute(f"INSERT INTO inventory(name, quantity, exp_date, price) VALUES ('{name}', {quantity}, '{exp_date}', {price});")

                    #insert to changelog
                    cursor.execute(f"SELECT max(id) FROM inventory")
                    new_item = cursor.fetchall()[0][0]

                    cursor.execute(f"INSERT INTO change_log(employee_id, inventory_id, change_type) VALUES({getEmpId()}, {new_item}, 'ADDED INVENTORY')")

                    # sucess popup
                    popup = Popup(title='Success!', content=Label(text='The item has been added to the database.'), size_hint=(None, None), size=(400, 200))
                    popup.open()
    
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
                    
PinkTabInventory().run()
# close db
pinkTab.close
