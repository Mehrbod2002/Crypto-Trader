import tkinter as tk
from tkinter import messagebox
from tkinter.constants import HORIZONTAL, LEFT, VERTICAL, Y
from tkinter.ttk import *
from types import coroutine
from tkcalendar import DateEntry
from defs import JSON
from main import mains
import os,datetime,time
delete_image = str(os.getcwd())+"/delete.png"
root = tk.Tk()
root.geometry('1029x1500')
root.title("coin")
recent = ""
reader = JSON("data")
caller = mains()
def fill_file():
    telegram.insert(0,reader.get("telegram"))
    kucoin_api.insert(0,reader.get("kucoin_api"))
    kucoin_secret.insert(0,reader.get("kucoin_secret"))
    kucoin_pass.insert(0,reader.get("kucoin_pass"))
def percenrage_validate(new_value):
    if new_value == "":
        return True
    try:
        return 0<float(new_value)<=100
    except:
        return False
def percenrage_validate_sell(new_value):
    if new_value == "":
        return True
    try:
        return 0<float(new_value)
    except:
        return False
def setting_save():
    telegram_token = telegram.get()
    kucoin_api1 = kucoin_api.get()
    kucoin_pass1 = kucoin_pass.get()
    kucoin_secret1 = kucoin_secret.get()
    answer = messagebox.askquestion("Setting Changes","Are you sure ?")
    if answer == "yes":
        reader.set("telegram",telegram_token)
        reader.set("kucoin_api",kucoin_api1)
        reader.set("kucoin_secret",kucoin_secret1)
        reader.set("kucoin_pass",kucoin_pass1)
        messagebox.showinfo("Setting Changes","Saved")
    else:
        telegram.delete(0,'end')
        kucoin_api.delete(0,'end')
        kucoin_secret.delete(0,'end')
        kucoin_pass.delete(0,'end')
        telegram.insert(0,reader.get("telegram"))
        kucoin_api.insert(0,reader.get("kucoin_api"))
        kucoin_secret.insert(0,reader.get("kucoin_secret"))
        kucoin_pass.insert(0,reader.get("kucoin_pass"))
def take_order():
    global recents
    value = [wallet_per.get(),coin_name.get(),sell_per.get(),entry_clock.get()]
    for i in value:
        if str(i) == "":
            messagebox.showerror("Error","FIll all fileds")
            return 
    if (entry_clock.get()).count(":") != 2:
        messagebox.showerror("Error","Invalid Clock")
        return
    if ("-" in coin_name.get()) == False:
        messagebox.showerror("Error","Invalid Coin")
        return
    try:
        val = entry_clock.get().split(":")
        for i in val:
            float(i)
    except:
        messagebox.showerror("Error","Invalid Clock")
        return
    answer = messagebox.askquestion("Setting Changes","Are you sure ?")
    if answer == "yes":
        day = cal.get_date().day
        year = cal.get_date().year
        month = cal.get_date().month
        timestamp = f'{day}/{month}/{year[-2:]} {entry_clock.get()}'
        timestamp = datetime.datetime.strptime(timestamp,"%d/%m/%y %H:%M:%S.%f").timetuple()
        timestamp = time.mktime(timestamp)
        if timestamp < time.time():
            messagebox.showerror("Error","Time was passed")
            return 0
        data = {"wallet_per":wallet_per.get(),"coin_name":coin_name.get(),
        "sell_per":sell_per.get(),"clock":entry_clock.get(),"day":str(day),"year":str(year),"month":str(month)}
        reader.set("","",data)
        messagebox.showinfo("Done","Order Saved")
        recents.destroy()
        recents = get_recent()
        caller.call(timestamp,wallet_per.get(),coin_name.get(),sell_per.get())
        return recents
def delete_click(coin,wallet,sell,date,clock):
    global recents
    try:
        reader.delete(coin,clock)
        caller.kill(coin)
        recents.destroy()
        recents = get_recent()
        return recents
    except:
        pass
def get_recent():
    recent_order = LabelFrame(root,text="Recent Orders")
    recent_order.pack(fill="both",expand="yes")
    data = reader.get("order")
    if len(data) == 0:
        Label(recent_order,text="No Orders").pack(side=tk.TOP)
    else:
        Label(recent_order,text="Coin Name",anchor="w").grid(row=1,column=3,ipadx=70,rowspan=2,sticky="n")
        Label(recent_order,text="Wallet %",anchor="w").grid(row=1,column=4,ipadx=70,rowspan=2)
        Label(recent_order,text="Sell %",anchor="w").grid(row=1,column=5,ipadx=70,rowspan=2)
        Label(recent_order,text="Calendar",anchor="w").grid(row=1,column=6,ipadx=70,rowspan=2)
        Label(recent_order,text="Clock",anchor="w").grid(row=1,column=7,ipadx=70,rowspan=2)
        row = 10
        for wallet in data:
            date = str(wallet["year"])+"/"+str(wallet["month"])+"/"+str(wallet["day"])
            Label(recent_order,text=wallet["coin_name"],anchor="w").grid(row=row,column=3,ipadx=70,rowspan=2)
            Label(recent_order,text=wallet["wallet_per"],anchor="w").grid(row=row,column=4,ipadx=70,rowspan=2)
            Label(recent_order,text=wallet["sell_per"],anchor="w").grid(row=row,column=5,ipadx=70,rowspan=2)
            Label(recent_order,text=date,anchor="w").grid(row=row,column=6,ipadx=70,rowspan=2)
            Label(recent_order,text=wallet["clock"],anchor="w").grid(row=row,column=7,ipadx=70,rowspan=2)
            Button(recent_order,width=1,text="Del",
            command=lambda:delete_click(wallet["coin_name"],wallet["wallet_per"],wallet["sell_per"],date,wallet["clock"])).grid(row=row,column=7,ipadx=20,rowspan=2)
            row+=5
    return recent_order
percentag_func = root.register(percenrage_validate)
percentag_func_sell = root.register(percenrage_validate_sell)
#Create Order
create_order = LabelFrame(root,text="Create Order")
create_order.pack(fill="both")
Label(create_order, text='Choose date').grid(row=3,column=5,ipadx=10)
cal = DateEntry(create_order, width=12, background='darkblue',foreground='white',borderwidth=2)
cal.grid(row=5,column=5,ipadx=10)
Label(create_order,text="Clock").grid(row=3,column=7,ipadx=10)
entry_clock = Entry(create_order)
entry_clock.grid(row=5,column=7,ipadx=10)
Label(create_order,text="Coin Name").grid(row=3,column=9,ipadx=10)
coin_name = Entry(create_order)
coin_name.grid(row=5,column=9,ipadx=10)
Label(create_order,text="Wallet % Buy").grid(row=3,column=11,ipadx=10)
wallet_per = Entry(create_order,validate="key",validatecommand=(percentag_func,"%P"))
wallet_per.grid(row=5,column=11,ipadx=10)
Label(create_order,text="Sell %").grid(row=3,column=13,ipadx=10)
sell_per = Entry(create_order,validate="key",validatecommand=(percentag_func_sell,"%P"))
sell_per.grid(row=5,column=13,ipadx=10)
button_order = Button(create_order,command=lambda:take_order(),text="Order")
button_order.grid(row=15,column=10,pady=10,ipadx=10)
#Setting
setting = LabelFrame(root,text="Setting")
setting.pack(fill="both")
Label(setting,text="telegram Token").pack()
telegram = Entry(setting)
telegram.pack()
Label(setting,text="Kucoin Api").pack()
kucoin_api = Entry(setting)
kucoin_api.pack()
Label(setting,text="Kucoin Secret").pack()
kucoin_secret = Entry(setting)
kucoin_secret.pack()
Label(setting,text="Kucoin PassPhrase").pack()
kucoin_pass = Entry(setting)
kucoin_pass.pack()
Button(setting,text="Save",command=setting_save).pack(pady=5)
fill_file()
#Recent Order
recents = get_recent()
root.mainloop()