import kivy
import pandas as pd
import xlrd
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
data = pd.read_excel(r'C:\Users\Shawn\Desktop\NFL Stats.xlsx', engine='openpyxl')
df = pd.DataFrame(data)
data2 = pd.read_excel(r'C:\Users\Shawn\Desktop\NBA Stats.xlsx', engine='openpyxl')
df2 = pd.DataFrame(data2)


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class SecondWindow(Screen):
    current= ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            AccountWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):

    def logOut(self):
        sm.current = "login"

    def sportBtn(self):
        sm.current = "sport"

    def accountBtn(self):
        sm.current = "account"


class AccountWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created
    def mainBtn(self):
        sm.current = "main"

class NFLWindow(Screen):
    current = ""
    def mainBtn(self):
        sm.current = "main"
    def nextBtn(self):
        sm.current = "NFC"
    def teamBtn(self):
        sm.current = "NFL2"


class NFCWindow(Screen):
    current = ""
    def mainBtn(self):
        sm.current = "NFL"
    def nextBtn(self):
        sm.current = "NFL"

    def teamBtn(self):
        sm.current = "NFL2"


class NFLWindow2(Screen):
    current = ""
    def mainBtn(self):
        sm.current = "NFL"
    def nextBtn(self):
        sm.current = "NFC2"


class NFCWindow2(Screen):
    current = ""
    def mainBtn(self):
        sm.current = "NFL2"
    def nextBtn(self):
        sm.current = "NFL2"



class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"), SecondWindow(name="sport"), AccountWindow(name="account"), NFLWindow(name="NFL"),
           NFCWindow(name="NFC"), NFLWindow2(name="NFL2"), NFCWindow2(name="NFC2")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"




class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()