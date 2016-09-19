import datetime
import json
import urllib
import urllib2

class Menu:
    def __init__(self):
        self.date = datetime.date.today()
        url = "https://api.ruoka.xyz/" + str(self.date)
        u = urllib2.urlopen(url)
        self.menustr = u.read()
        self.menujson = json.loads(self.menustr)

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
