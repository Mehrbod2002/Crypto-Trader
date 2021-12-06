import multiprocessing
import threading
from kucoin import Kucoin,JSON
from multiprocessing import Process
from datetime import datetime
import time,asyncio
reader = JSON("data")
class mains:
    def __init__(self):
        order = reader.get("order")
        if len(order) != 0:
            for i in order:
                self.kuco = Kucoin()
                timestamp = f'{i["day"]}/{i["month"]}/{i["year"][-2:]} {i["clock"]}'
                timestamp = datetime.strptime(timestamp,"%d/%m/%y %H:%M:%S.%f").timetuple()
                timestamp = time.mktime(timestamp)
                Process(target=self.run_sync,args=(timestamp,i["wallet_per"],i["coin_name"],i["sell_per"],),daemon=True).start()
    def call(self,timestamp,amount,coin,percentage):
        self.kuco = Kucoin()
        p = Process(target=self.run_sync,args=(timestamp,amount,coin,percentage),daemon=True)
        p.name = str(coin)
        p.start()
    def kill(self,coin):
        for i in multiprocessing.active_children():
            if i.name == str(coin):
                i.kill()
    def run_sync(self,timestamp,amount,coin,percentage):
        asyncio.run(self.kuco.check_time(timestamp,amount,coin,percentage))
    def thread_list(self):
        return threading.enumerate()
        