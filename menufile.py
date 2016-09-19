import datetime
import json
import requests

class Menu:
    def __init__(self):
        self.date = datetime.date.today()
        url = "https://api.ruoka.xyz/" + str(self.date)
        r = requests.get(url)
        self.menustr = r.text
        self.menujson = r.json()

    def hae_menu_json(self):
        if self.date == datetime.date.today():
            return self.menujson
        else:
            self.date = datetime.date.today()
            url = "https://api.ruoka.xyz/" + str(self.date)
            r = requests.get(url)
            self.menustr = r.text
            self.menujson = r.json()
            return self.menujson
