import os,json
class JSON:
    def __init__(self,file):
        if os.path.exists(file+".json") == False:
            with open(file+".json","w") as reader:
                data = {"kucoin_secret":"","kucoin_api":"","kucoin_pass":"","order":[]}
                json.dump(data,reader)
        self.file = file+".json"
    def get(self,key):
        with open(self.file,"r") as reader:
            data = json.loads(reader.read())
            try:
                return data[key]
            except:
                return ""
    def set(self,key,value,arrow=None):
        if arrow == None:
            with open(self.file,"r") as reader:
                data = json.loads(reader.read())
                data[key] = value
                with open(self.file,"w") as readers:
                    json.dump(data,readers)
        else:
            with open(self.file,"r") as reader:
                data = json.loads(reader.read())
                data["order"].append(arrow)
                with open(self.file,"w") as readers:
                    json.dump(data,readers)
    def delete(self,coin_name,clock):
        with open(self.file,"r") as file:
            data = json.loads(file.read())
            list = [item for item in data["order"] if str(item["clock"]) != str(clock) and str(item["coin_name"]) != str(coin_name)]
            data["order"] = list
            with open(self.file,"w") as file:
                json.dump(data,file)