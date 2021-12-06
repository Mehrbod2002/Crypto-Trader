from os import read
from defs import JSON
import requests,enum
reader = JSON("data")
class status(enum.Enum):
    empty_token = "توکن بایننس خالی است"
    new_order = "درخواست جدید"
    balance_not_enough = "موجودی تتر شما نا کافی می باشد"
class Noti:
    def __init__(self):
        self.chat_id = ""
        try:
            if reader.get("telegram") != "":
                self.token = reader.get("telegram")
        except:
            pass
    def send(self,text):
        if self.token != "":
            bot = "https://api.telegram.org/bot"+self.token+"/sendMessage?chat_id="+self.chat_id+"&text="+text
            try:
                requests.get(bot,timeout=2)
            except:
                pass