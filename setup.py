from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import telegram,requests,locale
locale.setlocale( locale.LC_ALL, '' )
coin_name_demand = ["REV","TEL","BSV","HEX","1M-BABYDOGE","100STARTL","1000ELON","ICP","LUNA"]
token = "5028534057:AAHTfG4-LrzYJJwZ_zgEaU8AlsI20ZgDLy4"
chat_id = ["69619707","93002681"]
updater = Updater(token=token,use_context=True)
header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"http://ramzinex.com/exchange/api/v1.0/exchange/pairs",
    "Accept-Language":"en-US,en;q=0.5",
    "Connection":"keep-alive",
    "Host":"ramzinex.com",
    "TE":"Trailers",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
}
ramzinex_price_list_url = "http://ramzinex.com/exchange/api/v1.0/exchange/pairs"
binance_get_price = "https://api.binance.com/api/v3/ticker/price"
compare = {}
def get_price(update,context):
    text_telegram = ""
    list_coin = requests.get(ramzinex_price_list_url,headers=header).json()
    a = 0
    for i in list_coin["data"]:
        a+=1
        if (str(i["base_currency_symbol"]["en"]).upper() in coin_name_demand) == True or str(i["quote_currency_symbol"]["en"]) != str("irr"):
            continue
        try:
            coin_name = str(i["base_currency_symbol"]["en"])
            prices = requests.get(ramzinex_price_list_url,headers=header)
            if prices.status_code != 200:
                raise ValueError("error")
            prices = prices.json()
            usdt = prices["data"][1]["sell"]
            for i in prices["data"]:
                if str(i["base_currency_symbol"]["en"]) == str(coin_name.lower()) and str(i["quote_currency_symbol"]["en"]) == str("irr"):
                    price_ramiznex = i["sell"]
                    binance_price = requests.get(binance_get_price+"?symbol="+coin_name.upper()+"USDT").json()
                    val = float(binance_price["price"])
                    profit = float(1000)/float(val)
                    text_telegram += "\ncoin name : "+str(coin_name)
                    text_telegram += "\ntether : "+str(usdt)
                    text_telegram += "\nbinance : "+str(val)
                    text_telegram += "\nramzinex : "+str(price_ramiznex)
                    val = float(binance_price["price"])*float(usdt)
                    text_telegram += "\nbinance * tethr: "+str(val)
                    profit *= float(price_ramiznex)-float(val)
                    text_telegram += "\nmin : "+str(float(price_ramiznex)-float(val))
                    text_telegram += "\nprofit :"+str(locale.currency(profit,grouping=True))+"\n\n"
                    compare[profit] = coin_name
        except Exception as ef:
            pass
        if str(a % 5) == str(0):
            for chatid in chat_id:
                context.bot.sendMessage(chat_id=str(chatid),text=str(text_telegram))
            text_telegram = ""
    maxprice = list(compare.keys())
    maxprice.sort()
    maxprice.reverse()
    maxprice = maxprice[0:4]
    for p in maxprice:
        for chatid in chat_id:
            maxprice = "Max Profit : "+str(p)+"\n"+"Coin Name : "+str(compare[p])
            context.bot.sendMessage(chat_id=str(chatid),text=str(maxprice))
    minprice = list(compare.keys())
    minprice.sort()
    minprice = minprice[0:4]
    for p in minprice:
        for chatid in chat_id:
            maxprice = "Min Profit : "+str(p)+"\n"+"Coin Name : "+str(compare[p])
            context.bot.sendMessage(chat_id=str(chatid),text=str(maxprice))
def start(update,context):
    list = [[telegram.KeyboardButton("دریافت قیمت")]]
    rp = telegram.ReplyKeyboardMarkup(list,resize_keyboard=True)
    text = "خوش آمدید"
    update.message.reply_text(text=text,reply_markup=rp)
updater.dispatcher.add_handler(CommandHandler("start",start))
updater.dispatcher.add_handler(MessageHandler(Filters.regex("دریافت قیمت"),get_price))
updater.start_polling()
updater.idle()