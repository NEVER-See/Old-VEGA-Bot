# -*- coding: utf-8 -*-
import disnake as discord
import disnake
import asyncio
import datetime
import time
import random
import json
import os
import re
from discord import activity
from discord import webhook
from discord.channel import DMChannel
import requests
import pymongo
import typing
import aiohttp

# import word
# import config
# from discord import utils
from discord.ext import tasks
from discord.utils import get
from discord.ext import commands
from random import randint
from disnake.ext import commands
from helper import checkchannel, convert, hmsd, hmsd1, urlspotify, get_language
from cache import *
import json
from enum import Enum

# from plot import send_graph
# from Cybernator import Paginator as pag
# from config import Color
# from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
# from discord_buttons import DiscordButton, Button, ButtonStyle, InteractionType
# from PIL import Image, ImageFont, ImageDraw, ImageOps
# from pypresence import Presence

# from discord.http import Route
# print(Route.BASE)


# Для хелпа
HELP_MENUS = {}
HELP_COMMANDS = {}

# Для Антиспама
"""time_window_milliseconds = 5000
time_window_milliseconds_bot = 10000
max_msg_per_window = 5
max_msg_per_window_bot = 10
author_msg_times = {}"""


intents = disnake.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True


# Активиция MongoDB
with open("json/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


# Для MongoDB временно, потом нужно удалить
try:
    MDB_key = open("important_information/Tokens/token_MDB.txt", "r").readline()
    mongo = pymongo.MongoClient(MDB_key)
except:
    print("!!! [ ОШИБКА ]  Нет подключения к MongoDB!\n")


def gdata(db, collection):
    return mongo[db][collection].find_one()


def wdata(db, collection, data):
    mongo[db][collection].update(gdata(db, collection), data)


# Клиент — сам бот
#test_guilds=[824906215304986625, 826022179568615445, 779351525586632784]
prefix = "/"
client = commands.AutoShardedBot(
    intents=intents,
    command_prefix=prefix,
    sync_permissions=True,
    shard_count=config["shard_count"],
    activity=discord.Game("loading..."),
)
client.remove_command("info")
client.remove_command("clear")
client.remove_command("help")

cpath = "release"
if config["debug_mode"]:
    cpath = "debug"


# Коги — запуск команд
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        # try:
        client.load_extension("cogs." + file[:-3])
        print(f"[ ИНФО ]  Cog загружен: {file[:-3]}\n")
        """except:
            print(f"[ ОШИБКА ]  Cog не загружен: {file[:-3]}\n")"""


# Кол-во серверов и шардов, мониторинг бота
@tasks.loop(minutes=35)
async def update_sdc_stats():
    if client.user.id == 795551166393876481:
        API_ds_key = open(
            "important_information/Tokens/API_sd.txt", "r"
        ).readline()  # Проверить правильность написание указания файла по папкам
        try:
            r = requests.post(
                "https://api.server-discord.com/v2/bots/795551166393876481/stats",
                headers={"Authorization": f"SDC {API_ds_key}"},
                data={"shards": client.shard_count, "servers": len(client.guilds)},
            )
            print(f"[ ИНФО ]  Серверов: {len(client.guilds)}\n")
            print(f"[ ИНФО ]  Отправляю данные на BDSC {r}\n")
        except Exception as e:
            print(f"!!! [ ОШИБКА ]  Не удалось обновить счетчик из-за: {e}\n")
    else:
        print("[ ИНФО ]  Активирован тестовый бот! (Мониторинг: BSDC)\n")


# Префикс бота и его смена в json
@tasks.loop(minutes=5)
async def update_stats():
    if client.user.id == 795551166393876481:
        try:
            w = gdata("vega", "wlbots")
            count1 = w["Bots"].count(",")

            user = client.get_guild(826022179568615445).me
            online = discord.Status.online
            dnd = discord.Status.dnd
            if user.status == online or dnd:
                bstatus = f"https://cdn.discordapp.com/attachments/713751423128698950/842622758664142868/everything_is_stable.gif"
            if user.status == discord.Status.idle:
                bstatus = f"https://cdn.discordapp.com/attachments/713751423128698950/842622756885102632/possible_shutdown.gif"
            if user.status == discord.Status.offline:
                bstatus = f"https://cdn.discordapp.com/attachments/777495710252924928/894569603726974976/not_online.png"

            if user.status == online or dnd:
                bstatus1 = f"Онлайн"
            if user.status == discord.Status.idle:
                bstatus1 = f"Деактивирован"
            if user.status == discord.Status.offline:
                bstatus1 = f"Не в сети"

            requests.post(
                "https://vegabot.xyz/vegabot/updatesg.php",
                data={
                    "SERVERS": len(client.guilds),
                    "SHARDS": len(client.shards),
                    "USERS": len([m for m in client.users if not m.bot]),
                    "OWN1": client.get_user(351020816466575372),
                    "OWN2": client.get_user(750245767142441000),
                    "OWN3": client.get_user(777494101179629569),
                    "WLBOTS": count1,
                    "STATUS": bstatus,
                    "STATUS1": bstatus1,
                },
            )

            """shard0 = client.get_shard(0)
            shard1 = client.get_shard(1)
            shard2 = client.get_shard(2)
            shard3 = client.get_shard(3)
            g0 = len([g for g in client.guilds if g.shard_id == 0])
            g1 = len([g for g in client.guilds if g.shard_id == 1])
            g2 = len([g for g in client.guilds if g.shard_id == 2])
            g3 = len([g for g in client.guilds if g.shard_id == 3])
            requests.get(f'https://vegabot.xyz/vegabot/status/shards/update.php?s0p={int(shard0.latency * 1000)}&s0s={g0}&s1p={int(shard1.latency * 1000)}&s1s={g1}&avg={int(client.latency * 1000)}&s2s={g2}&avg2={int(client.latency * 1000)}&s3s={g3}&avg3={int(client.latency * 1000)}')"""
            print("[ ИНФО ]  Сервера и шарды были обновлены на сайте!\n")
        except:
            print("!!! [ ОШИБКА ]  Что-то пошло не так!\n")
    else:
        print("[ ИНФО ]  Активирован тестовый бот! (Сайт VEGA)\n")


class FLAGS:
    total_connected = 0
    started_tasks = False


@client.event
async def on_connect():
    FLAGS.total_connected += 1
    if FLAGS.total_connected >= client.shard_count:
        if FLAGS.started_tasks:
            return
        FLAGS.started_tasks = True
        update_sdc_stats.start()
        update_stats.start()
        # client.loop.create_task(refresh())
        print("[ ЗАГРУЗКА ]  Запуск задач (tasks)...\n")


# Запуск бота
@client.event
async def on_ready():
    # client.loop.create_task(update_stats())
    client.start_time = datetime.datetime.now()
    w = gdata("vega", "wlbots")
    count1 = w["Bots"].count(",")
    if count1:
        print(f"[ ИНФО ]  Ботов в белом списке: {count1}\n")
    else:
        print("!!! [ ОШИБКА ]  Ботов в белом списке не обнаружено!\n")

    try:
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if not enabled:
            channel = client.get_channel(
                812666804441841684
            )  # получаем айди канала 812666804441841684
            await channel.send("\🔄**` RESTART `**\nБот **VEGA ⦡#7724** был запущен!")
            print(">>>  [ ЗАПУСК ]  БОТ включен и готов к работе!\n")
        else:
            channel = client.get_channel(
                812666804441841684
            )  # получаем айди канала 812666804441841684
            await channel.send(
                "\🔄**` RESTART `**\nБот **VEGA ⦡#7724** был запущен (деактивирован)!"
            )
            print(f">>>  [ ЗАПУСК ]  В данный момент, бот деактивирован!\n")
    except:
        print(">>>  [ ОШИБКА ]  Сообщение о запуске бота небыло доставлено!\n")
        pass

    # Статус бота (не беспокоить, играет в v!help, смотрит за сервером VEGA ⦡)
    # guilds = await client.fetch_guilds(limit = None).flatten()
    # guilds = client.guilds

    # await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f"v!help | Bots wl: 300+ | vegabot.xyz"))

    while True:
        try:
            try:
                enabled = deactivatedata[0]["Option"]
            except KeyError:
                enabled = False
            if not enabled:
                w = gdata('vega', 'wlbots')
                count = w["Bots"].count(',')
                await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f"Bots wl: {count} | vegabot.xyz"))
            else:
                await client.change_presence(status=discord.Status.idle, activity=discord.Game("DEACTIVATED"))
        except:
            pass
        await asyncio.sleep(300)
        """try:
            try:
                enabled = deactivatedata[0]["Option"]
            except KeyError:
                enabled = False
            if not enabled:
                await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f"vegabot.xyz | v!help"))
            else:
                await client.change_presence(status=discord.Status.idle, activity=discord.Game("DEACTIVATED"))
        except:
            pass
        await asyncio.sleep(120)
        try:
            try:
                enabled = deactivatedata[0]["Option"]
            except KeyError:
                enabled = False
            if not enabled:
                await client.change_presence(status = discord.Status.dnd, activity= discord.Activity(name=f'{len(client.guilds)} servers', type= discord.ActivityType.watching))
            else:
                await client.change_presence(status=discord.Status.idle, activity=discord.Game("DEACTIVATED"))
        except:
            pass
        await asyncio.sleep(120)
        try:
            try:
                enabled = deactivatedata[0]["Option"]
            except KeyError:
                enabled = False
            if not enabled:
                w = gdata('vega', 'wlbots')
                count = w["Bots"].count(',')
                await client.change_presence(status = discord.Status.dnd, activity= discord.Activity(name=f'{count} bots in the wl', type= discord.ActivityType.watching))
            else:
                await client.change_presence(status=discord.Status.idle, activity=discord.Game("DEACTIVATED"))
        except:
            pass
        await asyncio.sleep(120)"""

        """try:
            try:
                enabled = deactivatedata[0]["Option"]
            except KeyError:
                enabled = False
            if not enabled:
                await client.change_presence(
                    status=discord.Status.dnd, activity=discord.Game("〔████[][] 60%〕")
                )
            else:
                await client.change_presence(
                    status=discord.Status.idle, activity=discord.Game("DEACTIVATED")
                )
        except:
            pass
        await asyncio.sleep(20)
        try:
            try:
                enabled = deactivatedata[0]["Option"]
            except KeyError:
                enabled = False
            if not enabled:
                await client.change_presence(
                    status=discord.Status.dnd, activity=discord.Game("〔█████[] 80%〕")
                )
            else:
                await client.change_presence(
                    status=discord.Status.idle, activity=discord.Game("DEACTIVATED")
                )
        except:
            pass
        await asyncio.sleep(20)
        try:
            try:
                enabled = deactivatedata[0]["Option"]
            except KeyError:
                enabled = False
            if not enabled:
                await client.change_presence(
                    status=discord.Status.dnd, activity=discord.Game("〔██████  100%〕")
                )
            else:
                await client.change_presence(
                    status=discord.Status.idle, activity=discord.Game("DEACTIVATED")
                )
        except:
            pass
        await asyncio.sleep(20)"""


def first_allowed_channel(guild):
    if guild.system_channel is not None:
        can = guild.system_channel.permissions_for(guild.me)
        if can.send_messages and can.embed_links:
            return guild.system_channel
    for channel in guild.text_channels:
        can = channel.permissions_for(guild.me)
        if can.send_messages and can.embed_links:
            return channel


# Присоеденился на сервер
@client.event
async def on_guild_join(guild):
    lan = gdata("vega", "language")
    if not str(guild.id) in lan:
        if str(guild.region) == "russia":
            lan[str(guild.id)] = True
        else:
            lan[str(guild.id)] = False
    else:
        pass

    try:
        enabled = lan[str(guild.id)]
    except KeyError:
        enabled = False
    if not enabled:
        lan[str(guild.id)] = False
    else:
        pass
    wdata("vega", "language", lan)

    version_bot = open("important_information/version_bot.txt", "r").readline()
    try:
        prefix = "/"
        embed = discord.Embed(
            title=f"{get_language(guild.id,'👋 Привет, спасибо что добавили меня!')}",
            description=f"{get_language(guild.id,'• Префикс на сервере')} `{prefix}`, {get_language(guild.id,'справка по командам')} `{prefix}help`.\n• {get_language(guild.id,'Сменить язык:')} `{prefix}{get_language(guild.id,'lang en')}`\n\n{get_language(guild.id,'**Описание:**')}\n{get_language(guild.id,'• Бот предназначен для защиты вашего сервера от других ботов! Защиты от self-ботов пока нет. Чтобы включить защиту, напишите команду')} `{prefix}antibot on` {get_language(guild.id,'(Данную команду может включить только Владелец сервера!).')}\n{get_language(guild.id,'Командой')} `{prefix}channel add {get_language(guild.id,'{#канал | ID канала}')}` {get_language(guild.id,'добавьте канал, в котором бот сможет отвечать на команды.')} {get_language(guild.id,'Советуем не убирать право Администратора у бота для корректной работы.')}\n{get_language(guild.id,'Для проверки ботов введите команду')} `{prefix}checkwl all`",
            color=0xE21E1E
        )
        embed.add_field(
            name=f":warning: {get_language(guild.id,'Важно:')}",
            value=f"{get_language(guild.id,'- Команды')} `channel`, `clear`, `uclear`, `echo`, `emb`, `delchannels` {get_language(guild.id,'и')} `delroles` {get_language(guild.id,'работают во всех каналах!')}",
            inline=False
        )
        embed.add_field(
            name=f"{get_language(guild.id,'🗃 Версия бота:')}",
            value=f"{version_bot}",
            inline=True
        )
        embed.add_field(
            name=f"<:vb_developer:931450178488107060> {get_language(guild.id,'Разработчик:')}",
            value=f"{client.get_user(351020816466575372)}\n`ID: 351020816466575372`\n\n{client.get_user(750245767142441000)}\n`ID: 750245767142441000`",
            inline=True
        )
        #            embed.add_field(name='<:python:814170890564534342> Версия py:', value='v.3.9.2', inline=True)
        embed.add_field(
            name=f"{get_language(guild.id,'Зарегистрирован:')}",
            value=f"<t:{int(client.user.created_at.timestamp())}:F>",
            inline=False
        )
        embed.add_field(
            name=f"{get_language(guild.id,'🔗 Ссылки:')}",
            value=f"{get_language(guild.id,'[Документация](https://never-see.gitbook.io/vega-bot/v/russian/)')}\n{get_language(guild.id,'[Сайт бота](https://vegabot.xyz/vegabot/)')}\n{get_language(guild.id,'[Служба поддержки](https://discord.gg/8YhmtsYvpK)')}",
            inline=False
        )
        embed.set_thumbnail(
            url=client.get_user(795551166393876481).avatar.replace(size=1024)
        )
        embed.set_footer(
            icon_url=client.get_user(351020816466575372).avatar.replace(size=1024),
            text=f"{client.get_user(351020816466575372)} {get_language(guild.id, '© 2021 - 2022 Все права защищены!')}"
        )
        await first_allowed_channel(guild).send(embed=embed)
        embed = discord.Embed(
            description=f"{get_language(guild.id,'**Обязательно выполните следующее:**')}\n{get_language(guild.id,'**1)** Не отбирать права Администратора у бота.')}\n{get_language(guild.id,'**2)** Переместить роль бота на самый верх списка ролей.')}\n{get_language(guild.id,'**3)** Если есть боты, которых нужно игнорировать, то занесите их в список.')}\n{get_language(guild.id,'**4)** Включить функцию AntiBot.')}",
            color=0xE21E1E
        )
        await first_allowed_channel(guild).send(embed=embed)
        # await entry.user.send(embed=embed)
    except:
        pass

    if client.user.id == 795551166393876481:
        try:
            async for entry in guild.audit_logs(
                limit=1, action=discord.AuditLogAction.bot_add
            ):
                owner = guild.owner
                inv_user = entry.user
                if owner == inv_user:
                    invuser = ""
                else:
                    invuser = f"\n**Кто пригласил:** {inv_user}\n**ID кто пригласил:** {inv_user.id}"

                embed = discord.Embed(
                    title="Бот был добавлен на сервер",
                    description=f"**Сервер:** {guild.name}\n**ID сервера:** {guild.id}\n**Количество участников:** {len(guild.members)}\n**Владелец:** {owner}\n**ID Владельца:** {owner.id}{invuser}",
                    color=discord.Colour.green()
                )
                embed.set_thumbnail(url=guild.icon)
                await client.get_channel(811963689677619230).send(embed=embed)
        except:
            pass
    else:
        pass

    w = gdata("vega", "wlbots")
    wl = gdata("vega", "ignorebots")
    ig = []
    prefix = "/"
    try:
        enabled = False
        if str(guild.id) in wl:
            dop = wl[str(guild.id)]
        else:
            dop = ""
    except KeyError:
        print("!!! [ ОШИБКА ] Произошла неизвестная ошибка!")
        pass
    embed = discord.Embed(
        description=f"{get_language(guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется проверка ботов...')}",
        color=0xF4900C
    )
    msg = await first_allowed_channel(guild).send(embed=embed)
    new = await first_allowed_channel(guild).fetch_message(msg.id)
    for member in [m for m in guild.members if m.bot]:
        # try:
        if not str(member.id) in w[str("Bots")] and not str(member.id) in dop:
            ig.append(member.mention)

    bot1 = len([m for m in guild.members if m.bot])
    if bot1 > 1:
        embed = discord.Embed(
            title=f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Проверка завершена!')}",
            color=0x43B581
        )
        await asyncio.sleep(2)
        if len(ig) == 0:
            embed.description = f"{get_language(guild.id,'Все боты были проверены.')}"
        else:
            try:
                enabled = deactivatedata[0]["Option"]
            except KeyError:
                enabled = False
            if enabled:
                embed.description = (
                    f"{get_language(guild.id,'⚠️ В данный момент бот деактивирован!')}"
                )
                embed.add_field(
                    name=f"{get_language(guild.id,'Боты:')}",
                    value=", ".join(ig),
                    inline=False
                )
            else:
                data = gdata("vega", "antibot")
                try:
                    enabled = data[str(member.guild.id)]
                except KeyError:
                    enabled = False
                if member.bot:
                    if enabled:
                        embed.description = f"{get_language(guild.id,'Данные боты могут быть забанены функцией **AntiBot**!')}\n{get_language(guild.id,'Воспользуйтесь командой')} `{prefix}ignore add @user`, {get_language(guild.id,'чтобы занести ботов в игнорируемый список.')}"
                        embed.add_field(
                            name=f"{get_language(guild.id,'Боты:')}",
                            value=", ".join(ig),
                            inline=False
                        )
                    else:
                        embed.description = f"{get_language(guild.id,'Данные боты не занесены в игнорируемый список!')}\n{get_language(guild.id,'Воспользуйтесь командой')} `{prefix}ignore add @user`, {get_language(guild.id,'чтобы занести ботов в список.')}"
                        embed.add_field(
                            name=f"{get_language(guild.id,'Боты:')}",
                            value=", ".join(ig),
                            inline=False
                        )
        await new.edit(embed=embed)
    else:
        embed = discord.Embed(
            description=f"{get_language(guild.id,'<a:vega_x:810843492266803230> Боты не обнаружены!')}",
            color=0xCC1A1D
        )
        await new.edit(embed=embed)


# Информация о командах
"""
#Кнопки для справки
class links(disnake.ui.View):
    def __init__(self, ctx):
        super().__init__()

        url1 = f"{get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/')}"
        self.add_item(disnake.ui.Button(label=f"{get_language(ctx.guild.id,'📚 Документация')}", url=url1))

        url2 = "https://vegabot.xyz/vegabot"
        self.add_item(disnake.ui.Button(label=f"{get_language(ctx.guild.id,'🌐 Сайт')}", url=url2))

class menuhelp(disnake.ui.Select):
    async def menu_help(self, ctx):
        options = [
            disnake.SelectOption(
                emoji="<:info:860380081268588545>", label=f"{get_language(ctx.guild.id, 'Информация')}", description=f"{get_language(ctx.guild.id,'Команды информации.')}", value="❓"
            ),
            disnake.SelectOption(
                emoji="<:owner:860380081594564688>", label=f"{get_language(ctx.guild.id,'Для Владельца')}", description=f"{get_language(ctx.guild.id,'Команды для Владельца.')}", value="👑"
            ),
            disnake.SelectOption(
                emoji="<:admin:860380081536761886>", label=f"{get_language(ctx.guild.id,'Для Администратора')}", description=f"{get_language(ctx.guild.id,'Команды для Администратора.')}", value="⚙️"
            ),
            disnake.SelectOption(
                emoji="<:moder:860380081627856906>", label=f"{get_language(ctx.guild.id,'Для Модератора')}", description=f"{get_language(ctx.guild.id,'Команды для Модератора.')}", value="🛠"
            ),
            disnake.SelectOption(
                emoji="<:fun:860380081637031936>", label=f"{get_language(ctx.guild.id,'Веселье')}", description=f"{get_language(ctx.guild.id,'Команды веселья.')}", value="🎉"
            ),
        ]
        super().__init__(
                placeholder=f"{get_language(ctx.guild.id, 'Выберите группу')}",
                min_values=1,
                max_values=1,
                options=options,
            )
    async def interaction_check(self, ctx):
        if ctx.author != self.author:
            await ctx.send(f"{get_language(ctx.guild.id, 'Этим меню управляете не вы!')}", ephemeral=True)
            return False
        return True
class menuhelpview(disnake.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(menuhelp())
"""


class Info(int, Enum):
    ping = 1
    info = 2
    stats = 3
    server = 4
    user = 5
    links = 6
    wlbots = 7


class Owner(int, Enum):
    reset = 1
    rgive = 2
    rselect = 3
    antibot = 4
    antiinvite = 5
    ignore = 6
    pаss = 7
    delchannels = 8
    delroles = 9


class Admin(int, Enum):
    log = 1
    language = 2
    channel = 3
    rmute = 4
    settings = 5
    list = 6
    echo = 7
    emb = 8
    slowmode = 9


class Moder(int, Enum):
    checkwl = 1
    ban = 2
    unban = 3
    kick = 4
    clear = 5
    uclear = 6
    rolen = 7
    mute = 8
    unmute = 9


class Fun(int, Enum):
    eightball = 1
    avatar = 2
    emoji = 3
    random = 4
    math = 5


# @commands.guild_permissions(826022179568615445, user_ids={351020816466575372: True})
# @commands.bot_has_permissions(send_messages=True)
# @commands.cooldown(1, 5, commands.BucketType.member)
@client.slash_command(
    name="help",
    description="Help about commands (Select the group and command) | Справка о командах (Укажите группу и команду)",
)
@commands.guild_only()
@commands.bot_has_permissions(send_messages=True, embed_links=True)
async def help(
    ctx,
    info: Info = commands.Param(
        description="Select the group and command | Укажите группу и команду"
    )
    == None,
    owner: Owner = commands.Param(
        description="Select the group and command | Укажите группу и команду"
    )
    == None,
    admin: Admin = commands.Param(
        description="Select the group and command | Укажите группу и команду"
    )
    == None,
    moder: Moder = commands.Param(
        description="Select the group and command | Укажите группу и команду"
    )
    == None,
    fun: Fun = commands.Param(
        description="Select the group and command | Укажите группу и команду"
    )
    == None,
):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        if await checkchannel(ctx):
            # row_i = ActionRow(Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vegabot.xyz/vegabot"))
            timestamp = datetime.datetime.now()
            on = "{on}"
            off = "{off}"
            add = "{add}"
            remove = "{remove}"
            эмодзи = "{эмодзи}"
            число = "{число}"
            текст = "{текст}"
            символы = "{символы}"
            пример = "{пример}"
            причина = "{причина}"
            a = "{a}"
            b = "{b}"
            название_роли = "{название роли}"
            роль = "{@роль}"
            роли = "{ID роли}"
            бота = "{ID бота}"
            всем = "{all}"
            пользователь = "{@пользователь}"
            пользователя = "{ID пользователя}"
            канал = "{#канал}"
            канала = "{ID канала}"
            channels = "{channels}"
            ignores = "{ignores}"
            каналов = "{каналов}"
            игнора = "{игнора}"
            название_канала = "{название канала}"
            обязательный_параметр = "{**_обязательный параметр_**}"
            wl = "{wl}"
            бс = "{бс}"
            все = "{all}"
            преф = "{prefix}"
            оканалы = "{channels}"
            игноры = "{ignores}"
            пвмьюте = "{muteusers}"
            пропуск = "{pass}"
            # ru = '{ru}'
            # en = '{en}'
            if info:
                if info == 1:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} ping",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Посмотрите пинг бота и количество шардов.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}ping`",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif info == 2:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} info",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Вы можете прочитать информацию о боте VEGA ⦡#7724.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}info`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}info`\n╰ {get_language(ctx.guild.id,'Покажет информацию о боте VEGA ⦡#7724.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif info == 3:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} stats",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Посмотреть статистику бота VEGA ⦡#7724.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}stats`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}stats`\n╰ {get_language(ctx.guild.id,'Покажет статистику бота VEGA ⦡#7724.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif info == 4:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} server",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Посмотреть информацию о сервере. Количество ролей, каналов, пользователей и т.д.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}server`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Подобные:')}",
                        value=f"`{prefix}serverinfo`\n`{prefix}server-info`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}server`\n╰ {get_language(ctx.guild.id,'Покажет информацию о сервере.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif info == 5:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} userinfo",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Посмотреть информацию о себе или пользователе.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}userinfo {get_language(ctx.guild.id,'[@пользователь]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'[@пользователь]')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'[ID пользователя]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}userinfo`\n╰ {get_language(ctx.guild.id,'Покажет информацию о вас.')}\n\n`{prefix}userinfo {get_language(ctx.guild.id,'[@пользователь]')}`\n╰ {get_language(ctx.guild.id,'Покажет информацию о пользователе.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif info == 6:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} links",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Бот отправит вам в лс ссылку сервера поддержки и документацию.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}links`",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif info == 7:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} wlbots",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Посмотреть или скачать белый список ботов.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}wlbots`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}wlbots`\n╰ {get_language(ctx.guild.id,'Бот отправит вам белый список.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
            elif owner:
                if owner == 1:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} reset",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Команда предназначена для сброса настроек бота.')}\n{get_language(ctx.guild.id,'`prefix` — сброс префикса')}\n{get_language(ctx.guild.id,'`channels` — сброс игнорируемых каналов')}\n{get_language(ctx.guild.id,'`ignores` — сброс игнорируемых ботов')}\n{get_language(ctx.guild.id,'`muteusers` — сброс замьюченных пользователей')}\n{get_language(ctx.guild.id,'`pass` — сброс пропусков')}\n{get_language(ctx.guild.id,'`all` — сброс всех настроек бота')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}pass {все}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{преф}`; `{оканалы}`; `{игноры}`; `{пвмьюте}`; `{пропуск}`; `{все}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}reset all`\n╰ {get_language(ctx.guild.id,'Сбросит все настройки бота.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 2:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} rgive",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Выдать всем пользователям роль. Указанная вами роль не будет выдаваться ботам!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}rgive {get_language(ctx.guild.id,'{all}')} {get_language(ctx.guild.id,'{@роль}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{all}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}rgive all {get_language(ctx.guild.id,'@роль')}`\n╰ {get_language(ctx.guild.id,'Выдать всем роль.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 3:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} rselect",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Забрать у всех пользователей на сервере указанную роль.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}rselect {get_language(ctx.guild.id,'{all}')} {get_language(ctx.guild.id,'{@роль}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{all}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}rselect all {get_language(ctx.guild.id,'@роль')}`\n╰ {get_language(ctx.guild.id,'Забрать у всех роль.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 4:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} antibot",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Включите или отключите антибот. VEGA ⦡#7724 будет выгонять неизвестных ботов и пропускать ботов из белого списка.')}\n\
                        {get_language(ctx.guild.id,'[Открыть белый список](https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots)')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}antibot {get_language(ctx.guild.id,'{on}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}antibot on`\n╰ {get_language(ctx.guild.id,'Антибот включится.')}\n\n`{prefix}antibot off`\n╰ {get_language(ctx.guild.id,'Антибот отключится.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 5:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} antiinvite",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Включите или отключите анти приглашения. Работает на всех каналах, команду ограничить нельзя!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}antiinvite {get_language(ctx.guild.id,'{on}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Подобные:')}",
                        value=f"`{prefix}ai`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}antiinvite on`\n╰ {get_language(ctx.guild.id,'Анти приглашения включится.')}\n\n`{prefix}antiinvite off`\n╰ {get_language(ctx.guild.id,'Анти приглашения отключится.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 6:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} ignore",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Укажите бота. VEGA ⦡ (не) будет игнорировать действия указанных ботов.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}ignore {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{ID бота}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID бота}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}ignore add 795551166393876481`\n╰ {get_language(ctx.guild.id,'VEGA ⦡#7724 будет игнорировать бота.')}\n\n`{prefix}ignore remove 795551166393876481`\n╰ {get_language(ctx.guild.id,'VEGA ⦡#7724 перестанет игнорировать бота.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 7:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} pass",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Выдайте или заберите пропуск у бота. Пропуск можно выдавать только тем ботам, которые не занесены в игнорируемый и белый список. Команда работает только с включенной функцией **AntiBot**!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}pass {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{ID пользователя}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{ID пользователя}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}pass add {get_language(ctx.guild.id,'ID пользователя')}`\n╰ {get_language(ctx.guild.id,'Выдаст пропуск боту.')}\n\n`{prefix}rmute remove {get_language(ctx.guild.id,'ID пользователя')}`\n╰ {get_language(ctx.guild.id,'Заберет пропуск у бота.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 8:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} delchannels",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Бот начнет удалять каналы и | или категории с одинаковым названием.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}delchannels {get_language(ctx.guild.id,'{название канала}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{название канала}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}delchannels {get_language(ctx.guild.id,'Тест')}`\n╰ {get_language(ctx.guild.id,'Удалит одинаковые каналы и | или категории.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 9:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} delroles",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Бот начнет удалять роли с одинаковым названием.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}delroles {get_language(ctx.guild.id,'{@роль}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{название роли}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}delroles {get_language(ctx.guild.id,'@роль')}`\n╰ {get_language(ctx.guild.id,'Удалит одинаковые роли.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
            elif admin:
                if admin == 1:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} log",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Только пользователи с правом Администратора могут указать канал логов для бота!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}log {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{#канал}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{#канал}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID канала}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}log add 824916166400802902`\n╰ {get_language(ctx.guild.id,'Назначит канал логов боту.')}\n\n`{prefix}log remove`\n╰ {get_language(ctx.guild.id,'Удалит канал логов из списка.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 2:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} language",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Только пользователи с правом Администратора могут сменить язык боту!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}language en`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`en` {get_language(ctx.guild.id,'или')} `ru`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}language en`\n╰ {get_language(ctx.guild.id,'Установиться английский язык.')}\n\n`{prefix}language ru`\n╰ {get_language(ctx.guild.id,'Установиться русский язык.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 3:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} channel",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Ограничте бота VEGA ⦡#7724 по каналам. Изначально бот будет отвечать на команды во всех каналах, но если ему указать канал, то он будет отвечать на команды только в указанном канале.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}channel {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{#канал}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{add}` {get_language(ctx.guild.id,'или')} `{remove}` {get_language(ctx.guild.id,'и')} `{канал}` {get_language(ctx.guild.id,'или')} `{канала}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}channel add {get_language(ctx.guild.id,'#канал')}`\n╰ {get_language(ctx.guild.id,'Добавить канал в список.')}\n\n`{prefix}channel remove {get_language(ctx.guild.id,'#канал')}`\n╰ {get_language(ctx.guild.id,'Удалить канал из списка.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 4:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} rmute",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Только пользователи с правом Администратора могут указать роль мьюта для бота!')}\n\
                        {get_language(ctx.guild.id,'Если роль мьюта была удалена, ты вы можете указать ее заново.')}\n{get_language(ctx.guild.id,'Роль мьюта не будет настраиваться ботом!')} {get_language(ctx.guild.id,'Вы сами должны настроить роль мьюта!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}rmute {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{@роль}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}rmute add @Muted`\n╰ {get_language(ctx.guild.id,'Назначит роль мьюта боту.')}\n\n`{prefix}rmute remove @Muted`\n╰ {get_language(ctx.guild.id,'Удалит роль мьюта из списка.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 5:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} settings",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Вы можете посмотреть все настройки бота.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}settings`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Подобные:')}",
                        value=f"`{prefix}stg`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}settings`\n╰ {get_language(ctx.guild.id,'Посмотреть настройки.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 6:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} list",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Посмотреть список ограниченных каналов, игнорируемых ботов, пропусков или количество ботов в белом списке.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}list {get_language(ctx.guild.id,'{channels}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{channels}')}`; `{get_language(ctx.guild.id,'{ignores}')}`; `{get_language(ctx.guild.id,'{pass}')}`; `{get_language(ctx.guild.id,'{wl}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}list channels`\n╰ {get_language(ctx.guild.id,'Список ограниченных каналов.')}\n\n`{prefix}list ignores`\n╰ {get_language(ctx.guild.id,'Список игнорируемых ботов.')}\n\n`{prefix}list pass`\n╰ {get_language(ctx.guild.id,'Боты, у которых есть пропуска на сервер.')}\n\n`{prefix}list wl`\n╰ {get_language(ctx.guild.id,'Белый список ботов.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 7:
                    # текст = '{текст}'
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} echo",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Только Администраторы могут писать от лица бота.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}echo {get_language(ctx.guild.id,'{текст}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{текст}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}echo` {get_language(ctx.guild.id,'Это тестовое сообщение!')}\n╰ {get_language(ctx.guild.id,'Отправит сообщение от лица бота.')}",
                        inline=False,
                    )
                    embed.set_image(
                        url=f"{get_language(ctx.guild.id,'https://media.discordapp.net/attachments/713751423128698950/859417527594254346/messages_from_VEGA__line_RU.png')}"
                    )
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 8:
                    # текст = '{текст}'
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} emb",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Только Администраторы могут писать эмбед от лица бота.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}emb {get_language(ctx.guild.id,'{текст}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{текст}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}emb` {get_language(ctx.guild.id,'Это тестовое сообщение!')}\n╰ {get_language(ctx.guild.id,'Отправит сообщение эмбедом от лица бота.')}",
                        inline=False,
                    )
                    embed.set_image(
                        url=f"{get_language(ctx.guild.id,'https://media.discordapp.net/attachments/713751423128698950/859417490324455444/emb_messages_from_VEGA__line_RU.png')}"
                    )
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 9:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} slowmode",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Установите медленный режим в канале. Максимальное число в секундах 31600, минимальное 1. Число 0 сбросит медленный режим в канале.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}slowmode {get_language(ctx.guild.id,'{число}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{число}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}slowmode 2`\n╰ {get_language(ctx.guild.id,'Бот установит медленный режим в канале.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
            elif moder:
                if moder == 1:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} checkwl",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Только пользователи с правом Администратора или Управления сервером, могут проверить наличие одного или всех ботов из сервера в белом списке!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Администратор')}\n{get_language(ctx.guild.id,'Управлять сервером')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}checkwl {get_language(ctx.guild.id,'{ID бота}')}` {get_language(ctx.guild.id,'или')} `{prefix}checkwl {get_language(ctx.guild.id,'{all}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID бота}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{all}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}checkwl 767994849600602143`\n╰ {get_language(ctx.guild.id,'Проверка бота в белом списке.')}\n\n`{prefix}checkwl all`\n╰ {get_language(ctx.guild.id,'Проверка ботов на сервере в списках.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif moder == 2:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} ban",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Забаньте нарушителя. Причина необязательна!')}\n{get_language(ctx.guild.id,'Бот забанит пользователя и удалит последние сообщения.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Банить пользователей')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}ban {get_language(ctx.guild.id,'{@пользователь}')} {get_language(ctx.guild.id,'[причина]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}ban {get_language(ctx.guild.id,'@пользователь')} {get_language(ctx.guild.id,'Спам приглашениями.')}`\n╰ {get_language(ctx.guild.id,'Бот забанит нарушителя.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif moder == 3:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} unban",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Разбаньте нарушителя.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Банить пользователей')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}unban {get_language(ctx.guild.id,'{@пользователь}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}unban {get_language(ctx.guild.id,'@пользователь')}`\n╰ {get_language(ctx.guild.id,'Бот разбанит нарушителя.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif moder == 4:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} kick",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Кикните нарушителя. Причина необязательна!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Кикать пользователей')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}kick {get_language(ctx.guild.id,'{@пользователь}')} {get_language(ctx.guild.id,'[причина]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}kick {get_language(ctx.guild.id,'@пользователь')} {get_language(ctx.guild.id,'Спам приглашениями.')}`\n╰ {get_language(ctx.guild.id,'Бот выгонит нарушителя из сервера.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif moder == 5:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} clear",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Очистите чат и сообщения пользователей на вашем сервере. Минимальное количество очистки сообщений 1, а максимальное 200.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Управлять сообщениями')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}clear {get_language(ctx.guild.id,'[@пользователь]')} {get_language(ctx.guild.id,'{число}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'[@пользователь]')}` {get_language(ctx.guild.id,'и')} | {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{число}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Подобные:')}",
                        value=f"`{prefix}purge`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}clear 12`\n╰ {get_language(ctx.guild.id,'Бот очистит сообщения в чате.')}\n\n`{prefix}clear {get_language(ctx.guild.id,'@пользователь')} 12`\n╰ {get_language(ctx.guild.id,'Бот очистит сообщения пользователя в чате.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif moder == 6:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} uclear",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Очистите сообщения пользователя. Бот очистит сообщения написанные пользователем за последнюю неделю.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Управлять сообщениями')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}uclear {get_language(ctx.guild.id,'{@пользователь}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{@пользователь}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}uclear {get_language(ctx.guild.id,'@пользователь')}`\n╰ {get_language(ctx.guild.id,'Бот очистит последние сообщения пользоватея.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif moder == 7:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} rolen",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Посмотреть количество пользователей с данной ролью.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Управлять ролями')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}rolen {get_language(ctx.guild.id,'{@роль}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}rolen {роль}`\n╰ {get_language(ctx.guild.id,'Покажет количество пользователей с ролью.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif moder == 8:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} mute",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Замьютьте нарушителя. Причина не обязательна.')}\n{get_language(ctx.guild.id,'Роль мьюта не будет настраиваться ботом!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Журнал аудита')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}mute {get_language(ctx.guild.id,'{@пользователь}')} {get_language(ctx.guild.id,'[причина]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}mute {get_language(ctx.guild.id,'@пользователь')} {get_language(ctx.guild.id,'Спам сообщениями.')}`\n╰ {get_language(ctx.guild.id,'Бот выдаст нарушителю роль мьюта.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif moder == 9:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} unmute",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Забрать у нарушителя роль мьюта.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Журнал аудита')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}unmute {get_language(ctx.guild.id,'{@пользователь}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}unmute {get_language(ctx.guild.id,'@пользователь')}`\n╰ {get_language(ctx.guild.id,'Бот заберет у нарушителя роль мьюта.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
            elif fun:
                if fun == 1:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} 8ball",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Задайте вопрос шару и узнайте правду.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}8ball {get_language(ctx.guild.id,'{текст}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{текст}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}8ball {get_language(ctx.guild.id,'Завтра будет ясная погода?')}`\n╰ {get_language(ctx.guild.id,'Бот ответит на ваш вопрос.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif fun == 2:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} avatar",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Посмотрите и скачайте аватар пользователя.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}avatar {get_language(ctx.guild.id,'[@пользователь]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'[@пользователь]')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'[ID пользователя]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Подобные:')}",
                        value=f"`{prefix}ava`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}avatar`\n╰ {get_language(ctx.guild.id,'Покажет ваш аватар.')}\n\n`{prefix}avatar {get_language(ctx.guild.id,'[@пользователь]')}`\n╰ {get_language(ctx.guild.id,'Покажет аватар пользователя.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif fun == 3:
                    # эмодзи = '{эмодзи}'
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} emoji",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Вы можете осмотреть и скачать эмодзи.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}emoji {get_language(ctx.guild.id,'{эмодзи}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{эмодзи}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"{prefix}emoji <:python:826158844555427891>\n╰ {get_language(ctx.guild.id,'Посмотреть эмодзи.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif fun == 4:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} random",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Если хотите выбрать случайное число, то воспользуйтесь данной командой.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}random {a} {b}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{a}` {get_language(ctx.guild.id,'и')} `{b}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Подобные:')}",
                        value=f"`{prefix}r`\n`{prefix}rand`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}random 5 10`\n╰ {get_language(ctx.guild.id,'Бот выберет рандомное число.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif fun == 5:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} math",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Калькулятор для решения простых примеров.')}\n{get_language(ctx.guild.id,'Используются знаки')} `() + - / *`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}math {get_language(ctx.guild.id,'{пример}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{пример}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Подобные:')}",
                        value=f"`{prefix}calculate`\n`{prefix}calc`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}math 5*5`\n╰ {get_language(ctx.guild.id,'Бот решит пример за вас.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vegabot.xyz/vegabot",
                        url="https://vegabot.xyz/vegabot/",
                        icon_url=client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}",
                    description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{prefix}help Info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{prefix}help Owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{prefix}help Admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{prefix}help Moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{prefix}help Fun` — {get_language(ctx.guild.id, 'команды веселья')}.",
                    color=0xE21E1E,
                )
                embed.set_author(
                    name=f"vegabot.xyz/vegabot",
                    url="https://vegabot.xyz/vegabot/",
                    icon_url=client.get_user(795551166393876481).avatar.replace(
                        size=1024, format="png"
                    ),
                )
                embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                embed.set_footer(
                    icon_url=client.get_user(351020816466575372).avatar.replace(
                        size=1024
                    ),
                    text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                )
                await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}",
                color=0xFCC21B,
            )
            await ctx.send(embed=embed, ephemeral=True)


"""            
            elif option.lower() in ["help"]:
                embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} help", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Показывает справку о всех командах.')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}help {get_language(ctx.guild.id,'[команда]')}`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}h`', inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}help`\n╰ {get_language(ctx.guild.id,'Список всех команд.')}\n\n\
                    `{prefix}help [emoji]`\n╰ {get_language(ctx.guild.id,'Информация о команде.')}", inline=False)
                embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                await inter.reply(embed=embed, components=[row_i])
            elif option.lower() in ["language"]:
                embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} language", color=0xd81911)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Установите язык для бота на вашем сервере.')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}language {get_language(ctx.guild.id,'{ru}')}`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{ru}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{en}')}`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}lang`', inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}language ru`\n╰ {get_language(ctx.guild.id,'Установить русский язык для бота.')}\n\n`{prefix}language en`\n╰ {get_language(ctx.guild.id,'Установить английский язык для бота.')}", inline=False)
                embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                await inter.reply(embed=embed, components=[row_i])
            elif option.lower() in ["antimsg"]:
                embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} antimsg", color=0xd81911)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Включите или отключите автоматическое удаление сообщений оффлайн ботов. VEGA ⦡#7724 будет удалять сообщения неизвестных ботов, которые находятся не в сети.')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}antimsg {get_language(ctx.guild.id,'{on}')}`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}antimsg on`\n╰ {get_language(ctx.guild.id,'Антисообщения включатся.')}\n\n`{prefix}antimsg off`\n╰ {get_language(ctx.guild.id,'Антисообщения отключатся.')}", inline=False)
                embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                await inter.reply(embed=embed, components=[row_i])
"""

"""
                elif option.lower() in ["*info"]:
                    embed = discord.Embed(title=f"{get_language(ctx.guild.id, '❓ Группа: Информация')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}ping` — {get_language(ctx.guild.id, 'пинг бота и состояние шардов.')}\n`{prefix}info` — {get_language(ctx.guild.id,'информация о боте.')}\n`{prefix}stats` — {get_language(ctx.guild.id,'статистика бота.')}\n`{prefix}server` — {get_language(ctx.guild.id,'информация о сервере.')}\n`{prefix}links` — {get_language(ctx.guild.id,'полезные ссылки.')}\n`{prefix}wlbots` — {get_language(ctx.guild.id,'белый список ботов.')}", inline=False)
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                    await inter.reply(embed=embed, components=[row_i])
                elif option.lower() in ["*fun"]:
                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Веселье')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}8ball` — {get_language(ctx.guild.id,'задать вопрос шару.')}\n`{prefix}avatar` — {get_language(ctx.guild.id,'посмотреть аватар пользователя.')}\n`{prefix}emoji` — {get_language(ctx.guild.id,'посмотреть эмодзи.')}\n`{prefix}random` — {get_language(ctx.guild.id,'рандомное число, от и до.')}\n`{prefix}math` — {get_language(ctx.guild.id,'обычный калькулятор.')}", inline=False)
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                    await inter.reply(embed=embed, components=[row_i])
                elif option.lower() in ["*owner"]:
                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Владельца')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}reset` — {get_language(ctx.guild.id,'сброс настроек бота.')}\n`{prefix}rgive` — {get_language(ctx.guild.id,'выдать всем роль.')}\n`{prefix}rselect` — {get_language(ctx.guild.id,'забрать у всех роль.')}\n`{prefix}antibot` — {get_language(ctx.guild.id,'функция Антибот.')}\n`{prefix}antiinvite` — {get_language(ctx.guild.id,'функция Анти приглашения.')}\n`{prefix}ignore` — {get_language(ctx.guild.id,'игнорировать ботов.')}\n`{prefix}pass` — {get_language(ctx.guild.id,'пропуск для бота.')}\n`{prefix}delchannels` — {get_language(ctx.guild.id,'удалить спам каналы | категории.')}\n`{prefix}delroles` — {get_language(ctx.guild.id,'удалить спам роли.')}", inline=False)
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                    await inter.reply(embed=embed, components=[row_i])
                elif option.lower() in ["*admin"]:
                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Администратора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}prefix` — {get_language(ctx.guild.id,'сменить префикс боту.')}\n`{prefix}log` — {get_language(ctx.guild.id,'указать канал логов.')}\n`{prefix}channel` — {get_language(ctx.guild.id,'ограничить команды бота по каналам.')}\n`{prefix}rmute` — {get_language(ctx.guild.id,'указать роль Мьюта.')}\n`{prefix}settings` — {get_language(ctx.guild.id,'настройки бота.')}\n`{prefix}list` — {get_language(ctx.guild.id,'существующие списки.')}\n`{prefix}echo` — {get_language(ctx.guild.id,'текст от лица бота.')}\n`{prefix}emb` — {get_language(ctx.guild.id,'текст в панели от лица бота.')}\n`{prefix}slowmode` — {get_language(ctx.guild.id,'установить медленный режим в канале.')}", inline=False)
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                    await inter.reply(embed=embed, components=[row_i])
                elif option.lower() in ["*moder"]:
                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Модератора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}checkwl` — {get_language(ctx.guild.id,'проверить бота в белом списке.')}\n`{prefix}ban` — {get_language(ctx.guild.id,'забанить пользователя.')}\n`{prefix}unban` — {get_language(ctx.guild.id,'разбанить пользователя.')}\n`{prefix}kick` — {get_language(ctx.guild.id,'кикнуть пользователя.')}\n`{prefix}clear` — {get_language(ctx.guild.id,'очистить чат.')}\n`{prefix}uclear` — {get_language(ctx.guild.id,'очистить сообщения указанного пользователя.')}\n`{prefix}rolen` — {get_language(ctx.guild.id,'посмотреть кол-во пользователей с ролью.')}\n`{prefix}user` — {get_language(ctx.guild.id,'информация о пользователе.')}\n`{prefix}mute` — {get_language(ctx.guild.id,'замьютить пользователя.')}\n`{prefix}unmute` — {get_language(ctx.guild.id,'размьютить пользователя.')}", inline=False)
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                    await inter.reply(embed=embed, components=[row_i])
                else:
                    ctx.command.reset_cooldown(ctx)
            else:"""

"""
            global HELP_MENUS
            # Достаём последнее хелп сообщение пользователя
            last_msg = HELP_MENUS.get(ctx.author.id)
            if last_msg is not None:
                # Удаляем его кнопки
                try:
                    await last_msg.edit_original_message(view=None)
                except:
                    pass

            pre = prefix
            embed = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
            embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
            embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
"""

"""         row = ActionRow(Button(style=ButtonStyle.blurple, emoji="<:info:860380081268588545>", custom_id = '❓'), Button(style=ButtonStyle.blurple, emoji="<:owner:860380081594564688>", custom_id = '👑'),
                Button(style=ButtonStyle.blurple, emoji="<:admin:860380081536761886>", custom_id = '⚙️'), Button(style=ButtonStyle.blurple, emoji="<:moder:860380081627856906>", custom_id = '🛠'), Button(style=ButtonStyle.blurple, emoji="<:fun:860380081637031936>", custom_id = '🎉'))

            back = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vegabot.xyz/vegabot"))
            back1 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад1'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vegabot.xyz/vegabot"))                
            back2 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад2'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vegabot.xyz/vegabot"))                
            back3 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад3'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vegabot.xyz/vegabot"))                
            back4 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад4'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vegabot.xyz/vegabot"))                
            back5 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад5'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vegabot.xyz/vegabot"))                
"""

# msg = await ctx.message.reply(embed=embed, components=[row, row_1])
# Запоминаешь сообщение чтобы если чё удалить кнопки в нём
# HELP_MENUS[ctx.author.id] = msg

"""         helpmenuinfo = SelectMenu(custom_id="menuhelpi", placeholder=f"{get_language(ctx.guild.id, 'Информация о команде')}", max_values=1, options=[
                SelectOption(label=f"{prefix}ping", value="info1"),
                SelectOption(label=f"{prefix}info", value="info2"),
                SelectOption(label=f"{prefix}stats", value="info3"),
                SelectOption(label=f"{prefix}server", value="info4"),
                SelectOption(label=f"{prefix}links", value="info5"),
                SelectOption(label=f"{prefix}wlbots", value="info6")
                ])
            helpmenuowner = SelectMenu(custom_id="menuhelpo", placeholder=f"{get_language(ctx.guild.id, 'Информация о команде')}", max_values=1, options=[
                SelectOption(label=f"{prefix}reset", value="owner1"),
                SelectOption(label=f"{prefix}rgive", value="owner2"),
                SelectOption(label=f"{prefix}rselect", value="owner3"),
                SelectOption(label=f"{prefix}antibot", value="owner4"),
                SelectOption(label=f"{prefix}antimsg", value="owner10"),
                SelectOption(label=f"{prefix}antiinvite", value="owner5"),
                SelectOption(label=f"{prefix}ignore", value="owner6"),
                SelectOption(label=f"{prefix}pass", value="owner7"),
                SelectOption(label=f"{prefix}delchannels", value="owner8"),
                SelectOption(label=f"{prefix}delroles", value="owner9")
                ])
            helpmenuadmin = SelectMenu(custom_id="menuhelpa", placeholder=f"{get_language(ctx.guild.id, 'Информация о команде')}", max_values=1, options=[
                SelectOption(label=f"{prefix}log", value="admin2"),
                SelectOption(label=f"{prefix}channel", value="admin3"),
                SelectOption(label=f"{prefix}rmute", value="admin4"),
                SelectOption(label=f"{prefix}settings", value="admin5"),
                SelectOption(label=f"{prefix}list", value="admin6"),
                SelectOption(label=f"{prefix}echo", value="admin7"),
                SelectOption(label=f"{prefix}emb", value="admin8"),
                SelectOption(label=f"{prefix}slowmode", value="admin9")
                ])
            helpmenumoder = SelectMenu(custom_id="menuhelpm", placeholder=f"{get_language(ctx.guild.id, 'Информация о команде')}", max_values=1, options=[
                SelectOption(label=f"{prefix}checkwl", value="moder1"),
                SelectOption(label=f"{prefix}ban", value="moder2"),
                SelectOption(label=f"{prefix}unban", value="moder3"),
                SelectOption(label=f"{prefix}kick", value="moder4"),
                SelectOption(label=f"{prefix}clear", value="moder5"),
                SelectOption(label=f"{prefix}uclear", value="moder6"),
                SelectOption(label=f"{prefix}rolen", value="moder7"),
                SelectOption(label=f"{prefix}user", value="moder8"),
                SelectOption(label=f"{prefix}mute", value="moder9"),
                SelectOption(label=f"{prefix}unmute", value="moder10")
                ])
            helpmenufun = SelectMenu(custom_id="menuhelpf", placeholder=f"{get_language(ctx.guild.id, 'Информация о команде')}", max_values=1, options=[
                SelectOption(label=f"{prefix}8ball", value="fun1"),
                SelectOption(label=f"{prefix}avatar", value="fun2"),
                SelectOption(label=f"{prefix}emoji", value="fun3"),
                SelectOption(label=f"{prefix}random", value="fun4"),
                SelectOption(label=f"{prefix}math", value="fun5")
                ])
"""
"""
            menuhelp_view = menuhelpview(timeout=60)
            msg = await ctx.send(embed=embed, view=[menuhelp_view, links])
            await menuhelp_view.wait()
            try:await ctx.edit_original_message(view=links)
            except:pass

            # Запоминаешь сообщение чтобы если чё удалить кнопки в нём
            HELP_MENUS[ctx.author.id] = msg

            while True:            
                helpvalue = intermenu.select_menu.selected_options[0].value

                # Если тыкнул не тот чел, скажи ему об этом
                if intermenu.author != ctx.author:
                    await intermenu.reply(f"{get_language(ctx.guild.id, 'Этим меню управляете не вы!')}", ephemeral=True)
                else:
                    on = '{on}'
                    off = '{off}'
                    add ='{add}'
                    remove = '{remove}'
                    эмодзи = '{эмодзи}'
                    число = '{число}'
                    текст = '{текст}'
                    символы = '{символы}'
                    пример = '{пример}'
                    причина = '{причина}'
                    a = '{a}'
                    b = '{b}'
                    название_роли = '{название роли}'
                    роль = '{@роль}'
                    роли = '{ID роли}'
                    бота = '{ID бота}'
                    всем = '{all}'
                    пользователь = '{@пользователь}'
                    пользователя = '{ID пользователя}'
                    канал = '{#канал}'
                    канала = '{ID канала}'
                    channels = '{channels}'
                    ignores = '{ignores}'
                    каналов = '{каналов}'
                    игнора = '{игнора}'
                    название_канала = '{название канала}'
                    обязательный_параметр = '{**_обязательный параметр_**}'
                    wl = '{wl}'
                    бс = '{бс}'
                    все = '{all}'
                    преф = '{prefix}'
                    оканалы = '{channels}'
                    игноры = '{ignores}'
                    пвмьюте = '{muteusers}'
                    пропуск = '{pass}'
                    #ru = '{ru}'
                    #en = '{en}'
                    if helpvalue == "❓":
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id, '❓ Группа: Информация')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                            ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}ping` — {get_language(ctx.guild.id, 'пинг бота и состояние шардов.')}\n`{pre}info` — {get_language(ctx.guild.id, 'информация о боте.')}\n`{pre}stats` — {get_language(ctx.guild.id, 'статистика бота.')}\n`{pre}server` — {get_language(ctx.guild.id, 'информация о сервере.')}\n`{pre}links` — {get_language(ctx.guild.id, 'полезные ссылки.')}\n`{pre}wlbots` — {get_language(ctx.guild.id, 'белый список ботов.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                        await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuinfo, back])
                        
                        #Меню информации о команде helpmenuinfo
                        def check(inter):
                            return inter.message.id == msg.id

                        while True:
                            try:
                                inter = await client.multiple_wait_for(
                                    {
                                        "dropdown": check,
                                        "button_click": check
                                    },
                                    timeout=60
                                )
                            except asyncio.TimeoutError:
                                await msg.edit(components=[row_1])
                                return

                            if inter.author != ctx.author:
                                # Не тот автор
                                await inter.reply(f"{get_language(ctx.guild.id, 'Этим меню управляете не вы!')}", ephemeral=True)
                            elif inter.button:
                                # Была нажата кнопка
                                button_id = inter.button.custom_id
                                if button_id == "Назад1":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id, '❓ Группа: Информация')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}ping` — {get_language(ctx.guild.id, 'пинг бота и состояние шардов.')}\n`{pre}info` — {get_language(ctx.guild.id, 'информация о боте.')}\n`{pre}stats` — {get_language(ctx.guild.id, 'статистика бота.')}\n`{pre}server` — {get_language(ctx.guild.id, 'информация о сервере.')}\n`{pre}links` — {get_language(ctx.guild.id, 'полезные ссылки.')}\n`{pre}wlbots` — {get_language(ctx.guild.id, 'белый список ботов.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuinfo, back])
                                elif button_id == "Назад":
                                    embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                    embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed1.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed1, components=[helpmenu, row_1])
                                    break
                            elif inter.select_menu:
                                # Было нажато меню
                                helpvaluei = inter.select_menu.selected_options[0].value
                                if helpvaluei == "info1":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} ping", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотрите пинг бота и количество шардов.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}ping`", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                elif helpvaluei == "info2":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} info", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Вы можете прочитать информацию о боте VEGA ⦡#7724.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}info`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}info`\n╰ {get_language(ctx.guild.id,'Покажет информацию о боте VEGA ⦡#7724.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                elif helpvaluei == "info3":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} stats", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value='Посмотреть статистику бота VEGA ⦡#7724.', inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}stats`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}stats`\n╰ Покажет статистику бота VEGA ⦡#7724.", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                elif helpvaluei == "info4":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} server", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотреть информацию о сервере. Количество ролей, каналов, пользователей и т.д.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}server`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}serverinfo`\n`{prefix}server-info`', inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}server`\n╰ {get_language(ctx.guild.id,'Покажет информацию о сервере.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                elif helpvaluei == "info5":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} links", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Бот отправит вам в лс ссылку сервера поддержки и документацию.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}links`", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                elif helpvaluei == "info6":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} wlbots", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотреть или скачать белый список ботов.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}wlbots`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}wlbots`\n╰ {get_language(ctx.guild.id,'Бот отправит вам белый список.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                
                    elif helpvalue == "👑":
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Владельца')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                            ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}reset` — {get_language(ctx.guild.id,'сброс настроек бота.')}\n`{pre}rgive` — {get_language(ctx.guild.id,'выдать всем роль.')}\n`{pre}rselect` — {get_language(ctx.guild.id,'забрать у всех роль.')}\n`{pre}antibot` — {get_language(ctx.guild.id,'функция Антибот.')}\n`{pre}antimsg` — {get_language(ctx.guild.id,'функция Антисообщения.')}\n`{pre}antiinvite` — {get_language(ctx.guild.id,'функция Анти приглашения.')}\n`{pre}ignore` — {get_language(ctx.guild.id,'игнорировать ботов.')}\n`{pre}pass` — {get_language(ctx.guild.id,'пропуск для бота.')}\n`{pre}delchannels` — {get_language(ctx.guild.id,'удалить спам каналы | категории.')}\n`{pre}delroles` — {get_language(ctx.guild.id,'удалить спам роли.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                        await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuowner, back])


                        def check(inter):
                            return inter.message.id == msg.id

                        while True:
                            try:
                                inter = await client.multiple_wait_for(
                                    {
                                        "dropdown": check,
                                        "button_click": check
                                    },
                                    timeout=60
                                )
                            except asyncio.TimeoutError:
                                await msg.edit(components=[row_1])
                                return

                            if inter.author != ctx.author:
                                # Не тот автор
                                await inter.reply(f"{get_language(ctx.guild.id, 'Этим меню управляете не вы!')}", ephemeral=True)
                            elif inter.button:
                                # Была нажата кнопка
                                button_id = inter.button.custom_id
                                if button_id == "Назад2":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Владельца')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}reset` — {get_language(ctx.guild.id,'сброс настроек бота.')}\n`{pre}rgive` — {get_language(ctx.guild.id,'выдать всем роль.')}\n`{pre}rselect` — {get_language(ctx.guild.id,'забрать у всех роль.')}\n`{pre}antibot` — {get_language(ctx.guild.id,'функция Антибот.')}\n`{pre}antimsg` — {get_language(ctx.guild.id,'функция Антисообщения.')}\n`{pre}antiinvite` — {get_language(ctx.guild.id,'функция Анти приглашения.')}\n`{pre}ignore` — {get_language(ctx.guild.id,'игнорировать ботов.')}\n`{pre}pass` — {get_language(ctx.guild.id,'пропуск для бота.')}\n`{pre}delchannels` — {get_language(ctx.guild.id,'удалить спам каналы | категории.')}\n`{pre}delroles` — {get_language(ctx.guild.id,'удалить спам роли.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuowner, back])
                                elif button_id == "Назад":
                                    embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                    embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed1.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed1, components=[helpmenu, row_1])
                                    break
                            elif inter.select_menu:
                                # Было нажато меню
                                helpvalueo = inter.select_menu.selected_options[0].value
                                if helpvalueo == "owner1":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} reset", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Команда предназначена для сброса настроек бота.')}\n{get_language(ctx.guild.id,'`prefix` — сброс префикса')}\n{get_language(ctx.guild.id,'`channels` — сброс игнорируемых каналов')}\n{get_language(ctx.guild.id,'`ignores` — сброс игнорируемых ботов')}\n{get_language(ctx.guild.id,'`muteusers` — сброс замьюченных пользователей')}\n{get_language(ctx.guild.id,'`pass` — сброс пропусков')}\n{get_language(ctx.guild.id,'`all` — сброс всех настроек бота')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}pass {все}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{преф}`; `{оканалы}`; `{игноры}`; `{пвмьюте}`; `{пропуск}`; `{все}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}reset all`\n╰ {get_language(ctx.guild.id,'Сбросит все настройки бота.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                elif helpvalueo == "owner2":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} rgive", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Выдать всем пользователям роль. Указанная вами роль не будет выдаваться ботам!')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}rgive {get_language(ctx.guild.id,'{all}')} {get_language(ctx.guild.id,'{@роль}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{all}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}rgive all {get_language(ctx.guild.id,'@роль')}`\n╰ {get_language(ctx.guild.id,'Выдать всем роль.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                elif helpvalueo == "owner3":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} rselect", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Забрать у всех пользователей на сервере указанную роль.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}rselect {get_language(ctx.guild.id,'{all}')} {get_language(ctx.guild.id,'{@роль}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{all}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}rselect all {get_language(ctx.guild.id,'@роль')}`\n╰ {get_language(ctx.guild.id,'Забрать у всех роль.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                elif helpvalueo == "owner4":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} antibot", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Включите или отключите антибот. VEGA ⦡#7724 будет выгонять неизвестных ботов и пропускать ботов из белого списка.')}\n\
                                        {get_language(ctx.guild.id,'[Открыть белый список](https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots)')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}antibot {get_language(ctx.guild.id,'{on}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}antibot on`\n╰ {get_language(ctx.guild.id,'Антибот включится.')}\n\n`{prefix}antibot off`\n╰ {get_language(ctx.guild.id,'Антибот отключится.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                elif helpvalueo == "owner5":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} antiinvite", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Включите или отключите анти приглашения. Работает на всех каналах, команду ограничить нельзя!')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}antiinvite {get_language(ctx.guild.id,'{on}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}ai`', inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}antiinvite on`\n╰ {get_language(ctx.guild.id,'Анти приглашения включится.')}\n\n`{prefix}antiinvite off`\n╰ {get_language(ctx.guild.id,'Анти приглашения отключится.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                elif helpvalueo == "owner6":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} ignore", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Укажите бота. VEGA ⦡ (не) будет игнорировать действия указанных ботов.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}ignore {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{ID бота}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID бота}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}ignore add 795551166393876481`\n╰ {get_language(ctx.guild.id,'VEGA ⦡#7724 будет игнорировать бота.')}\n\n`{prefix}ignore remove 795551166393876481`\n╰ {get_language(ctx.guild.id,'VEGA ⦡#7724 перестанет игнорировать бота.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                elif helpvalueo == "owner7":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} pass", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Выдайте или заберите пропуск у бота. Пропуск можно выдавать только тем ботам, которые не занесены в игнорируемый и белый список. Команда работает только с включенной функцией **AntiBot**!')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}pass {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{ID пользователя}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{ID пользователя}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}pass add {get_language(ctx.guild.id,'ID пользователя')}`\n╰ {get_language(ctx.guild.id,'Выдаст пропуск боту.')}\n\n`{prefix}rmute remove {get_language(ctx.guild.id,'ID пользователя')}`\n╰ {get_language(ctx.guild.id,'Заберет пропуск у бота.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                elif helpvalueo == "owner8":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} delchannels", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Бот начнет удалять каналы и | или категории с одинаковым названием.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}delchannels {get_language(ctx.guild.id,'{название канала}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{название канала}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}delchannels {get_language(ctx.guild.id,'Тест')}`\n╰ {get_language(ctx.guild.id,'Удалит одинаковые каналы и | или категории.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                elif helpvalueo == "owner9":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} delroles", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Бот начнет удалять роли с одинаковым названием.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}delroles {get_language(ctx.guild.id,'{@роль}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{название роли}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}delroles {get_language(ctx.guild.id,'@роль')}`\n╰ {get_language(ctx.guild.id,'Удалит одинаковые роли.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                elif helpvalueo == "owner10":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} antimsg", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Включите или отключите автоматическое удаление сообщений оффлайн ботов. VEGA ⦡#7724 будет удалять сообщения неизвестных ботов, которые находятся не в сети.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}antimsg {get_language(ctx.guild.id,'{on}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}antimsg on`\n╰ {get_language(ctx.guild.id,'Антисообщения включатся.')}\n\n`{prefix}antimsg off`\n╰ {get_language(ctx.guild.id,'Антисообщения отключатся.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
        
                    elif helpvalue == "⚙️":
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Администратора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                            ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}log` — {get_language(ctx.guild.id,'указать канал логов.')}\n`{pre}channel` — {get_language(ctx.guild.id,'ограничить команды бота по каналам.')}\n`{pre}rmute` — {get_language(ctx.guild.id,'указать роль Мьюта.')}\n`{pre}settings` — {get_language(ctx.guild.id,'настройки бота.')}\n`{pre}list` — {get_language(ctx.guild.id,'существующие списки.')}\n`{pre}echo` — {get_language(ctx.guild.id,'текст от лица бота.')}\n`{pre}emb` — {get_language(ctx.guild.id,'текст в панели от лица бота.')}\n`{pre}slowmode` — {get_language(ctx.guild.id,'установить медленный режим в канале.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                        await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuadmin, back])
                        def check(inter):
                            return inter.message.id == msg.id
                        while True:
                            try:
                                inter = await client.multiple_wait_for(
                                    {
                                        "dropdown": check,
                                        "button_click": check
                                    },
                                    timeout=60
                                )
                            except asyncio.TimeoutError:
                                await msg.edit(components=[row_1])
                                return
                            if inter.author != ctx.author:
                                # Не тот автор
                                await inter.reply(f"{get_language(ctx.guild.id, 'Этим меню управляете не вы!')}", ephemeral=True)
                            elif inter.button:
                                # Была нажата кнопка
                                button_id = inter.button.custom_id
                                if button_id == "Назад3":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Администратора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}log` — {get_language(ctx.guild.id,'указать канал логов.')}\n`{pre}channel` — {get_language(ctx.guild.id,'ограничить команды бота по каналам.')}\n`{pre}rmute` — {get_language(ctx.guild.id,'указать роль Мьюта.')}\n`{pre}settings` — {get_language(ctx.guild.id,'настройки бота.')}\n`{pre}list` — {get_language(ctx.guild.id,'существующие списки.')}\n`{pre}echo` — {get_language(ctx.guild.id,'текст от лица бота.')}\n`{pre}emb` — {get_language(ctx.guild.id,'текст в панели от лица бота.')}\n`{pre}slowmode` — {get_language(ctx.guild.id,'установить медленный режим в канале.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuadmin, back])
                                elif button_id == "Назад":
                                    embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                    embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed1.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed1, components=[helpmenu, row_1])
                                    break
                            elif inter.select_menu:
                                # Было нажато меню
                                helpvaluea = inter.select_menu.selected_options[0].value
                                if helpvaluea == "admin1":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} prefix", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Установите собственный префикс боту на своем сервере.')}\n{get_language(ctx.guild.id,'Запрещено использование символов  ` * ~ _ > |')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}prefix {get_language(ctx.guild.id,'{символы}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{символы}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}prefix !`\n╰ {get_language(ctx.guild.id,'Вы установите префикс боту.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                elif helpvaluea == "admin2":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} log", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Только пользователи с правом Администратора могут указать канал логов для бота!')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}log {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{#канал}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{#канал}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID канала}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}log add 824916166400802902`\n╰ {get_language(ctx.guild.id,'Назначит канал логов боту.')}\n\n`{prefix}log remove`\n╰ {get_language(ctx.guild.id,'Удалит канал логов из списка.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                elif helpvaluea == "admin3":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} channel", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Ограничте бота VEGA ⦡#7724 по каналам. Изначально бот будет отвечать на команды во всех каналах, но если ему указать канал, то он будет отвечать на команды только в указанном канале.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}channel {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{#канал}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{add}` {get_language(ctx.guild.id,'или')} `{remove}` {get_language(ctx.guild.id,'и')} `{канал}` {get_language(ctx.guild.id,'или')} `{канала}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}channel add {get_language(ctx.guild.id,'#канал')}`\n╰ {get_language(ctx.guild.id,'Добавить канал в список.')}\n\n`{prefix}channel remove {get_language(ctx.guild.id,'#канал')}`\n╰ {get_language(ctx.guild.id,'Удалить канал из списка.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                elif helpvaluea == "admin4":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} rmute", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Только пользователи с правом Администратора могут указать роль мьюта для бота!')}\n\
                                        {get_language(ctx.guild.id,'Если роль мьюта была удалена, ты вы можете указать ее заново.')}\n{get_language(ctx.guild.id,'Роль мьюта не будет настраиваться ботом!')} {get_language(ctx.guild.id,'Вы сами должны настроить роль мьюта!')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}rmute {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{@роль}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}rmute add @Muted`\n╰ {get_language(ctx.guild.id,'Назначит роль мьюта боту.')}\n\n`{prefix}rmute remove @Muted`\n╰ {get_language(ctx.guild.id,'Удалит роль мьюта из списка.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                elif helpvaluea == "admin5":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} settings", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Вы можете посмотреть все настройки бота.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}settings`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}stg`', inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}settings`\n╰ {get_language(ctx.guild.id,'Посмотреть настройки.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                elif helpvaluea == "admin6":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} list", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотреть список ограниченных каналов, игнорируемых ботов, пропусков или количество ботов в белом списке.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}list {get_language(ctx.guild.id,'{channels}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{channels}')}`; `{get_language(ctx.guild.id,'{ignores}')}`; `{get_language(ctx.guild.id,'{pass}')}`; `{get_language(ctx.guild.id,'{wl}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}list channels`\n╰ {get_language(ctx.guild.id,'Список ограниченных каналов.')}\n\n`{prefix}list ignores`\n╰ {get_language(ctx.guild.id,'Список игнорируемых ботов.')}\n\n`{prefix}list pass`\n╰ {get_language(ctx.guild.id,'Боты, у которых есть пропуска на сервер.')}\n\n`{prefix}list wl`\n╰ {get_language(ctx.guild.id,'Белый список ботов.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                elif helpvaluea == "admin7":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} echo", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Только Администраторы могут писать от лица бота.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}echo {get_language(ctx.guild.id,'{текст}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{текст}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}echo` {get_language(ctx.guild.id,'Это тестовое сообщение!')}\n╰ {get_language(ctx.guild.id,'Отправит сообщение от лица бота.')}", inline=False)
                                    embed.set_image(url=f"{get_language(ctx.guild.id,'https://media.discordapp.net/attachments/713751423128698950/859417527594254346/messages_from_VEGA__line_RU.png')}")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                elif helpvaluea == "admin8":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} emb", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Только Администраторы могут писать эмбед от лица бота.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}emb {get_language(ctx.guild.id,'{текст}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{текст}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}emb` {get_language(ctx.guild.id,'Это тестовое сообщение!')}\n╰ {get_language(ctx.guild.id,'Отправит сообщение эмбедом от лица бота.')}", inline=False)
                                    embed.set_image(url=f"{get_language(ctx.guild.id,'https://media.discordapp.net/attachments/713751423128698950/859417490324455444/emb_messages_from_VEGA__line_RU.png')}")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                elif helpvaluea == "admin9":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} slowmode", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Установите медленный режим в канале. Максимальное число в секундах 31600, минимальное 1. Число 0 сбросит медленный режим в канале.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}slowmode {get_language(ctx.guild.id,'{число}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{число}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}slowmode 2`\n╰ {get_language(ctx.guild.id,'Бот установит медленный режим в канале.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                    
                    elif helpvalue == "🛠":
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Модератора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                            ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}checkwl` — {get_language(ctx.guild.id,'проверить бота в белом списке.')}\n`{pre}ban` — {get_language(ctx.guild.id,'забанить пользователя.')}\n`{pre}unban` — {get_language(ctx.guild.id,'разбанить пользователя.')}\n`{pre}kick` — {get_language(ctx.guild.id,'кикнуть пользователя.')}\n`{pre}clear` — {get_language(ctx.guild.id,'очистить чат.')}\n`{pre}uclear` — {get_language(ctx.guild.id,'очистить сообщения указанного пользователя.')}\n`{pre}rolen` — {get_language(ctx.guild.id,'посмотреть кол-во пользователей с ролью.')}\n`{pre}user` — {get_language(ctx.guild.id,'информация о пользователе.')}\n`{pre}mute` — {get_language(ctx.guild.id,'замьютить пользователя.')}\n`{pre}unmute` — {get_language(ctx.guild.id,'размьютить пользователя.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                        await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenumoder, back])
                        def check(inter):
                            return inter.message.id == msg.id
                        while True:
                            try:
                                inter = await client.multiple_wait_for(
                                    {
                                        "dropdown": check,
                                        "button_click": check
                                    },
                                    timeout=60
                                )
                            except asyncio.TimeoutError:
                                await msg.edit(components=[row_1])
                                return
                            if inter.author != ctx.author:
                                # Не тот автор
                                await inter.reply(f"{get_language(ctx.guild.id, 'Этим меню управляете не вы!')}", ephemeral=True)
                            elif inter.button:
                                # Была нажата кнопка
                                button_id = inter.button.custom_id
                                if button_id == "Назад4":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Модератора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}checkwl` — {get_language(ctx.guild.id,'проверить бота в белом списке.')}\n`{pre}ban` — {get_language(ctx.guild.id,'забанить пользователя.')}\n`{pre}unban` — {get_language(ctx.guild.id,'разбанить пользователя.')}\n`{pre}kick` — {get_language(ctx.guild.id,'кикнуть пользователя.')}\n`{pre}clear` — {get_language(ctx.guild.id,'очистить чат.')}\n`{pre}uclear` — {get_language(ctx.guild.id,'очистить сообщения указанного пользователя.')}\n`{pre}rolen` — {get_language(ctx.guild.id,'посмотреть кол-во пользователей с ролью.')}\n`{pre}user` — {get_language(ctx.guild.id,'информация о пользователе.')}\n`{pre}mute` — {get_language(ctx.guild.id,'замьютить пользователя.')}\n`{pre}unmute` — {get_language(ctx.guild.id,'размьютить пользователя.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenumoder, back])
                                elif button_id == "Назад":
                                    embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                    embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed1.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed1, components=[helpmenu, row_1])
                                    break
                            elif inter.select_menu:
                                # Было нажато меню
                                helpvaluem = inter.select_menu.selected_options[0].value
                                if helpvaluem == "moder1":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} checkwl", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Только пользователи с правом Администратора или Управления сервером, могут проверить наличие одного или всех ботов из сервера в белом списке!')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}\n{get_language(ctx.guild.id,'Управлять сервером')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}checkwl {get_language(ctx.guild.id,'{ID бота}')}` {get_language(ctx.guild.id,'или')} `{prefix}checkwl {get_language(ctx.guild.id,'{all}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID бота}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{all}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}checkwl 767994849600602143`\n╰ {get_language(ctx.guild.id,'Проверка бота в белом списке.')}\n\n`{prefix}checkwl all`\n╰ {get_language(ctx.guild.id,'Проверка ботов на сервере в списках.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])
                                elif helpvaluem == "moder2":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} ban", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Забаньте нарушителя. Причина необязательна!')}\n{get_language(ctx.guild.id,'Бот забанит пользователя и удалит последние сообщения.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Банить пользователей')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}ban {get_language(ctx.guild.id,'{@пользователь}')} {get_language(ctx.guild.id,'[причина]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}ban {get_language(ctx.guild.id,'@пользователь')} {get_language(ctx.guild.id,'Спам приглашениями.')}`\n╰ {get_language(ctx.guild.id,'Бот забанит нарушителя.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])
                                elif helpvaluem == "moder3":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} unban", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Разбаньте нарушителя.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Банить пользователей')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}unban {get_language(ctx.guild.id,'{@пользователь}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}unban {get_language(ctx.guild.id,'@пользователь')}`\n╰ {get_language(ctx.guild.id,'Бот разбанит нарушителя.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])
                                elif helpvaluem == "moder4":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} kick", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Кикните нарушителя. Причина необязательна!')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Кикать пользователей')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}kick {get_language(ctx.guild.id,'{@пользователь}')} {get_language(ctx.guild.id,'[причина]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}kick {get_language(ctx.guild.id,'@пользователь')} {get_language(ctx.guild.id,'Спам приглашениями.')}`\n╰ {get_language(ctx.guild.id,'Бот выгонит нарушителя из сервера.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])
                                elif helpvaluem == "moder5":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} clear", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Очистите чат и сообщения пользователей на вашем сервере. Минимальное количество очистки сообщений 1, а максимальное 200.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Управлять сообщениями')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}clear {get_language(ctx.guild.id,'[@пользователь]')} {get_language(ctx.guild.id,'{число}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'[@пользователь]')}` {get_language(ctx.guild.id,'и')} | {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{число}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}purge`', inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}clear 12`\n╰ {get_language(ctx.guild.id,'Бот очистит сообщения в чате.')}\n\n`{prefix}clear {get_language(ctx.guild.id,'@пользователь')} 12`\n╰ {get_language(ctx.guild.id,'Бот очистит сообщения пользователя в чате.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])
                                elif helpvaluem == "moder6":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} uclear", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Очистите сообщения пользователя. Бот очистит сообщения написанные пользователем за последнюю неделю.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Управлять сообщениями')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}uclear {get_language(ctx.guild.id,'{@пользователь}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{@пользователь}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}uclear {get_language(ctx.guild.id,'@пользователь')}`\n╰ {get_language(ctx.guild.id,'Бот очистит последние сообщения пользоватея.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])
                                elif helpvaluem == "moder7":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} rolen", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотреть количество пользователей с данной ролью.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Управлять ролями')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}rolen {get_language(ctx.guild.id,'{@роль}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}rolen {роль}`\n╰ {get_language(ctx.guild.id,'Покажет количество пользователей с ролью.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])
                                elif helpvaluem == "moder8":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} user", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотреть информацию о себе или пользователе.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Журнал аудита')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}user {get_language(ctx.guild.id,'[@пользователь]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'[@пользователь]')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'[ID пользователя]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}userinfo`\n`{prefix}user-info`\n`{prefix}u`', inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}user`\n╰ {get_language(ctx.guild.id,'Покажет информацию о вас.')}\n\n`{prefix}user {get_language(ctx.guild.id,'[@пользователь]')}`\n╰ {get_language(ctx.guild.id,'Покажет информацию о пользователе.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])
                                elif helpvaluem == "moder9":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} mute", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Замьютьте нарушителя. Причина не обязательна.')}\n{get_language(ctx.guild.id,'Роль мьюта не будет настраиваться ботом!')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Журнал аудита')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}mute {get_language(ctx.guild.id,'{@пользователь}')} {get_language(ctx.guild.id,'[причина]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}mute {get_language(ctx.guild.id,'@пользователь')} {get_language(ctx.guild.id,'Спам сообщениями.')}`\n╰ {get_language(ctx.guild.id,'Бот выдаст нарушителю роль мьюта.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])
                                elif helpvaluem == "moder10":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} unmute", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Забрать у нарушителя роль мьюта.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Журнал аудита')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}unmute {get_language(ctx.guild.id,'{@пользователь}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}unmute {get_language(ctx.guild.id,'@пользователь')}`\n╰ {get_language(ctx.guild.id,'Бот заберет у нарушителя роль мьюта.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])

                    elif helpvalue == "🎉":
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Веселье')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                            ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}8ball` — {get_language(ctx.guild.id,'задать вопрос шару.')}\n`{pre}avatar` — {get_language(ctx.guild.id,'посмотреть аватар пользователя.')}\n`{pre}emoji` — {get_language(ctx.guild.id,'посмотреть эмодзи.')}\n`{pre}random` — {get_language(ctx.guild.id,'рандомное число, от и до.')}\n`{pre}math` — {get_language(ctx.guild.id,'обычный калькулятор.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                        await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenufun, back])


                        def check(inter):
                            return inter.message.id == msg.id

                        while True:
                            try:
                                inter = await client.multiple_wait_for(
                                    {
                                        "dropdown": check,
                                        "button_click": check
                                    },
                                    timeout=60
                                )
                            except asyncio.TimeoutError:
                                await msg.edit(components=[row_1])
                                return

                            if inter.author != ctx.author:
                                # Не тот автор
                                await inter.reply(f"{get_language(ctx.guild.id, 'Этим меню управляете не вы!')}", ephemeral=True)
                            elif inter.button:
                                # Была нажата кнопка
                                button_id = inter.button.custom_id
                                if button_id == "Назад5":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Веселье')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}8ball` — {get_language(ctx.guild.id,'задать вопрос шару.')}\n`{pre}avatar` — {get_language(ctx.guild.id,'посмотреть аватар пользователя.')}\n`{pre}emoji` — {get_language(ctx.guild.id,'посмотреть эмодзи.')}\n`{pre}random` — {get_language(ctx.guild.id,'рандомное число, от и до.')}\n`{pre}math` — {get_language(ctx.guild.id,'обычный калькулятор.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenufun, back])
                                elif button_id == "Назад":
                                    embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                    embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed1.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed1, components=[helpmenu, row_1])
                                    break
                            elif inter.select_menu:
                                # Было нажато меню
                                helpvaluef = inter.select_menu.selected_options[0].value
                                if helpvaluef == "fun1":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} 8ball", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Задайте вопрос шару и узнайте правду.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}8ball {get_language(ctx.guild.id,'{текст}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{текст}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}8ball {get_language(ctx.guild.id,'Завтра будет ясная погода?')}`\n╰ {get_language(ctx.guild.id,'Бот ответит на ваш вопрос.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back5])
                                elif helpvaluef == "fun2":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} avatar", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотрите и скачайте аватар пользователя.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}avatar {get_language(ctx.guild.id,'[@пользователь]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'[@пользователь]')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'[ID пользователя]')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}ava`', inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}avatar`\n╰ {get_language(ctx.guild.id,'Покажет ваш аватар.')}\n\n`{prefix}avatar {get_language(ctx.guild.id,'[@пользователь]')}`\n╰ {get_language(ctx.guild.id,'Покажет аватар пользователя.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back5])
                                elif helpvaluef == "fun3":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} emoji", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Вы можете осмотреть и скачать эмодзи.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}emoji {get_language(ctx.guild.id,'{эмодзи}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{эмодзи}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"{prefix}emoji <:python:826158844555427891>\n╰ {get_language(ctx.guild.id,'Посмотреть эмодзи.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back5])
                                elif helpvaluef == "fun4":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} random", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Если хотите выбрать случайное число, то воспользуйтесь данной командой.')}", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}random {a} {b}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{a}` {get_language(ctx.guild.id,'и')} `{b}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}r`\n`{prefix}rand`', inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}random 5 10`\n╰ {get_language(ctx.guild.id,'Бот выберет рандомное число.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back5])
                                elif helpvaluef == "fun5":
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} math", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                        {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Калькулятор для решения простых примеров.')}\n{get_language(ctx.guild.id,'Используются знаки')} `() + - / *`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}math {get_language(ctx.guild.id,'{пример}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{пример}')}`", inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}calculate`\n`{prefix}calc`', inline=False)
                                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}math 5*5`\n╰ {get_language(ctx.guild.id,'Бот решит пример за вас.')}", inline=False)
                                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                    embed.set_footer(icon_url=client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                    await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back5])
"""



# Перезапустить ког
@client.slash_command(name="reload", description="Restart the cog | Переапустить ког", default_permission=False)
@commands.guild_only()
@commands.guild_permissions(826022179568615445, users={351020816466575372: True})
async def reload(ctx,  cog_name: str = commands.Param(name="cog_name", description="Specify the cog | Укажите ког")):
    if ctx.author.id != 351020816466575372:
        embed = discord.Embed(description=f"**{get_language(ctx.guild.id,'Команда только для РАЗРАБОТЧИКОВ!')}**", color=0xcc1a1d)
        await ctx.send(embed=embed, ephemeral=True)
    client.unload_extension("cogs." + cog_name)
    client.load_extension("cogs." + cog_name)
    await ctx.send(f"Ког **{cog_name}** был перезапущен!", ephemeral=True)




# Тест
# @client.command(name="test", aliases=["тест"], pass_context=True)
# @commands.guild_only()
# @commands.bot_has_permissions(send_messages=True)
# async def test(ctx):
#    await send_graph(ctx, [1, 3, 5, 7, 9], [2, 4, 3, 6 ,7], title="Количество макарон")


# Оброботчик ошибок в оставшееся время команды (Неверная команда)
kd = {}


@client.event
async def on_command_error(ctx, error):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        """with open('logging/console_log.log','a') as file:
        file.write(f"{str(error)}\n\n")
        print("[ ИНФО ]  Ошибки были сохранены!\n")"""

        if await checkchannel(ctx):
            global kd
            try:
                unix = kd[ctx.author.id]
            except:
                unix = 0
            if isinstance(error, commands.CommandOnCooldown):
                if unix < int(time.time()):
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'⏱ Кулдаун команды. Будет активна через:')}\n    {format(hmsd(ctx, error.retry_after))}",
                        color=0x2F3136,
                    )
                    await ctx.message.reply(embed=embed, delete_after=12.0)
                    msg = ctx.message
                    try:
                        await msg.add_reaction("<a:time:811137967309586452>")
                    except:
                        pass
                    kd[ctx.author.id] = int(time.time()) + 10

            if isinstance(error, commands.MissingPermissions):
                if unix < int(time.time()):
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,':warning: Отсутствуют необходимые полномочия!')}",
                        color=0xFCC21B,
                    )
                    missing = str(error)
                    missing = missing.replace("You are missing ", "")
                    missing = missing.replace(" permission(s) to run this command.", "")
                    missing = missing.lower()
                    perms = {
                        "administrator": f"{get_language(ctx.guild.id,'Администратор')}",
                        "view audit log": f"{get_language(ctx.guild.id,'Просмотр журнала аудита')}",
                        "manage server": f"{get_language(ctx.guild.id,'Управлять сервером')}",
                        "manage roles": f"{get_language(ctx.guild.id,'Управлять ролями')}",
                        "manage channels": f"{get_language(ctx.guild.id,'Управлять каналами')}",
                        "kick members": f"{get_language(ctx.guild.id,'Выгонять участников')}",
                        "ban members": f"{get_language(ctx.guild.id,'Банить участников')}",
                        "change nickname": f"{get_language(ctx.guild.id,'Изменить никнейм')}",
                        "manage nicknames": f"{get_language(ctx.guild.id,'Управлять никнеймами')}",
                        "view channels": f"{get_language(ctx.guild.id,'Читать сообщения')}",
                        "send messages": f"{get_language(ctx.guild.id,'Отправлять сообщения')}",
                        "send tts messages": f"{get_language(ctx.guild.id,'Отправлять TTS сообщения')}",
                        "manage messages": f"{get_language(ctx.guild.id,'Управлять сообщениями')}",
                        "embed links": f"{get_language(ctx.guild.id,'Встраивать ссылки')}",
                        "attach files": f"{get_language(ctx.guild.id,'Прикреплять файлы')}",
                    }
                    ctx.command.reset_cooldown(ctx)
                    if missing in perms:
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Необходимое право:')}",
                            value=f"`{perms[missing]}`",
                            inline=False,
                        )
                    await ctx.message.reply(embed=embed, delete_after=12)
                    msg = ctx.message
                    try:
                        await msg.add_reaction(":warning:")
                    except:
                        pass
                    kd[ctx.author.id] = int(time.time()) + 10

            if isinstance(error, commands.errors.BotMissingPermissions):
                if unix < int(time.time()):
                    embed = discord.Embed(
                        description=":warning: У бота отсутствую необходимые полномочия!",
                        color=0xFCC21B,
                    )
                    missing = str(error)
                    missing = missing.replace("Bot requires ", "")
                    missing = missing.replace(" permission(s) to run this command.", "")
                    missing = missing.lower()
                    perms = {
                        "administrator": f"{get_language(ctx.guild.id,'Администратор')}",
                        "view audit log": f"{get_language(ctx.guild.id,'Просмотр журнала аудита')}",
                        "manage server": f"{get_language(ctx.guild.id,'Управлять сервером')}",
                        "manage channels": f"{get_language(ctx.guild.id,'Управлять каналами')}",
                        "manage roles": f"{get_language(ctx.guild.id,'Управлять ролями')}",
                        "kick members": f"{get_language(ctx.guild.id,'Выгонять участников')}",
                        "ban members": f"{get_language(ctx.guild.id,'Банить участников')}",
                        "change nickname": f"{get_language(ctx.guild.id,'Изменить никнейм')}",
                        "manage nicknames": f"{get_language(ctx.guild.id,'Управлять никнеймами')}",
                        "view channels": f"{get_language(ctx.guild.id,'Читать сообщения')}",
                        "send messages": f"{get_language(ctx.guild.id,'Отправлять сообщения')}",
                        "send tts messages": f"{get_language(ctx.guild.id,'Отправлять TTS сообщения')}",
                        "manage messages": f"{get_language(ctx.guild.id,'Управлять сообщениями')}",
                        "embed links": f"{get_language(ctx.guild.id,'Встраивать ссылки')}",
                        "attach files": f"{get_language(ctx.guild.id,'Прикреплять файлы')}",
                    }
                    ctx.command.reset_cooldown(ctx)
                    if missing in perms:
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Необходимое право:')}",
                            value=f"`{perms[missing]}`",
                            inline=False,
                        )
                    await ctx.message.reply(embed=embed, delete_after=12)
                    msg = ctx.message
                    try:
                        await msg.add_reaction(":warning:")
                    except:
                        pass
                    kd[ctx.author.id] = int(time.time()) + 10

            if isinstance(error, commands.MemberNotFound):
                if unix < int(time.time()):
                    ctx.command.reset_cooldown(ctx)
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,':warning: Пользователь не найден!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, delete_after=5.0)
                    msg = ctx.message
                    await msg.add_reaction(":warning:")
                    kd[ctx.author.id] = int(time.time()) + 10
            if isinstance(error, commands.UserNotFound):
                if unix < int(time.time()):
                    ctx.command.reset_cooldown(ctx)
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,':warning: Пользователь не найден!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, delete_after=5.0)
                    msg = ctx.message
                    try:
                        await msg.add_reaction(":warning:")
                    except:
                        pass
                    kd[ctx.author.id] = int(time.time()) + 10
            # if isinstance(error, commands.ChannelNotFound):
            #    if unix < int(time.time()):
            #        ctx.command.reset_cooldown(ctx)
            #        embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Канал не найден!')}", color=0xfcc21b)
            #        await ctx.send(embed=embed, delete_after=5.0)
            #        msg = ctx.message
            #        await msg.add_reaction(':warning:')
            #        kd[ctx.author.id] = int(time.time()) + 10
            if isinstance(error, commands.RoleNotFound):
                if unix < int(time.time()):
                    ctx.command.reset_cooldown(ctx)
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Роли не обнаружены!')}",
                        color=0xCC1A1D,
                    )
                    await ctx.send(embed=embed, delete_after=5.0)
                    msg = ctx.message
                    try:
                        await msg.add_reaction(":warning:")
                    except:
                        pass
                    kd[ctx.author.id] = int(time.time()) + 10
            else:
                raise error
        else:
            pass


@client.event
async def on_slash_command_error(inter, error):
    ctx = inter
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        if await checkchannel(ctx):
            if isinstance(error, commands.CommandOnCooldown):
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,'⏱ Кулдаун команды. Будет активна через:')}\n    {format(hmsd(ctx, error.retry_after))}",
                    color=0x2F3136,
                )
                await ctx.send(embed=embed, ephemeral=True)

            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: Отсутствуют необходимые полномочия!')}",
                    color=0xFCC21B,
                )
                missing = str(error)
                missing = missing.replace("You are missing ", "")
                missing = missing.replace(" permission(s) to run this command.", "")
                missing = missing.lower()
                perms = {
                    "administrator": f"{get_language(ctx.guild.id,'Администратор')}",
                    "view audit log": f"{get_language(ctx.guild.id,'Просмотр журнала аудита')}",
                    "manage server": f"{get_language(ctx.guild.id,'Управлять сервером')}",
                    "manage roles": f"{get_language(ctx.guild.id,'Управлять ролями')}",
                    "manage channels": f"{get_language(ctx.guild.id,'Управлять каналами')}",
                    "kick members": f"{get_language(ctx.guild.id,'Выгонять участников')}",
                    "ban members": f"{get_language(ctx.guild.id,'Банить участников')}",
                    "change nickname": f"{get_language(ctx.guild.id,'Изменить никнейм')}",
                    "manage nicknames": f"{get_language(ctx.guild.id,'Управлять никнеймами')}",
                    "view channels": f"{get_language(ctx.guild.id,'Читать сообщения')}",
                    "send messages": f"{get_language(ctx.guild.id,'Отправлять сообщения')}",
                    "send tts messages": f"{get_language(ctx.guild.id,'Отправлять TTS сообщения')}",
                    "manage messages": f"{get_language(ctx.guild.id,'Управлять сообщениями')}",
                    "embed links": f"{get_language(ctx.guild.id,'Встраивать ссылки')}",
                    "attach files": f"{get_language(ctx.guild.id,'Прикреплять файлы')}",
                }
                try:
                    ctx.command.reset_cooldown(ctx)
                except:
                    pass
                if missing in perms:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Необходимое право:')}",
                        value=f"`{perms[missing]}`",
                        inline=False,
                    )
                await ctx.send(embed=embed, ephemeral=True)

            if isinstance(error, commands.errors.BotMissingPermissions):
                embed = discord.Embed(
                    description=":warning: У бота отсутствую необходимые полномочия!",
                    color=0xFCC21B,
                )
                missing = str(error)
                missing = missing.replace("Bot requires ", "")
                missing = missing.replace(" permission(s) to run this command.", "")
                missing = missing.lower()
                perms = {
                    "administrator": f"{get_language(ctx.guild.id,'Администратор')}",
                    "view audit log": f"{get_language(ctx.guild.id,'Просмотр журнала аудита')}",
                    "manage server": f"{get_language(ctx.guild.id,'Управлять сервером')}",
                    "manage channels": f"{get_language(ctx.guild.id,'Управлять каналами')}",
                    "manage roles": f"{get_language(ctx.guild.id,'Управлять ролями')}",
                    "kick members": f"{get_language(ctx.guild.id,'Выгонять участников')}",
                    "ban members": f"{get_language(ctx.guild.id,'Банить участников')}",
                    "change nickname": f"{get_language(ctx.guild.id,'Изменить никнейм')}",
                    "manage nicknames": f"{get_language(ctx.guild.id,'Управлять никнеймами')}",
                    "view channels": f"{get_language(ctx.guild.id,'Читать сообщения')}",
                    "send messages": f"{get_language(ctx.guild.id,'Отправлять сообщения')}",
                    "send tts messages": f"{get_language(ctx.guild.id,'Отправлять TTS сообщения')}",
                    "manage messages": f"{get_language(ctx.guild.id,'Управлять сообщениями')}",
                    "embed links": f"{get_language(ctx.guild.id,'Встраивать ссылки')}",
                    "attach files": f"{get_language(ctx.guild.id,'Прикреплять файлы')}",
                }
                try:
                    ctx.command.reset_cooldown(ctx)
                except:
                    pass
                if missing in perms:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Необходимое право:')}",
                        value=f"`{perms[missing]}`",
                        inline=False,
                    )
                await ctx.send(embed=embed, ephemeral=True)

            if isinstance(error, commands.MemberNotFound):
                try:
                    ctx.command.reset_cooldown(ctx)
                except:
                    pass
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: Пользователь не найден!')}",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
            if isinstance(error, commands.UserNotFound):
                try:
                    ctx.command.reset_cooldown(ctx)
                except:
                    pass
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: Пользователь не найден!')}",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
            """if isinstance(error, commands.ChannelNotFound):
                try:ctx.command.reset_cooldown(ctx)
                except:pass
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Канал не найден!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)"""
            if isinstance(error, commands.RoleNotFound):
                try:
                    ctx.command.reset_cooldown(ctx)
                except:
                    pass
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Роли не обнаружены!')}",
                    color=0xCC1A1D,
                )
                await ctx.send(embed=embed, ephemeral=True)
            else:
                raise error
        else:
            pass


# AntiBot код:

# Автокик новых ботов
@client.event
async def on_member_join(member):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        mr = gdata("vega", "muterole")
        w = gdata("vega", "mute_users")
        try:
            if str(member.id) in w[str(member.guild.id)]:
                muterole = member.guild.get_role(int(mr[str(member.guild.id)]))
                await member.add_roles(muterole)
            else:
                print("[ ИНФО ]  Пользователь не замьючен!\n")
                pass
        except:
            print("!!! [ ОШИБКА ]  Роль мьюта не указана!\n")

        lc = gdata("vega", "logchannel")
        wl = gdata("vega", "ignorebots")
        if str(member.guild.id) in wl:
            dop = wl[str(member.guild.id)]
        else:
            dop = ""

        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            data = gdata("vega", "antibot")
            w = gdata("vega", "wlbots")
            p = gdata("vega", "passbots")
            try:
                enabled = data[str(member.guild.id)]
            except KeyError:
                enabled = False
            if member.bot:
                try:
                    async for entry in member.guild.audit_logs(
                        limit=1, action=discord.AuditLogAction.bot_add
                    ):
                        if (
                            not str(member.id) in w[str("Bots")]
                            and not str(member.id) in dop
                        ):
                            if enabled:
                                if str(member.guild.id) in p:
                                    pss = p[str(member.guild.id)]
                                else:
                                    pss = ""
                                if not str(member.id) in pss:
                                    await member.ban(
                                        reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                        delete_message_days=1,
                                    )
                                    # await asyncio.sleep(5)
                                    embed = discord.Embed(
                                        description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})\n\n**{get_language(member.guild.id,'Информация о боте:')}**\n{get_language(member.guild.id,'Присоединился:')} <t:{int(member.joined_at.timestamp())}:F>\n{get_language(member.guild.id,'Создан:')} <t:{int(member.created_at.timestamp())}:F>",
                                        color=0xFCC21B,
                                    )
                                    embed.set_author(
                                        name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                    embed.set_thumbnail(
                                        url=member.avatar.replace(size=1024)
                                    )
                                    embed.set_footer(
                                        text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(lc[str(member.guild.id)])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                else:
                                    p = gdata("vega", "passbots")
                                    p.update(
                                        {
                                            str(member.guild.id): p[
                                                str(member.guild.id)
                                            ].replace(str(f"<@!{member.id}>, "), "")
                                        }
                                    )
                                    wdata("vega", "passbots", p)
                                    embed = discord.Embed(
                                        description=f"<:arrow:847308468091879434> **{get_language(member.guild.id,'Пригласил бота:')}** {entry.user}\nㅤ **ID:** `{entry.user.id}`\n\n**{get_language(member.guild.id,'Информация о боте:')}**\n{get_language(member.guild.id,'Присоединился:')} <t:{int(member.joined_at.timestamp())}:F>\n{get_language(member.guild.id,'Создан:')} <t:{int(member.created_at.timestamp())}:F>",
                                        color=0xCC1A1D,
                                    )
                                    embed.set_author(
                                        name=f"{get_language(member.guild.id, 'Пропуск')} {member} {get_language(member.guild.id, 'истек!')}",
                                        icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                    )
                                    embed.set_footer(text=f"ID: {member.id}")
                                    try:
                                        await client.get_channel(
                                            int(lc[str(member.guild.id)])
                                        ).send(embed=embed)
                                    except:
                                        pass

                        elif (
                            not str(member.id) in w[str("Bots")]
                            and str(member.id) in dop
                        ):
                            embed = discord.Embed(
                                description=f"<:arrow:847308468091879434> **{get_language(member.guild.id,'Пригласил бота:')}** {entry.user}\nㅤ **ID:** `{entry.user.id}`\n\n**{get_language(member.guild.id,'Информация о боте:')}**\n{get_language(member.guild.id,'Присоединился:')} <t:{int(member.joined_at.timestamp())}:F>\n{get_language(member.guild.id,'Создан:')} <t:{int(member.created_at.timestamp())}:F>",
                                color=discord.Colour.blue(),
                            )
                            embed.set_author(
                                name=f"{member} {get_language(member.guild.id,'игнорируется на данном сервере!')}",
                                icon_url="https://cdn.discordapp.com/attachments/713751423128698950/904448009583100005/invisible1600.png",
                            )
                            embed.set_thumbnail(url=member.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(lc[str(member.guild.id)])
                                ).send(embed=embed)
                            except:
                                pass
                        elif str(member.id) in w[str("Bots")]:
                            embed = discord.Embed(
                                description=f"<:arrow:847308468091879434> **{get_language(member.guild.id,'Пригласил бота:')}** {entry.user}\nㅤ **ID:** `{entry.user.id}`\n\n**{get_language(member.guild.id,'Информация о боте:')}**\n{get_language(member.guild.id,'Присоединился:')} <t:{int(member.joined_at.timestamp())}:F>\n{get_language(member.guild.id,'Создан:')} <t:{int(member.created_at.timestamp())}:F>",
                                color=discord.Colour.green(),
                            )
                            embed.set_author(
                                name=f"{member} {get_language(member.guild.id,'находится в белом списке!')}",
                                icon_url="https://cdn.discordapp.com/attachments/713751423128698950/904452846664183858/wl_bots.png",
                            )
                            embed.set_thumbnail(url=member.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(lc[str(member.guild.id)])
                                ).send(embed=embed)
                            except:
                                pass
                except:
                    pass


# Удаление канала
@client.event
async def on_guild_channel_delete(channel):
    wl = gdata("vega", "ignorebots")
    if str(channel.guild.id) in wl:
        dop = wl[str(channel.guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(channel.guild.id)]
        except KeyError:
            enabled = False
        try:
            async for entry in channel.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_delete
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != channel.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):

                    try:
                        await entry.user.ban(
                            reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}\n\n**{get_language(channel.guild.id,'Информация о боте:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(lc[str(channel.guild.id)])
                            ).send(embed=embed)
                        except:
                            pass
                    except:
                        pass

                    if isinstance(channel, discord.CategoryChannel):
                        await channel.clone()
                    elif not channel.category:
                        await channel.clone()
                    else:
                        if isinstance(channel, discord.TextChannel):
                            await channel.guild.create_text_channel(
                                category=get(
                                    channel.guild.categories, name=channel.category.name
                                ),
                                name=channel.name,
                                topic=channel.topic,
                                nsfw=channel.nsfw,
                                overwrites=channel.overwrites,
                                position=channel.position,
                                slowmode_delay=channel.slowmode_delay,
                            )
                        else:
                            await channel.guild.create_voice_channel(
                                category=get(
                                    channel.guild.categories, name=channel.category.name
                                ),
                                name=channel.name,
                                bitrate=channel.bitrate,
                                overwrites=channel.overwrites,
                                position=channel.position,
                                user_limit=channel.user_limit,
                            )
                        await asyncio.sleep(5)
                        await channel.edit(
                            category=get(
                                channel.guild.categories, name=channel.category.name
                            )
                        )
        except:
            pass


# Создание канала
@client.event
async def on_guild_channel_create(channel):
    wl = gdata("vega", "ignorebots")
    if str(channel.guild.id) in wl:
        dop = wl[str(channel.guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(channel.guild.id)]
        except KeyError:
            enabled = False
        try:
            async for entry in channel.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_create
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != channel.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}\n\n**{get_language(channel.guild.id,'Информация о боте:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(lc[str(channel.guild.id)])
                            ).send(embed=embed)
                        except:
                            pass
                    except:
                        pass
                    await channel.delete()
        except:
            pass


# Удаление роли
@client.event
async def on_guild_role_delete(role):
    wl = gdata("vega", "ignorebots")
    if str(role.guild.id) in wl:
        dop = wl[str(role.guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(role.guild.id)]
        except KeyError:
            enabled = False
        try:
            async for entry in role.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_delete
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != role.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    if not role.managed:
                        try:
                            await entry.user.ban(
                                reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны бота!')}",
                                delete_message_days=1,
                            )
                            lc = gdata("vega", "logchannel")
                            embed = discord.Embed(
                                description=f"{get_language(role.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(role.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(role.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}\n\n**{get_language(role.guild.id,'Информация о боте:')}**\n{get_language(role.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                color=0xFCC21B,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(role.guild.id,'был забанен функцией AntiBot')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024)
                            )
                            embed.set_footer(
                                text=f"{get_language(role.guild.id,'ID бота:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(lc[str(role.guild.id)])
                                ).send(embed=embed)
                            except:
                                pass
                        except:
                            pass
                        await role.guild.create_role(
                            name=role.name,
                            permissions=role.permissions,
                            colour=role.colour,
                            hoist=role.hoist,
                            mentionable=role.mentionable,
                        )
                    else:
                        print(f"[ ИНФО ] Роль {role} интегрирована.")
        except:
            pass


# Создание роли
@client.event
async def on_guild_role_create(role):
    wl = gdata("vega", "ignorebots")
    if str(role.guild.id) in wl:
        dop = wl[str(role.guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(role.guild.id)]
        except KeyError:
            enabled = False
        try:
            async for entry in role.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_create
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != role.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    if not role.managed:
                        try:
                            await entry.user.ban(
                                reason=f"{get_language(role.guild.id,'[AntiBot] Создане ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны бота!')}",
                                delete_message_days=1,
                            )
                            lc = gdata("vega", "logchannel")
                            embed = discord.Embed(
                                description=f"{get_language(role.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(role.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(role.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiBot] Создане ролей!')}\n\n**{get_language(role.guild.id,'Информация о боте:')}**\n{get_language(role.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                color=0xFCC21B,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(role.guild.id,'был забанен функцией AntiBot')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024)
                            )
                            embed.set_footer(
                                text=f"{get_language(role.guild.id,'ID бота:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(lc[str(role.guild.id)])
                                ).send(embed=embed)
                            except:
                                pass
                        except:
                            pass
                        await role.delete()
        except:
            pass


# Обновление роли
@client.event
async def on_guild_role_update(before, after):
    wl = gdata("vega", "ignorebots")
    if str(after.guild.id) in wl:
        dop = wl[str(after.guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(after.guild.id)]
        except KeyError:
            enabled = False
        try:
            async for entry in after.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_update
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != after.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление прав ролей!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление прав ролей!')}\n\n**{get_language(after.guild.id,'Информация о боте:')}**\n{get_language(after.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(int(lc[str(after.guild.id)])).send(
                                embed=embed
                            )
                        except:
                            pass
                    except:
                        pass
                    await after.edit(permissions=before.permissions)
        except:
            pass


# Обновление канала
@client.event
async def on_guild_channel_update(before, after):
    wl = gdata("vega", "ignorebots")
    if str(after.guild.id) in wl:
        dop = wl[str(after.guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(after.guild.id)]
        except KeyError:
            enabled = False
        try:
            async for entry in after.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_update
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != after.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление настроек каналов!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление настроек каналов!')}\n\n**{get_language(after.guild.id,'Информация о боте:')}**\n{get_language(after.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(int(lc[str(after.guild.id)])).send(
                                embed=embed
                            )
                        except:
                            pass
                    except:
                        pass

                    await after.edit(overwrites=before.overwrites)
        except:
            pass


# Бан пользователя
@client.event
async def on_member_ban(guild, user):
    wl = gdata("vega", "ignorebots")
    if str(guild.id) in wl:
        dop = wl[str(guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(guild.id)]
        except KeyError:
            enabled = False
        try:
            w = gdata("vega", "wlbots")
            lc = gdata("vega", "logchannel")
            async for entry in guild.audit_logs(
                limit=1, action=discord.AuditLogAction.ban
            ):
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(guild.id,'[AntiBot] Бан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        await guild.unban(user)
                        embed = discord.Embed(
                            description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Бан пользователя!')}\n\n**{get_language(guild.id,'Информация о боте:')}**\n{get_language(guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(int(lc[str(guild.id)])).send(
                                embed=embed
                            )
                        except:
                            pass
                    except:
                        pass
                elif entry.target.bot and entry.user != client.get_user(
                    795551166393876481
                ):
                    embed = discord.Embed(
                        description=f"**{get_language(guild.id,'Пользователем:')}** {entry.user}\n**ID:** `{entry.user.id}`\n\n**{get_language(guild.id,'Информация о боте:')}**\n{get_language(guild.id,'Присоединился:')} <t:{int(user.joined_at.timestamp())}:F>\n{get_language(guild.id,'Создан:')} <t:{int(user.created_at.timestamp())}:F>",
                        color=0xFF2B2B,
                    )
                    embed.set_author(
                        name=f"{user} {get_language(guild.id,'забанен!')}",
                        icon_url="https://cdn.discordapp.com/attachments/713751423128698950/810933957197037588/ban.png",
                    )
                    embed.set_thumbnail(url=user.avatar.replace(size=1024))
                    embed.set_footer(
                        text=f"{get_language(guild.id,'ID бота:')} {user.id}"
                    )
                    try:
                        await client.get_channel(int(lc[str(guild.id)])).send(
                            embed=embed
                        )
                    except:
                        pass
                else:
                    pass
        except:
            pass


# Разбан пользователя
@client.event
async def on_member_unban(guild, user):
    wl = gdata("vega", "ignorebots")
    if str(guild.id) in wl:
        dop = wl[str(guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(guild.id)]
        except KeyError:
            enabled = False
        try:
            async for entry in guild.audit_logs(
                limit=1, action=discord.AuditLogAction.unban
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(guild.id,'[AntiBot] Разбан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        await guild.ban(user)
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Разбан пользователя!')}\n\n**{get_language(guild.id,'Информация о боте:')}**\n{get_language(guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(int(lc[str(guild.id)])).send(
                                embed=embed
                            )
                        except:
                            pass
                    except:
                        pass
        except:
            pass


# Обновление пользователя
@client.event
async def on_member_update(before, after):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        if before.roles != after.roles:
            mu = gdata("vega", "mute_users")
            mr = gdata("vega", "muterole")
            if str(after.guild.id) in mu:
                mu2 = mu[str(after.guild.id)]
            else:
                mu2 = ""
            if str(after.guild.id) in mr:
                mr = int(mr[str(after.guild.id)])
                if mr in [r.id for r in before.roles] and not mr in [
                    r.id for r in after.roles
                ]:
                    mu2 = mu2.replace(str(after.id), "").strip()
                    mu[str(after.guild.id)] = mu2
                    wdata("vega", "mute_users", mu)
                elif not mr in [r.id for r in before.roles] and mr in [
                    r.id for r in after.roles
                ]:
                    mu2 += str(after.id) + " "
                    mu[str(after.guild.id)] = mu2
                    wdata("vega", "mute_users", mu)


"""@client.event
async def on_guild_member_update(before, after):
    global whitelistedbot
    with open('json/antibot.json', 'r') as f:
        data = json.load(f)
    data = gdata('vega', 'antibot')
    with open('json/ignorebots.json', 'r') as f:
        wl = json.load(f)
    wl = gdata('vega', 'ignorebots')
    if str(after.id) in wl:
        dop = wl[str(after.id)]
    else:
        dop = ''
    try:
        enabled = data[str(after.id)]
    except KeyError:
        enabled = False
    avaliable = [r for r in after.roles if not r.managed]
    mngd = get(after.roles, managed=True)
    for i in avaliable:
        try:
            await after.remove_roles(i)
        except:
            pass
    await mngd.edit(permissions=discord.Permissions(permissions=1024))"""


# Настройки гильдии
@client.event
async def on_guild_update(before, after):
    wl = gdata("vega", "ignorebots")
    if str(after.id) in wl:
        dop = wl[str(after.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(after.id)]
        except KeyError:
            enabled = False
        try:
            async for entry in after.audit_logs(
                limit=1, action=discord.AuditLogAction.guild_update
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != after.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):

                    try:
                        await entry.user.ban(
                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление настроек сервера!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление настроек сервера!')}\n\n**{get_language(after.guild.id,'Информация о боте:')}**\n{get_language(after.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(int(lc[str(after.guild.id)])).send(
                                embed=embed
                            )
                        except:
                            pass
                    except:
                        pass

                    await after.edit(name=before.name)
        except:
            pass


# Эмодзи
@client.event
async def on_guild_emojis_update(guild, before, after):
    wl = gdata("vega", "ignorebots")
    if str(guild.id) in wl:
        dop = wl[str(guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(guild.id)]
        except KeyError:
            enabled = False

        """# Эмодзи редактирован
        try:
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_update):
                w = gdata('vega', 'wlbots')
                if not str(entry.user.id) in w[str("Bots")] and entry.user != guild.owner and enabled and entry.user.bot and not str(entry.user.id) in dop:
                    try:
                        await entry.user.ban(reason=f"{get_language(guild.id,'[AntiBot] Редактирование эмодзи!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}", delete_message_days=1)
                        lc = gdata('vega', 'logchannel')
                        embed = discord.Embed(description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Редактирование эмодзи!')}\n\n**{get_language(guild.id,'Информация о боте:')}**\n{get_language(guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>", color=0xfcc21b)
                        embed.set_author(name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}", icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif")
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}")
                        try:
                            await client.get_channel(int(lc[str(guild.id)])).send(embed=embed)
                        except:
                            pass
                    except:
                        pass
                    
                    for emoji in after:
                        if after.name != before[after.index(emoji)].name:
                            await emoji.edit(name=before[after.index(emoji)].name)
        except:
            pass"""

        # Эмодзи создан
        try:
            async for entry in guild.audit_logs(
                limit=1, action=discord.AuditLogAction.emoji_create
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(guild.id,'[AntiBot] Создание эмодзи!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Создание эмодзи!')}\n\n**{get_language(guild.id,'Информация о боте:')}**\n{get_language(guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(int(lc[str(guild.id)])).send(
                                embed=embed
                            )
                        except:
                            pass
                    except:
                        pass

                    await before.emoji.delete()
        except:
            pass

        # Эмодзи удален
        try:
            async for entry in guild.audit_logs(
                limit=1, action=discord.AuditLogAction.emoji_delete
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(guild.id,'[AntiBot] Удаление эмодзи!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Удаление эмодзи!')}\n\n**{get_language(guild.id,'Информация о боте:')}**\n{get_language(guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(int(lc[str(guild.id)])).send(
                                embed=embed
                            )
                        except:
                            pass
                    except:
                        pass
        except:
            pass


# Создание приглашения
@client.event
async def on_invite_create(invite):
    wl = gdata("vega", "ignorebots")
    if str(invite.guild.id) in wl:
        dop = wl[str(invite.guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(invite.guild.id)]
        except KeyError:
            enabled = False

        # Приглашение создано
        try:
            async for entry in invite.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.invite_create
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != invite.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(invite.guild.id,'[AntiBot] Создание приглашения!')} {get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(invite.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(invite.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(invite.guild.id,'Причина:')}**\n{get_language(invite.guild.id,'[AntiBot] Создание приглашения!')}\n\n**{get_language(invite.guild.id,'Информация о боте:')}**\n{get_language(invite.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(invite.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(invite.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(lc[str(invite.guild.id)])
                            ).send(embed=embed)
                        except:
                            pass
                    except:
                        pass

                    await invite.delete()
        except:
            pass


# Удаление приглашения
@client.event
async def on_invite_remove(invite):
    wl = gdata("vega", "ignorebots")
    if str(invite.guild.id) in wl:
        dop = wl[str(invite.guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(invite.guild.id)]
        except KeyError:
            enabled = False

        # Приглашение удалено
        try:
            async for entry in invite.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.invite_remove
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != invite.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(invite.guild.id,'[AntiBot] Удаление приглашения!')} {get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(invite.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(invite.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(invite.guild.id,'Причина:')}**\n{get_language(invite.guild.id,'[AntiBot] Удаление приглашения!')}\n\n**{get_language(invite.guild.id,'Информация о боте:')}**\n{get_language(invite.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(invite.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(invite.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(lc[str(invite.guild.id)])
                            ).send(embed=embed)
                        except:
                            pass
                    except:
                        pass
        except:
            pass


# Вебхуки
@client.event
async def on_webhooks_update(channel):
    wl = gdata("vega", "ignorebots")
    if str(channel.guild.id) in wl:
        dop = wl[str(channel.guild.id)]
    else:
        dop = ""
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(channel.guild.id)]
        except KeyError:
            enabled = False

        # Вебхук создан
        try:
            async for entry in channel.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.webhook_create
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != channel.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}\n\n**{get_language(channel.guild.id,'Информация о боте:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(lc[str(channel.guild.id)])
                            ).send(embed=embed)
                        except:
                            pass
                    except:
                        pass

                    await channel.webhook.delete()
        except:
            pass

        # Вебхук удален
        try:
            async for entry in channel.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.webhook_delete
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != channel.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Удаление вебхука!')}\n\n**{get_language(channel.guild.id,'Информация о боте:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(lc[str(channel.guild.id)])
                            ).send(embed=embed)
                        except:
                            pass
                    except:
                        pass
        except:
            pass

        # Вебхук отредактирован
        try:
            async for entry in channel.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.webhook_update
            ):
                w = gdata("vega", "wlbots")
                if (
                    not str(entry.user.id) in w[str("Bots")]
                    and entry.user != channel.guild.owner
                    and enabled
                    and entry.user.bot
                    and not str(entry.user.id) in dop
                ):
                    try:
                        await entry.user.ban(
                            reason=f"{get_language(channel.guild.id,'[AntiBot] Редактирование вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                            delete_message_days=1,
                        )
                        lc = gdata("vega", "logchannel")
                        embed = discord.Embed(
                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Редактирование вебхука!')}\n\n**{get_language(channel.guild.id,'Информация о боте:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(url=entry.user.avatar.replace(size=1024))
                        embed.set_footer(
                            text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(lc[str(channel.guild.id)])
                            ).send(embed=embed)
                        except:
                            pass
                    except:
                        pass
        except:
            pass


# Логи бота
@client.event
async def on_guild_remove(guild):
    if client.user.id == 795551166393876481:
        try:
            owner = guild.owner
            embed = discord.Embed(
                title="Бот был удалён с сервера",
                description=f"**Сервер:** {guild.name}\n**ID сервера:** {guild.id}\n**Количество участников:** {len(guild.members) - 1}\n**Владелец:** {owner}\n**ID Владельца:** {owner.id}",
                color=discord.Colour.red()
            )
            embed.set_thumbnail(url=guild.icon)
            await client.get_channel(811963689677619230).send(embed=embed)
        except:
            pass
    else:
        pass


@client.event
async def on_member_remove(member):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        data = gdata("vega", "antibot")
        try:
            enabled = data[str(member.guild.id)]
        except KeyError:
            enabled = False
        if member.bot:
            lc = gdata("vega", "logchannel")
            # p = gdata('vega', 'passbots')
            """try:
                # Проверка пропуска
                if str(member.id) in p[str(member.guild.id)]:
                    p = gdata('vega', 'passbots')
                    p.update({str(member.guild.id):p[str(member.guild.id)].replace(str(f"<@!{member.id}>, "), '')})
                    wdata('vega', 'passbots', p)
                    embed = discord.Embed(color=0xcc1a1d)
                    embed.set_author(name=f"{get_language(member.guild.id, 'Пропуск')} {member} {get_language(member.guild.id, 'истек!')}", icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png")
                    embed.set_footer(text=f'ID: {member.id}')
                    try:
                        await client.get_channel(int(lc[str(member.guild.id)])).send(embed=embed)
                    except:
                        pass
                else:
                    pass
            except:
                pass"""

            # Кик пользователя
            wl = gdata("vega", "ignorebots")
            if str(member.guild.id) in wl:
                dop = wl[str(member.guild.id)]
            else:
                dop = ""
            try:
                async for entry in member.guild.audit_logs(
                    limit=1, action=discord.AuditLogAction.kick
                ):
                    w = gdata("vega", "wlbots")
                    lc = gdata("vega", "logchannel")
                    if (
                        not str(entry.user.id) in w[str("Bots")]
                        and entry.user != member.guild.owner
                        and enabled
                        and entry.user.bot
                        and not str(entry.user.id) in dop
                    ):
                        if enabled:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(member.guild.id,'[AntiBot] Кик пользователя!')} {get_language(member.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                embed = discord.Embed(
                                    description=f"{get_language(member.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot] Кик пользователя!')}\n\n**{get_language(member.guild.id,'Информация о боте:')}**\n{get_language(member.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                    color=0xFCC21B,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024)
                                )
                                embed.set_footer(
                                    text=f"{get_language(member.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(lc[str(member.guild.id)])
                                    ).send(embed=embed)
                                except:
                                    pass
                            except:
                                pass

                    try:
                        await member.guild.fetch_ban(member)
                        return
                    except discord.NotFound:
                        if not entry.user == client.get_user(795551166393876481):
                            embed = discord.Embed(
                                description=f"**{get_language(member.guild.id,'Пользователем:')}** {entry.user}\n**ID:** `{entry.user.id}`\n\n**{get_language(member.guild.id,'Информация о боте:')}**\n{get_language(member.guild.id,'Присоединился:')} <t:{int(member.joined_at.timestamp())}:F>\n{get_language(member.guild.id,'Создан:')} <t:{int(member.created_at.timestamp())}:F>",
                                color=0xF1A019,
                            )
                            embed.set_author(
                                name=f"{member} {get_language(member.guild.id,'кикнут!')}",
                                icon_url="https://i.postimg.cc/vZ12gJY4/kick.png",
                            )
                            embed.set_thumbnail(url=member.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(lc[str(member.guild.id)])
                                ).send(embed=embed)
                            except:
                                pass
            except:
                pass


# Авто загрузка белого списка ботов на канал
# VEGA - 806889107594674236
# @client.event
# async def autogetjson():
#    while True:
#        await asyncio.sleep(7200) #каждые 2 часа загружает файлы
#        a = client.get_channel(806889107594674236)
#        with open('message.txt', 'w') as f:
#            f.write(requests.get('https://vegabot.xyz/vegabot/data/whitelist.data').text)
#        await a.send(file=discord.File('message.txt'))


#        await a.send(file=discord.File(f'json/antibot.json'))
#        await a.send(file=discord.File(f'json/channel_rights.json'))
#        await a.send(file=discord.File(f'json/ignorebots.json'))
#        await a.send(file=discord.File(f'json/antiinvite.json'))
#        await a.send(file=discord.File(f'json/logchannel.json'))

# client.loop.create_task(autogetjson())


# Скачать json
# VEGA - 806889107594674236
# тест - 806889358740815895
# @client.command()
# @commands.guild_only()
# async def djson(ctx):
#    if ctx.author.id == 351020816466575372:
#        for file in os.listdir('json/'):
#            await client.get_channel(806889107594674236).send(file=discord.File(f'json/{file}'))


# Отправить сообщение пользователю в лс
# @client.command()
# @commands.guild_only()
# async def bd(ctx, user:discord.Member, *, message):
#    if ctx.author.id == 351020816466575372:
#        msg = ctx.message
#        try:
#            embed = discord.Embed(title='🛠 Сообщение от Разработчика:', description=f'{message}', color=0x1e1e1e)
#            await user.send(embed=embed)
#            await msg.add_reaction('<a:vega_check_mark:821700784927801394>')
#        except:
#            await msg.add_reaction('<a:vega_x:810843492266803230>')


# ban_image = ['https://cdn.discordapp.com/attachments/713751423128698950/804296020149141534/unknown.png']

try:
    asp = {}

    @client.event
    async def on_message(msg):
        user = msg.author

        # При упоминании бота, он напоминает свой префикс
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if msg.content.startswith(f"<@{client.user.id}>") or msg.content.startswith(
                f"<@!{client.user.id}>"
            ):
                embed = discord.Embed(
                    description=f"{get_language(msg.guild.id,'Префикс на данном сервере:')} `{prefix}`",
                    color=0x2F3136,
                )
                await msg.channel.send(embed=embed, delete_after=12.0)

            # Удаляет сообщения бота, который оффлайн.
            wl = gdata("vega", "ignorebots")
            if str(msg.id) in wl:
                dop = wl[str(msg.id)]
            else:
                dop = ""
            amsgdata = gdata("vega", "antimsg")
            try:
                enabled = amsgdata[str(msg.guild.id)]
            except KeyError:
                enabled = False
            if enabled:
                try:
                    if user.bot:
                        w = gdata("vega", "wlbots")
                        if (
                            not str(user.id) in w[str("Bots")]
                            and not str(user.id) in dop
                        ):
                            if msg.author.status == discord.Status.offline:
                                await msg.delete()
                        else:
                            pass
                    else:
                        pass
                except:
                    pass
            else:
                pass

        # Антиприглпшения на сервер!
        #    with open('json/antiinvite.json', 'r') as f:
        #        data = json.load(f)
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            data = gdata("vega", "antiinvite")
            try:
                enabled = data[str(msg.guild.id)]
            except KeyError:
                enabled = False
            if not msg.author.bot:
                if (
                    "discord.gg/" in msg.content.lower()
                    or "discord.com/invite/" in msg.content.lower()
                    or "discordapp.com/invite/" in msg.content.lower()
                ):
                    if msg.author != msg.guild.owner:
                        if enabled:
                            await msg.delete()
                        # embed = discord.Embed(title=f':warning: Пиар серверов Discord запрещен!', color=0xfcc21b)
                        # await msg.channel.send(embed=embed, delete_after=8.0)

        # Автоэмодзи в категории комментарии
        # 793014290835308554-VEGA комментарии
        # тестовый - 789346284628475904
        #    ID = 804022465932034128
        #    if msg.channel.id != ID:
        if msg.channel.id == 793014290835308554:
            if len(msg.content) > 5:
                await msg.add_reaction("👍")
                await asyncio.sleep(3)
                await msg.add_reaction("👎")
            else:
                await msg.delete()
                await msg.author.send(f"\❗ {user.mention}, оставьте нормальный отзыв.")

        # Автоэмодзи в категории Реклама
        # 775434430767956029-VEGA пиар сервера
        # Тестовый - 789346284628475905
        if msg.channel.id == 775434430767956029:
            if len(msg.content) > 24 and "https://discord.gg/" in msg.content:
                await msg.add_reaction("👍")
                await asyncio.sleep(3)
                await msg.add_reaction("👎")
            else:
                await msg.delete()
                await msg.author.send(
                    f":warning: {user.mention}, отсутствует ссылка на приглашение или текст слишком короткий!"
                )
        await client.process_commands(msg)

except:
    pass

    # Антиспам!
    """global author_msg_counts
    global asp

    wl = gdata('vega', 'ignorebots')
    if str(msg.guild.id) in wl:
        dop = wl[str(msg.guild.id)]
    else:
        dop = ''

    try:
        unix = asp[msg.author.id]
    except:
        unix = 0

    author_id = msg.author.id
    try:
        webhook_id = await client.fetch_webhook(msg.author.id)
    except discord.NotFound:
        return
    curr_time = datetime.datetime.now().timestamp() * 1000

    if not author_msg_times.get(author_id, False):
        author_msg_times[author_id] = []
    if not author_msg_times.get(webhook_id, False):
        author_msg_times[webhook_id] = []

    author_msg_times[author_id].append(curr_time)
    if not msg.author.bot:
        expr_time = curr_time - time_window_milliseconds
    if msg.author.bot:
        expr_time = curr_time - time_window_milliseconds_bot
    
    author_msg_times[webhook_id].append(curr_time)
    if webhook_id: 
        expr_time = curr_time - time_window_milliseconds_bot

    expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
    ]

    try:
        expired_msgs_webhook = [
            msg_time for msg_time in author_msg_times[webhook_id]
            if msg_time < expr_time
        ]
    except:
        pass

    for msg_time in expired_msgs:
        author_msg_times[author_id].remove(msg_time)

    for msg_time in expired_msgs_webhook:
        author_msg_times[webhook_id].remove(msg_time)

    #Антиспам для людей
    if not msg.author.bot:
        if len(author_msg_times[author_id]) > max_msg_per_window:
            await msg.delete()
        if unix < int(time.time()):
            if len(author_msg_times[author_id]) > max_msg_per_window:
                author_id = msg.author.mention
                await msg.channel.send(f"{author_id}, {get_language(msg.guild.id,'прекратите спамить!')}")
                asp[msg.author.id] = int(time.time()) + 50

    #Антиспам для ботов
    if msg.author.bot:
        w = gdata('vega', 'wlbots')
        if not str(author_id) in w[str("Bots")] and not str(author_id) in dop:
            if len(author_msg_times[author_id]) > max_msg_per_window_bot:
                try:
                    await msg.author_id.ban(reason=f"{get_language(msg.guild.id,'[AntiSpam] Спам')} {get_language(msg.guild.id,'Подозрительные действия со стороны бота!')}", delete_message_days=1)

                    lc = gdata('vega', 'logchannel')
                    embed = discord.Embed(description=f"{get_language(msg.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(msg.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {msg.author.id}`\n{get_language(msg.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {msg.author.id}`\n\n**{get_language(msg.guild.id,'Причина:')}**\n{get_language(msg.guild.id,'[AntiSpam] Спам')}\n\n**{get_language(msg.guild.id,'Информация о боте:')}**\n{get_language(msg.guild.id,'Создан:')} <t:{int(msg.author.created_at.timestamp())}:F>", color=0xfcc21b)
                    embed.set_author(name=f"{msg.author} {get_language(msg.guild.id,'был забанен функцией AntiBot')}", icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif")
                    embed.set_thumbnail(url=msg.author.avatar.replace(size=1024))
                    embed.set_footer(text=f"{get_language(msg.guild.id,'ID бота:')} {msg.author.id}")
                    try:
                        await client.get_channel(int(lc[str(msg.guild.id)])).send(embed=embed)
                    except:
                        pass
                except:
                    pass

    #Антиспам для вебхуков
    if webhook_id:
        if len(author_msg_times[webhook_id]) > max_msg_per_window_bot:
            try:
                lc = gdata('vega', 'logchannel')

                embed = discord.Embed(description=f"{get_language(msg.guild.id,'Подозрительные действия со стороны вебхука!')}\n**{get_language(msg.guild.id,'Причина:')}**\n{get_language(msg.guild.id,'[AntiSpam] Спам')}\n\n**{get_language(msg.guild.id,'Информация о вебхуке:')}**\n{get_language(msg.guild.id,'Создан:')} <t:{int(msg.webhook.created_at.timestamp())}:F>\n{get_language(msg.guild.id,'В канале:')} {msg.webhook.channel.mention}", color=0xfcc21b)
                embed.set_author(name=f"**{msg.webhook.name}** {get_language(msg.guild.id,'был удален функцией AntiSpam')}", icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif")
                embed.set_thumbnail(url=msg.webhook.avatar.replace(size=1024))
                embed.set_footer(text=f"{get_language(msg.guild.id,'ID вебхука:')} {msg.webhook_id}")
                try:
                    await client.get_channel(int(lc[str(msg.guild.id)])).send(embed=embed)
                except:
                    pass

                await msg.channel.webhook.delete()
                await msg.channel.send(f"{get_language(msg.guild.id,'Для предотвращения спама, был удален вебхук:')} **{msg.webhook.name}**")

            except:
                pass"""

"""
    #Команды для бампа сервера
    #-VEGA пиар сервера
    #Тестовый - 804022465932034128
#    if msg.channel.id == 804022465932034128:
#        words = ['s!up', '!bump']
#        ok = False
#        for word in words:
#            if word in msg.content:
#                ok = True
#        if not msg.author.bot:
#            if len(msg.content) >= 4 and ok:
#                pass
#            else:
#                await msg.delete()
    
    #Фильтр недействительных ссылок
    # 804022465932034128 - тестовый
#   if msg.channel.id == 804022465932034128:
#       for i in ban_image:
#           if i in msg.content:
#               await msg.delete()
"""


# Присоединение к боту по токену
client.run(config[cpath]["bot_token"])
