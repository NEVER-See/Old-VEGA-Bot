import pymongo
import json


print("ㅤ\nㅤ\nㅤ\n\033[31m ██╗░░░██╗███████╗░██████╗░░█████╗░\n\033[0m\033[31m ██║░░░██║██╔════╝██╔════╝░██╔══██╗\n\033[0m\033[31m ╚██╗░██╔╝█████╗░░██║░░██╗░███████║\n\033[0m\033[31m ░╚████╔╝░██╔══╝░░██║░░╚██╗██╔══██║\n\033[0m\033[31m ░░╚██╔╝░░███████╗╚██████╔╝██║░░██║\n\033[0m\033[31m ░░░╚═╝░░░╚══════╝░╚═════╝░╚═╝░░╚═╝\033[0m\n")


# Для MongoDB временно, потом нужно удалить
try:
    file = "important_information/Tokens/token_MDB.txt"
    MDB_key = open(file, "r").readline()
    mongo = pymongo.MongoClient(MDB_key)
except:
    print("\033[31m [ ОШИБКА ]  Нет подключения к MongoDB!\n\033[0m")


def gdata(db, collection):
    return mongo[db][collection].find_one()


def wdata(db, collection, data):
    mongo[db][collection].update(gdata(db, collection), data)


with open("json/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

cpath = "release"
if config["debug_mode"]:
    cpath = "debug"


# Подключение к MongoDB
db_client = pymongo.MongoClient(
    "mongodb+srv://{}:{}@{}/db?retryWrites=true&w=majority".format(
        config["db_username"], config["db_password"], config["cluster_url"]
    )
)
db = db_client[config[cpath]["db_name"]]
print("\033[1;32m [ СТАРТ ]  База данных MongoDB подключена!\n\033[0m")


# Коллекции и их функционал
class Collection:
    def __init__(self, collection):
        self.collection = db[collection]
        self.cached = {}

    def add(self, id, data):  # Добавьте новый ключ в документ
        idict = {"_id": id}
        self.collection.update_one(idict, {"$set": data}, upsert=True)
        if id not in self.cached:
            self.cached[id] = {}
        for i in data:
            self.cached[id][i] = data[i]

    def remove(self, id):  # Удалить документ
        idict = {"_id": id}
        self.collection.delete_one(idict)
        del self.cached[id]

    def delete(self, id, data):  # Удаление ключа из документа
        idict = {"_id": id}
        self.collection.update_one(idict, {"$unset": data})
        for i in data:
            del self.cached[id][i]

    def load_data(self):  # Загрузка данных из каждого документа в коллекции
        results = self.collection.find({})
        for res in results:
            self.cached[res["_id"]] = res
        return self.cached


# Список коллекций
antibot = Collection(collection="antibot")  # Имя коллекции в базе данных
antibotdata = antibot.load_data()

antiinvite = Collection(collection="antiinvite")
antiinvitedata = antiinvite.load_data()

antimsg = Collection(collection="antimsg")
antimsgdata = antimsg.load_data()

antispam = Collection(collection="antispam")
antispamdata = antispam.load_data()

#channel_rights = Collection(collection="channel_rights")
#channel_rightsdata = channel_rights.load_data()

deactivate = Collection(collection="deactivate")
deactivatedata = deactivate.load_data()

ignorebots = Collection(collection="ignorebots")
ignorebotsdata = ignorebots.load_data()

language = Collection(collection="language")
languagedata = language.load_data()

logchannel = Collection(collection="logchannel")
logchanneldata = logchannel.load_data()

mute_users = Collection(collection="mute_users")
mute_usersdata = mute_users.load_data()

muterole = Collection(collection="muterole")
muteroledata = muterole.load_data()

passbots = Collection(collection="passbots")
passbotsdata = passbots.load_data()

recovery = Collection(collection="recovery")
recoverydata = recovery.load_data()

wlbots = Collection(collection="wlbots")
wlbotsdata = wlbots.load_data()

wltxt = Collection(collection="wltxt")
wltxtdata = wltxt.load_data()

wluser = Collection(collection="wluser")
wluserdata = wluser.load_data()

editserver = Collection(collection="editserver")
editserverdata = editserver.load_data()

hard_antibot = Collection(collection="hard_antibot")
hard_antibotdata = hard_antibot.load_data()

user_anticrash = Collection(collection="user_anticrash")
user_anticrashdata = user_anticrash.load_data()

"""prefix = Collection(collection = "prefix")
prefixdata = prefix.load_data()"""
