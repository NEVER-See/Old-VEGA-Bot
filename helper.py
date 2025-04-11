import disnake as discord
import json

# import word
# import config
# from discord import utils
from cache import *


# Запуск бота
# with open("json/config.json", "r", encoding="utf-8") as f:
#    config = json.load(f)


# Для создателей бота
# async def is_owner(ctx):
#    if not ctx.author.id in config["owner_ids"]:
#        await ctx.send("Эта команда доступна только владельцам ботов!")
#        return False
#    return True


# Проверка языка
def get_language(id, text):
    try:
        language = languagedata[int(id)]["language"]
    except KeyError:
        language = True

    with open("languages/en.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if language == False:
        try:
            return data[text]
        except:
            return text
    else:
        return text


# Проверка канала на разрешение
"""async def checkchannel(ctx):
    #    with open('json/channel_rights.json', 'r') as f:
    #        data = json.load(f)
    if ctx.guild.id not in channel_rightsdata:
        return True
    elif "rights" not in channel_rightsdata[ctx.guild.id]:
        return True
    else:
        return ctx.channel.id in channel_rightsdata[ctx.guild.id]["rights"]
        if not str(ctx.channel.id) in data[str(ctx.guild.id)]:
            embed = discord.Embed(
                description=f":warning: Эта команда доступна только в определенных каналах!",
                color=0xFCC21B,
            )
            await ctx.send(embed=embed, delete_after=5.0)
            ctx.command.reset_cooldown(ctx)
        else:
            if str(ctx.channel.id) in data[str(ctx.channel.guild.id)]:
                embed = discord.Embed(
                    description=":warning: Чтобы писать команды, укажите боту канал для команд!\nИспользуйте команду: `v!channel add <#chanel | ID>`",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, delete_after=15.0)"""


# Для эмодзи
def convert_em(emoji):
    if emoji.startswith("<"):
        emoji = emoji.replace("<:", "")
        emoji = emoji.replace("<a:", "")
        emoji = emoji[:-20]
    else:
        emoji = emoji.replace(":", "")
    return emoji


# Конвертор времени по языку
def convert(time):
    time_convert = {
        "s": 1,
        "с": 1,
        "m": 60,
        "м": 60,
        "h": 3600,
        "ч": 3600,
        "d": 86400,
        "д": 86400,
    }
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return time


# Время в мин часах днях
def hmsd(ctx, sec: float):
    d = int(sec // 86400)
    h = int((sec % 86400) // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(sec % 1 * 1000)

    if h > 0:
        display_h = f"**{h}** {get_language(ctx.guild.id,'ч')} "
    else:
        display_h = ""

    if m > 0:
        display_m = f"**{m}** {get_language(ctx.guild.id,'мин')} "
    else:
        display_m = ""

    if s > 0:
        display_s = f"**{s}** {get_language(ctx.guild.id,'сек')}"
    else:
        display_s = ""

    if sec < 1:
        return f"**{ms}** {get_language(ctx.guild.id,'мс')}"
    elif sec < 60:
        return f"**{s}** {get_language(ctx.guild.id,'сек')} **{ms}** {get_language(ctx.guild.id,'мс')}"
    elif sec < 3600:
        return f"**{m}** {get_language(ctx.guild.id,'мин')} {display_s} **{ms}** {get_language(ctx.guild.id,'мс')}"
    elif sec < 86400:
        return f"**{h}** {get_language(ctx.guild.id,'ч')} {display_m}{display_s} **{ms}** {get_language(ctx.guild.id,'мс')}"
    else:
        return f"**{d}** {get_language(ctx.guild.id,'д')} {display_h}{display_m}{display_s}"


def hmsd1(ctx, sec: float):
    d = int(sec // 86400)
    h = int((sec % 86400) // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(sec % 1 * 1000)

    if h > 0:
        display_h = f"{h} {get_language(ctx.guild.id,'ч')} "
    else:
        display_h = ""

    if m > 0:
        display_m = f"{m} {get_language(ctx.guild.id,'мин')} "
    else:
        display_m = ""

    if s > 0:
        display_s = f"{s} {get_language(ctx.guild.id,'сек')}"
    else:
        display_s = ""

    if sec < 1:
        return f"{ms} {get_language(ctx.guild.id,'мс')}"
    elif sec < 60:
        return f"{s} {get_language(ctx.guild.id,'сек')} {ms} {get_language(ctx.guild.id,'мс')}"
    elif sec < 3600:
        return f"{m} {get_language(ctx.guild.id,'мин')} {display_s} {ms} {get_language(ctx.guild.id,'мс')}"
    elif sec < 86400:
        return f"{h} {get_language(ctx.guild.id,'ч')} {display_m}{display_s} {ms} {get_language(ctx.guild.id,'мс')}"
    else:
        return f"{d} {get_language(ctx.guild.id,'д')} {display_h}{display_m}{display_s}"


# Заменитель пробелов в ссылке
def urlspotify(s):
    s = s.strip().split(" ")
    return ("%20").join(s)


def url_game_search(s):
    s = s.strip().split(" ")
    return ("%20").join(s)
