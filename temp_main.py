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

# main

Window.clearcolor = "#fccce7"

class PinkTabInventory(App):
    def build(self):
        Builder.load_file('PinkTabInventory.kv')

class Navigator(ScreenManager):
    pass

class TestPage(Screen):
    pass

class LogInPage(BoxLayout, Screen):

    emp_id = ObjectProperty(None)
    password = ObjectProperty(None)

    def validateUser(self):
        emp_id = self.emp_id.text
        password = self.password.text
        cursor.execute("SELECT id FROM employee")
        users = [x for i in cursor.fetchall() for x in i]
        
        
        if emp_id in users:
            cursor.execute(f"SELECT emp_pass FROM employee WHERE id={emp_id}")
            user_pass = ''.join([str(x) for i in cursor.fetchall() for x in i])
            if password == user_pass:
                self.manager.transition.direction = "left"
                self.manager.current = "home"
        
    def getEmpId(self):
        return self.emp_id.text


class HomePage(Screen):
    def endApp(self, *args):
        PinkTabInventory.stop()
        Window.close()

class AddRecord(Screen):
    def addNewInventory(self):
        name = self.item_name.text
        quantity = self.quantity.text
        exp_date = self.exp_date.text
        price = self.price.text

        try:
            int(quantity)
        except ValueError:
            popup = Popup(title='Test popup', content=Label(text='Please input a whole number.'), size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            try:
                float(price)
            except ValueError:
                popup = Popup(title='Test popup', content=Label(text='Please input an whole or decimal number.'), size_hint=(None, None), size=(400, 200))
                popup.open()
            else:
                try:
                    self.dateError(exp_date)
                except:
                    popup = Popup(title='Test popup', content=Label(text='Please input a valid date.'), size_hint=(None, None), size=(400, 200))
                    popup.open()
                else:
                    cursor.execute(f"INSERT INTO inventory(name, quantity, exp_date, price) VALUES ('{name}', {quantity}, '{exp_date}', {price});")

                    popup = Popup(title='Success!', content=Label(text='The item has been added to the database.'), size_hint=(None, None), size=(400, 200))
                    popup.open()
    
    def dateError(self, date):
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