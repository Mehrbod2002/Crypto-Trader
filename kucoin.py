from defs import JSON
from notification import Noti,status
from base64 import b64encode
import time,hashlib,hmac,requests,uuid,random,json,websockets,asyncio
reader = JSON("data")
noti = Noti()
class Kucoin:
    def __init__(self):
        try:
            if reader.get("kucoin_secret") != "" and reader.get("kucoin_api") and reader.get("kucoin_pass"):
                self.key = reader.get("kucoin_api")
                self.secret = reader.get("kucoin_secret")
                self.passPhrase = reader.get("kucoin_pass")
                self.header = {"Content-Type":"application/json"}
                self.url = "https://api.kucoin.com"
            else:
                noti.send(status.empty_token.value)
        except:
            noti.send(status.empty_token.value)
    def signature(self,endpoint,method="GET",data={}):
        now = self.req("/api/v1/timestamp",data={},sign=False)
        try:
            now = now[1]["data"]
        except:
            return 0
        str_to_sign = str(now)+method+endpoint
        if len(data) != 0: str_to_sign+=data
        sign = b64encode(hmac.new(str(self.secret).encode("utf-8"),str_to_sign.encode('utf-8'),hashlib.sha256).digest())
        passPhrase = b64encode(hmac.new(str(self.secret).encode("utf-8"),str(self.passPhrase).encode("utf-8"),hashlib.sha256).digest())
        header = {
            "KC-API-SIGN": sign,
            "KC-API-TIMESTAMP": str(now),
            "KC-API-KEY": str(self.key),
            "KC-API-PASSPHRASE": passPhrase,
            "KC-API-KEY-VERSION": "2"
        }
        self.header.update(header)
    def req(self,endpoint,data,sign=True,method="GET"):
        if len(data) != 0:
            data = json.dumps(data)
        else:
            data = {}
        if sign:
            self.signature(endpoint,method,data)
        request = requests.request(method=str(method).lower(),url=self.url+endpoint,headers=self.header,data=data)
        return request.status_code,request.json()
    def new_order(self,side,symbol,amount,type="market"):
        data = {
            "clientOid":str(uuid.uuid4()),
            "side":str(side),
            "symbol":str(symbol),
            "type":str(type),
            "size":str(amount)
        }
        result = self.req("/api/v1/orders",data,method="POST")
        if str(result[0]) == str(200):
            noti.send(status.new_order.value+"\n"+str(result[1]["orderId"])+"\n"+str(data))
        return result
    def balance(self,symbol,percentage):
        result = self.req("/api/v1/margin/account",data={})
        if result != 0:
            try:
                if result["accounts"][0]["currency"] == symbol:
                    result = float(result["accounts"][0]["currency"]["availableBalance"])*float(percentage/100)
                    if result > 0:
                        return result
                    else:
                        noti.send(status.balance_not_enough)
                        return 0
            except:
                return 0
    def websocket_token(self):
        data = {
            "id": str(random.randrange(10000000,99999999)),                       
            "type": "ping",                
        }
        result = self.req("/api/v1/bullet-private",data,method="POST")
        if result[0] == 200:
            return_data = result[1]["data"]["instanceServers"][0]
            id = str(int(time.time()*1000))
            url = f'{return_data["endpoint"]}?token={result[1]["data"]["token"]}&connectId={id}'
            return url,return_data["encrypt"],return_data["pingTimeout"],id
        return 0
    async def price_checker(self,coin,percentage,amount):
        data = self.websocket_token()
        async def looper():
            if data != 0:
                subscribe = {
                    "id": data[3],                         
                    "type": "subscribe",
                    "topic": f"/market/snapshot:{coin}",
                    "response":True                 
                }
                i = 0
                async with websockets.connect(data[0]) as socket:
                    datas = await asyncio.wait_for(socket.recv(),timeout=int(data[2]))
                    while True:
                        await asyncio.shield(socket.send(json.dumps(subscribe)))
                        datas = json.loads(await asyncio.wait_for(socket.recv(),timeout=int(data[2])))
                        if datas["type"] != "ack" and datas["type"] == "message":
                            price_float = float(datas["data"]["data"]["sell"])
                            if i == 0:
                                inital_price = price_float
                                continue
                            inital_price = float(inital_price)
                            if (((float(percentage)/100)*inital_price) <= price_float):
                                self.new_order("sell",coin,amount)
                                try:
                                    asyncio.get_running_loop().stop()
                                except:
                                    asyncio.get_running_loop().close()
                            i+=1
                        await asyncio.sleep(0.1)
        async def main():
            loop = asyncio.get_event_loop()
            loop.run_forever(await looper())
        try:
            asyncio.run(main())
        except:
            pass
    async def check_time(self,timestamp,amount,coin,percentage):
        amount = self.balance("USDT",amount)
        if amount == 0:return
        while True:
            if int(timestamp) <= int(time.time()*1000):
                await asyncio.gather(
                    self.new_order("buy",coin,amount),
                    self.price_checker(coin,percentage,amount)
                )
                break