import pymongo
import json

with open("json/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

cpath = "release"
if config["debug_mode"]:
    cpath = "debug"


# Подключение к MongoDB
db_client = pymongo.MongoClient("mongodb+srv://{}:{}@{}/db?retryWrites=true&w=majority".format(config["db_username"], config["db_password"], config["cluster_url"]))
db = db_client[config[cpath]["db_name"]]
print("[ ИНФО ]  База данных MongoDB подключена!\n")


# Коллекции и их функционал
class Collection:
    def __init__(self, collection):
        self.collection = db[collection]
        self.cached = {}

    def add(self, id, data): # Добавьте новый ключ в документ
        idict = {"_id": id}
        self.collection.update_one(idict, {"$set": data}, upsert=True)
        if not id in self.cached:
            self.cached[id] = {}
        for i in data:
            self.cached[id][i] = data[i]

    def remove(self, id): # Удалить документ
        idict = {"_id": id}
        self.collection.delete_one(idict)
        del self.cached[id]

    def delete(self, id, data): # Удаление ключа из документа
        idict = {"_id": id}
        self.collection.update_one(idict, {"$unset": data})
        for i in data:
            del self.cached[id][i]

    def load_data(self): # Загрузка данных из каждого документа в коллекции
        results = self.collection.find({})
        for res in results:
            self.cached[res["_id"]] = res
        return self.cached


# Список коллекций
antibot = Collection(collection = "antibot") # Имя коллекции в базе данных
antibotdata = antibot.load_data()

antiinvite = Collection(collection = "antiinvite") # Имя коллекции в базе данных
antiinvitedata = antiinvite.load_data()

antimsg = Collection(collection = "antimsg") # Имя коллекции в базе данных
antimsgdata = antimsg.load_data()

antispam = Collection(collection = "antispam") # Имя коллекции в базе данных
antispamdata = antispam.load_data()

channel_rights = Collection(collection = "channel_rights") # Имя коллекции в базе данных
channel_rightsdata = channel_rights.load_data()

deactivate = Collection(collection = "deactivate") # Имя коллекции в базе данных
deactivatedata = deactivate.load_data()

ignorebots = Collection(collection = "ignorebots") # Имя коллекции в базе данных
ignorebotsdata = ignorebots.load_data()

language = Collection(collection = "language") # Имя коллекции в базе данных
languagedata = language.load_data()

logchannel = Collection(collection = "logchannel") # Имя коллекции в базе данных
logchanneldata = logchannel.load_data()

mute_users = Collection(collection = "mute_users") # Имя коллекции в базе данных
mute_usersdata = mute_users.load_data()

muterole = Collection(collection = "muterole") # Имя коллекции в базе данных
muteroledata = muterole.load_data()

passbots = Collection(collection = "passbots") # Имя коллекции в базе данных
passbotsdata = passbots.load_data()

recovery = Collection(collection = "recovery") # Имя коллекции в базе данных
recoverydata = recovery.load_data()

wlbots = Collection(collection = "wlbots") # Имя коллекции в базе данных
wlbotsdata = wlbots.load_data()

wltxt = Collection(collection = "wltxt") # Имя коллекции в базе данных
wltxtdata = wltxt.load_data()

"""prefix = Collection(collection = "prefix") # Имя коллекции в базе данных
prefixdata = prefix.load_data()"""