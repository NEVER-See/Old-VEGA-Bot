import asyncio
import datetime
import json
import os
import time
from tracemalloc import stop
from unittest import skip
#from termcolor import colored, cprint — для вывода красивого текста в консоль
#from colorama import init, Fore, Back, Style

import disnake as discord
import requests
#from discord import activity
#from discord import webhook
#from discord.channel import DMChannel
# from discord import utils
#from random import randint
from discord.ext import commands, tasks
from discord.utils import get
from disnake.ext import commands, tasks

from cache import *
# \/ convert, hmsd1, urlspotify
from helper import get_language, hmsd

#import re
#import typing
#import aiohttp
# import word
# import config

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


intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True
intents.webhooks = True


# Клиент — сам бот
#test_guilds=[824906215304986625, 826022179568615445, 779351525586632784]
prefix = "/"
#awl = gdata('vega', 'wlbots')
#acount = awl["Bots"].count(',')
with open('json/count_wlbots.json', 'r') as f:
    ct = json.load(f)
acount = ct["count_wlbots"]["count"]
client = commands.AutoShardedBot(
    intents=intents,
    command_prefix=prefix,
    shard_count=config["shard_count"],
    status=discord.Status.dnd,
    activity=discord.Activity(name=f"Bots wl: {acount} | vega-bot.ru", type=discord.ActivityType.watching),
)
#activity=discord.Game("loading..."),
client.remove_command("info")
client.remove_command("clear")
client.remove_command("help")

cpath = "release"
if config["debug_mode"]:
    cpath = "debug"


# Активиция MongoDB
with open("json/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)


# Коги — запуск команд
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        # try:
        client.load_extension("cogs." + file[:-3])
        print(f"\033[36m [ ЗАГРУЗКА ]  Cog загружен: {file[:-3]}\n\033[0m")
        """except:
            print(f"[ ОШИБКА ]  Cog не загружен: {file[:-3]}\n")"""


# Кол-во серверов и шардов, мониторинг бота
@tasks.loop(minutes=30)
async def update_sdc_stats():
    if client.user.id == 795551166393876481:
        API_ds_key = open(
            "important_information/Tokens/API_sd.txt", "r"
        ).readline()  # Проверить правильность написание указания файла по папкам
        try:
            r = requests.post(
                "https://api.server-discord.com/v2/bots/795551166393876481/stats",
                headers={"Authorization": f"SDC {API_ds_key}"},
                data={"shards": client.shard_count,
                      "servers": len(client.guilds)},
            )
            print(f"\033[36m [ ИНФО ]  Серверов: {len(client.guilds)}\n\033[0m")
            print(f"\033[36m [ ИНФО ]  Отправляю данные на BDSC {r}\n\033[0m")
        except Exception as e:
            print(f"\033[31m !!! [ ОШИБКА ]  Не удалось обновить счетчик из-за: {e}\n\033[0m")
            pass
    else:
        print("\033[36m [ ИНФО ]  Активирован тестовый бот! (Мониторинг: BSDC)\n\033[0m")
        pass


# Сайт обноволение
@tasks.loop(minutes=1)
async def update_stats():
    if client.user.id == 795551166393876481:
        try:
            with open('json/count_wlbots.json', 'r') as f:
                ct = json.load(f)
            count1 = ct["count_wlbots"]["count"]

            requests.post(
                "https://vega-bot.ru/updatesg.php",
                data={
                    "SERVERS": len(client.guilds),
                    "SHARDS": len(client.shards),
                    "USERS": len([m for m in client.users if not m.bot]),
                    "OWN1": client.get_user(351020816466575372),
                    "OWN2": client.get_user(750245767142441000),
                    "OWN3": client.get_user(777494101179629569),
                    "WLBOTS": count1,
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
            requests.get(f'https://vega-bot.ru/status/shards/update.php?s0p={int(shard0.latency * 1000)}&s0s={g0}&s1p={int(shard1.latency * 1000)}&s1s={g1}&avg={int(client.latency * 1000)}&s2s={g2}&avg2={int(client.latency * 1000)}&s3s={g3}&avg3={int(client.latency * 1000)}')"""
            print("\033[36m [ ИНФО ]  Сервера и шарды были обновлены на сайте!\n\033[0m")
        except:
            print("\033[31m [ ОШИБКА ]  Что-то пошло не так!\n\033[0m")
            pass
    else:
        print("\033[36m [ ИНФО ]  Активирован тестовый бот! (Сайт VEGA)\n\033[0m")
        pass


# Кик неверифицированных пользователей на сервере VEGA
@tasks.loop(seconds=10)
async def update_verify():
    meguild = client.get_guild(423107666253185024)
    if meguild:
        for member in [m for m in meguild.members if not m.bot and m.status == discord.Status.offline and not meguild.get_role(777795011177086986) in m.roles]:
            if member.status == discord.Status.offline:
                if meguild.get_role(777795011177086986) not in member.roles:
                    emb = discord.Embed(
                        title=f"<:kick:842447666990153828> Вы были изгнаны:", color=0xf1a019)
                    emb.add_field(name=f"С сервера:",
                                  value=f'{meguild.name}', inline=False)
                    emb.add_field(name=f"Модератором:",
                                  value=f'VEGA ⦡#7724', inline=False)
                    emb.add_field(
                        name=f"По причине:", value=f"Неверифицированный\n` Не в сети `", inline=False)
                    emb.add_field(
                        name=f"Просьба:", value=f"**При заходе на сервер, просим вас быть в сети для прохождения верификации!**", inline=False)
                    await member.send(embed=emb)
                    await member.kick()

                    emb = discord.Embed(
                        title=f"<:kick:842447666990153828> Кик", color=0xf1a019)
                    emb.add_field(name=f"Модератор:",
                                  value=f'VEGA ⦡#7724', inline=True)
                    emb.add_field(name=f"Пользователь:",
                                  value=f'{member.name}', inline=True)
                    emb.add_field(
                        name=f"Причина:", value=f"Неверифицированный\n` Не в сети `", inline=False)
                    emb.set_thumbnail(
                        url='https://i.postimg.cc/vZ12gJY4/kick.png')
                    await client.get_channel(934545389728698408).send(embed=emb)
                else:
                    print(f"{member.name} [{member.id}] — верифицирован!\n")
                    pass
            else:
                print(f"{member.name} [{member.id}] — в сети!\n")
                pass
    else:
        pass


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
        update_verify.start()
        # client.loop.create_task(refresh())
        print("\033[32m [ ЗАГРУЗКА ]  Запуск задач (tasks)...\n\033[0m")


global on_ready_start
on_ready_start = True
# Запуск бота


@client.event
async def on_ready():
    global on_ready_start
    if on_ready_start:
        # client.loop.create_task(update_stats())
        client.start_time = datetime.datetime.now()
        """
        count1 = w["Bots"].count(",")
        if count1:
            print(f"\033[36m [ ИНФО ]  Ботов в белом списке: {count1}\n")
        else:
            print("!!! [ ОШИБКА ]  Ботов в белом списке не обнаружено!\n")"""
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
                print("\033[5;32m >>>\033[0m\033[32m   [ ЗАПУСК ]  БОТ включен и готов к работе!\nㅤ\033[0m")
            else:
                channel = client.get_channel(
                    812666804441841684
                )  # получаем айди канала 812666804441841684
                await channel.send(
                    "\🔄**` RESTART `**\nБот **VEGA ⦡#7724** был запущен (деактивирован)!"
                )
                print(
                    f"\033[5;33m >>>\033[0m\033[33m   [ ЗАПУСК ]  В данный момент, бот деактивирован!\nㅤ\033[0m")
        except:
            print(
                "\033[5;31m >>>\033[0m\033[31m   [ ОШИБКА ]  Сообщение о запуске бота небыло доставлено!\nㅤ\033[0m")
            pass

        # Статус бота (не беспокоить, играет в v!help, смотрит за сервером VEGA ⦡)
        # guilds = await client.fetch_guilds(limit = None).flatten()
        # guilds = client.guilds

        # await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f"v!help | Bots wl: 300+ | vega-bot.ru"))

        on_ready_start = False
        while True:
            await asyncio.sleep(600)
            try:
                try:
                    enabled = deactivatedata[0]["Option"]
                except KeyError:
                    enabled = False
                if not enabled:
                    #w = wlbotsdata
                    #count = w["Bots"].count(",")
                    with open('json/count_wlbots.json', 'r') as f:
                        ct = json.load(f)
                    count1 = ct["count_wlbots"]["count"]
                    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(name=f"Bots wl: {count1} | vega-bot.ru", type=discord.ActivityType.watching))
                else:
                    await client.change_presence(status=discord.Status.idle, activity=discord.Game("DEACTIVATED"))
            except:
                pass
            """try:
                try:
                    enabled = deactivatedata[0]["Option"]
                except KeyError:
                    enabled = False
                if not enabled:
                    await client.change_presence(status=discord.Status.dnd, activity=discord.Game(f"vega-bot.ru | v!help"))
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
    if guild.id not in languagedata:
        if guild.region == "russia":
            language.add(guild.id, {"language": True})
        else:
            language.add(guild.id, {"language": False})
    else:
        pass
    try:
        enabled = languagedata[guild.id]["language"]
    except KeyError:
        enabled = False
    if not enabled:
        language.add(guild.id, {"language": False})
    else:
        pass

    version_bot = open("important_information/version_bot.txt", "r").readline()
    try:
        prefix = "/"
        embed = discord.Embed(
            title=f"{get_language(guild.id,'👋 Привет, спасибо что добавили меня!')}",
            description=f"{get_language(guild.id,'• Префикс на сервере')} `{prefix}`, {get_language(guild.id,'справка по командам')} `{prefix}help`.\n• {get_language(guild.id,'Сменить язык:')} `{prefix}{get_language(guild.id,'lang en')}`\n\n{get_language(guild.id,'**Описание:**')}\n{get_language(guild.id,'• Бот предназначен для защиты вашего сервера от участников и ботов! Включить функцию **AntiBot**: `/antibot on`. Включить функцию **AntiCrash**: `/anticrash on`. (Включить) Запретить редактирование сервера: `/edit-server on`.')} {get_language(guild.id,'(Данные команды может включить только Владелец сервера!).')}\n{get_language(guild.id,'Командой')} `{prefix}channel add {get_language(guild.id,'{#канал | ID канала}')}` {get_language(guild.id,'добавьте канал, в котором бот сможет отвечать на команды.')} {get_language(guild.id,'Советуем не убирать право Администратора у бота для корректной работы.')}\n{get_language(guild.id,'Для проверки ботов введите команду')} `{prefix}checkwl all`",
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
            value=f"{get_language(guild.id,'[Документация](https://never-see.gitbook.io/vega-bot/v/russian/)')}\n{get_language(guild.id,'[Сайт бота](https://vega-bot.ru/)')}\n{get_language(guild.id,'[Служба поддержки](https://discord.gg/8YhmtsYvpK)')}",
            inline=False
        )
        embed.set_thumbnail(
            url=client.get_user(795551166393876481).avatar.replace(size=1024)
        )
        embed.set_footer(
            icon_url=client.get_user(
                351020816466575372).avatar.replace(size=1024),
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
                if guild.icon != None:
                    embed.set_thumbnail(url=guild.icon)
                await client.get_channel(811963689677619230).send(embed=embed)
        except:
            pass
    else:
        pass

    
    ig = []
    prefix = "/"
    embed = discord.Embed(
        description=f"{get_language(guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется проверка ботов...')}",
        color=0xF4900C
    )
    msg = await first_allowed_channel(guild).send(embed=embed)
    new = await first_allowed_channel(guild).fetch_message(msg.id)
    for member in [m for m in guild.members if m.bot]:
        # try:
        if member.id not in wlbotsdata[0]["Bots"] and member.id not in ignorebotsdata[guild.id]["rights"]:
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
                try:
                    enabled = antibotdata[guild.id]["enabled"]
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

        url2 = "https://vega-bot.ru/"
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


# Перезапустить ког
@client.slash_command(name="reload",
    description="Restart the cog | Перезапустить ког",
    guild_ids=[826022179568615445],
    )
@commands.guild_only()
#@commands.guild_permissions(826022179568615445, users={351020816466575372: True})
async def reload(ctx,  cog_name: str = commands.Param(name="cog_name", description="Specify the cog | Укажите ког")):
    if ctx.author.id == 351020816466575372:
        try:
            client.unload_extension("cogs." + cog_name)
            client.load_extension("cogs." + cog_name)
            await ctx.send(f"Ког **{cog_name}** был перезапущен!", ephemeral=True)
        except:
            await ctx.send(f"Ошибка в обновлении кога [ `{cog_name}` ]!", ephemeral=True)
    else:
        embed = discord.Embed(
            description=f"**{get_language(ctx.guild.id,'Команда только для РАЗРАБОТЧИКОВ!')}**",
            color=0xCC1A1D,
        )
        await ctx.send(embed=embed, ephemeral=True)


# Тест
# @client.command(name="test", aliases=["тест"], pass_context=True)
# @commands.guild_only()
# @commands.bot_has_permissions(send_messages=True)
# async def test(ctx):
#    await send_graph(ctx, [1, 3, 5, 7, 9], [2, 4, 3, 6 ,7], title="Количество макарон")


# Оброботчик ошибок в оставшееся время команды (Неверная команда)

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
        #if await checkchannel(ctx):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                description=f"{get_language(ctx.guild.id,'⏱ Кулдаун команды. Будет активна через:')}\n    {format(hmsd(ctx, error.retry_after))}",
                color=0x2F3136,
            )
            await ctx.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"{get_language(ctx.guild.id,':warning: Отсутствуют необходимые полномочия!')}",
                color=0xFCC21B,
            )
            missing = str(error)
            missing = missing.replace("You are missing ", "")
            missing = missing.replace(
                " permission(s) to run this command.", "")
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

        if isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description=":warning: У бота отсутствую необходимые полномочия!",
                color=0xFCC21B,
            )
            missing = str(error)
            missing = missing.replace("Bot requires ", "")
            missing = missing.replace(
                " permission(s) to run this command.", "")
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
            #pass
            raise error
        """else:
            pass"""


"""@client.event
async def on_error(error, item, interaction):
    print(f"\n\n\033[31m ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤＥＲＲＯＲㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂\n\n\033[0m")
    try:
        print(f"\033[1;31m ERROR: \033[0m\033[31m {error}\033[0m")
    except:
        pass
    try:
        print(f"\n\n\033[1;31m Item:\033[0m\033[31m {item}\033[0m")
    except:
        pass
    try:
        print(f"\n\n\033[1;31m Interaction:\033[0m\033[31m {interaction}\033[0m")
    except:
        pass
    print(f"\n\033[31m ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂ㅤ▂\033[0m\n\n\033[31m")
    raise error"""



# AntiBot и Антикраш код:
# Весь код накрылся к хуям собычим из-за ебаного MongoDB с его новым кодом.
# Его нужно исправить и очень срочно


# Автокик новых ботов
@client.event
async def on_member_join(member):
    # Остальная команда антибота
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        """mr = gdata("vega", "muterole")
        w = gdata("vega", "mute_users")
        try:
            if str(member.id) in w[str(member.guild.id)]:
                muterole = member.guild.get_role(int(mr[str(member.guild.id)]))
                await member.add_roles(muterole)
            else:
                print("\033[36m [ ИНФО ]  Пользователь не замьючен!\n")
                pass
        except:
            print("!!! [ ОШИБКА ]  Роль мьюта не указана!\n")"""

        try:
            enabled_1 = hard_antibotdata[member.guild.id]["enabled"]
        except KeyError:
            enabled_1 = False
        try:
            enabled_2 = antibotdata[member.guild.id]["enabled"]
        except KeyError:
            enabled_2 = False
        if member.bot:
            try:
                if not enabled_1:
                    async for entry in member.guild.audit_logs(
                        limit=1, action=discord.AuditLogAction.bot_add
                    ):
                        if (
                            not member.id in wlbotsdata[0]["Bots"]
                        ):
                            if member.guild.id in ignorebotsdata:
                                if "rights" in ignorebotsdata[member.guild.id]:
                                    if member.id not in ignorebotsdata[member.guild.id]["rights"]:
                                        if enabled_2:
                                            if member.guild.id in passbotsdata:
                                                if "rights" in passbotsdata[member.guild.id]:
                                                    if member.id not in passbotsdata[member.guild.id]["rights"]:
                                                        # await asyncio.sleep(2)
                                                        await member.ban(
                                                            reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                            delete_message_days=1,
                                                        )
                                                        # await asyncio.sleep(5)
                                                        embed = discord.Embed(
                                                            description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                            color=0xFCC21B,
                                                        )
                                                        if member.public_flags.http_interactions_bot:
                                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                                        else:
                                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                                        if member.public_flags.verified_bot:
                                                            verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                        else:
                                                            verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                        if member.public_flags.spammer:
                                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                        else:
                                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                        embed.add_field(
                                                            name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                            value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                            inline=False,
                                                        )
                                                        embed.set_author(
                                                            name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                                        )
                                                        # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                                        embed.set_thumbnail(
                                                            url=member.avatar.replace(
                                                                size=1024)
                                                        )
                                                        embed.set_footer(
                                                            text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                                        )
                                                        try:
                                                            await client.get_channel(
                                                                int(logchanneldata[member.guild.id]["logchannel"])
                                                            ).send(embed=embed)
                                                        except:
                                                            pass
                                                    else:
                                                        if member.guild.id in passbotsdata:
                                                            if "rights" in passbotsdata[member.guild.id]:
                                                                if member.id in passbotsdata[member.guild.id]["rights"]:
                                                                    passbots.delete(member.guild.id, {"rights": member.id})
                                                        embed = discord.Embed(
                                                            description=f"<:arrow:847308468091879434> **{get_language(member.guild.id,'Пригласил бота:')}** {entry.user}\nㅤ **ID:** `{entry.user.id}`",
                                                            color=0xCC1A1D,
                                                        )
                                                        if member.public_flags.http_interactions_bot:
                                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                                        else:
                                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                                        if member.public_flags.verified_bot:
                                                            verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                        else:
                                                            verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                        if member.public_flags.spammer:
                                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                        else:
                                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                        embed.add_field(
                                                            name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                            value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                            inline=False,
                                                        )
                                                        embed.set_author(
                                                            name=f"{get_language(member.guild.id, 'Пропуск')} {member} {get_language(member.guild.id, 'истек!')}",
                                                            icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                        )
                                                        embed.set_footer(
                                                            text=f"ID: {member.id}")
                                                        try:
                                                            await client.get_channel(
                                                                int(logchanneldata[member.guild.id]["logchannel"])
                                                            ).send(embed=embed)
                                                        except:
                                                            pass
                                                else:
                                                    # await asyncio.sleep(2)
                                                    await member.ban(
                                                        reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                        delete_message_days=1,
                                                    )
                                                    # await asyncio.sleep(5)
                                                    embed = discord.Embed(
                                                        description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                        color=0xFCC21B,
                                                    )
                                                    if member.public_flags.http_interactions_bot:
                                                        http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                                    else:
                                                        http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                                    if member.public_flags.verified_bot:
                                                        verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                    else:
                                                        verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                    if member.public_flags.spammer:
                                                        spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                    else:
                                                        spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                    embed.add_field(
                                                        name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                        value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                        inline=False,
                                                    )
                                                    embed.set_author(
                                                        name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                                    )
                                                    # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                                    embed.set_thumbnail(
                                                        url=member.avatar.replace(
                                                            size=1024)
                                                    )
                                                    embed.set_footer(
                                                        text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                                    )
                                                    # try:
                                                    await client.get_channel(
                                                        int(logchanneldata[member.guild.id]["logchannel"])
                                                    ).send(embed=embed)
                                                    # except:
                                                    #     pass
                                            else:
                                                # await asyncio.sleep(2)
                                                print("-8")
                                                await member.ban(
                                                    reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                    delete_message_days=1,
                                                )
                                                # await asyncio.sleep(5)
                                                embed = discord.Embed(
                                                    description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                    color=0xFCC21B,
                                                )
                                                if member.public_flags.http_interactions_bot:
                                                    http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                                else:
                                                    http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                                if member.public_flags.verified_bot:
                                                    verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                else:
                                                    verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                if member.public_flags.spammer:
                                                    spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                else:
                                                    spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                embed.add_field(
                                                    name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                    value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                    inline=False,
                                                )
                                                embed.set_author(
                                                    name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                                )
                                                # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                                embed.set_thumbnail(
                                                    url=member.avatar.replace(
                                                        size=1024)
                                                )
                                                embed.set_footer(
                                                    text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                                )
                                                try:
                                                    await client.get_channel(
                                                        int(logchanneldata[member.guild.id]["logchannel"])
                                                    ).send(embed=embed)
                                                except:
                                                    pass
                                    else:
                                        embed = discord.Embed(
                                            description=f"<:arrow:847308468091879434> **{get_language(member.guild.id,'Пригласил бота:')}** {entry.user}\nㅤ **ID:** `{entry.user.id}`",
                                            color=discord.Colour.blue(),
                                        )
                                        if member.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                        if member.public_flags.verified_bot:
                                            verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if member.public_flags.spammer:
                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{member} {get_language(member.guild.id,'игнорируется на данном сервере!')}",
                                            icon_url="https://cdn.discordapp.com/attachments/713751423128698950/904448009583100005/invisible1600.png",
                                        )
                                        embed.set_thumbnail(
                                            url=member.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                        )
                                        try:
                                            await client.get_channel(
                                                int(logchanneldata[member.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                else:
                                    if enabled_2:
                                        if member.guild.id in passbotsdata:
                                            if "rights" in passbotsdata[member.guild.id]:
                                                if member.id not in passbotsdata[member.guild.id]["rights"]:
                                                    # await asyncio.sleep(2)
                                                    await member.ban(
                                                        reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                        delete_message_days=1,
                                                    )
                                                    # await asyncio.sleep(5)
                                                    embed = discord.Embed(
                                                        description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                        color=0xFCC21B,
                                                    )
                                                    if member.public_flags.http_interactions_bot:
                                                        http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                                    else:
                                                        http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                                    if member.public_flags.verified_bot:
                                                        verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                    else:
                                                        verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                    if member.public_flags.spammer:
                                                        spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                    else:
                                                        spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                    embed.add_field(
                                                        name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                        value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                        inline=False,
                                                    )
                                                    embed.set_author(
                                                        name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                                    )
                                                    # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                                    embed.set_thumbnail(
                                                        url=member.avatar.replace(
                                                            size=1024)
                                                    )
                                                    embed.set_footer(
                                                        text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                                    )
                                                    try:
                                                        await client.get_channel(
                                                            int(logchanneldata[member.guild.id]["logchannel"])
                                                        ).send(embed=embed)
                                                    except:
                                                        pass
                                                else:
                                                    if member.guild.id in passbotsdata:
                                                        if "rights" in passbotsdata[member.guild.id]:
                                                            if member.id in passbotsdata[member.guild.id]["rights"]:
                                                                passbots.delete(member.guild.id, {"rights": member.id})
                                                    embed = discord.Embed(
                                                        description=f"<:arrow:847308468091879434> **{get_language(member.guild.id,'Пригласил бота:')}** {entry.user}\nㅤ **ID:** `{entry.user.id}`",
                                                        color=0xCC1A1D,
                                                    )
                                                    if member.public_flags.http_interactions_bot:
                                                        http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                                    else:
                                                        http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                                    if member.public_flags.verified_bot:
                                                        verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                    else:
                                                        verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                    if member.public_flags.spammer:
                                                        spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                    else:
                                                        spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                    embed.add_field(
                                                        name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                        value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                        inline=False,
                                                    )
                                                    embed.set_author(
                                                        name=f"{get_language(member.guild.id, 'Пропуск')} {member} {get_language(member.guild.id, 'истек!')}",
                                                        icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                    )
                                                    embed.set_footer(
                                                        text=f"ID: {member.id}")
                                                    try:
                                                        await client.get_channel(
                                                            int(logchanneldata[member.guild.id]["logchannel"])
                                                        ).send(embed=embed)
                                                    except:
                                                        pass
                                            else:
                                                # await asyncio.sleep(2)
                                                await member.ban(
                                                    reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                    delete_message_days=1,
                                                )
                                                # await asyncio.sleep(5)
                                                embed = discord.Embed(
                                                    description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                    color=0xFCC21B,
                                                )
                                                if member.public_flags.http_interactions_bot:
                                                    http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                                else:
                                                    http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                                if member.public_flags.verified_bot:
                                                    verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                else:
                                                    verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                if member.public_flags.spammer:
                                                    spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                else:
                                                    spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                embed.add_field(
                                                    name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                    value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                    inline=False,
                                                )
                                                embed.set_author(
                                                    name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                                )
                                                # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                                embed.set_thumbnail(
                                                    url=member.avatar.replace(
                                                        size=1024)
                                                )
                                                embed.set_footer(
                                                    text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                                )
                                                try:
                                                    await client.get_channel(
                                                        int(logchanneldata[member.guild.id]["logchannel"])
                                                    ).send(embed=embed)
                                                except:
                                                    pass
                                        else:
                                            # await asyncio.sleep(2)
                                            await member.ban(
                                                reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                delete_message_days=1,
                                            )
                                            # await asyncio.sleep(5)
                                            embed = discord.Embed(
                                                description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                color=0xFCC21B,
                                            )
                                            if member.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                            if member.public_flags.verified_bot:
                                                verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if member.public_flags.spammer:
                                                spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                inline=False,
                                            )
                                            embed.set_author(
                                                name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                            )
                                            # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                            embed.set_thumbnail(
                                                url=member.avatar.replace(
                                                    size=1024)
                                            )
                                            embed.set_footer(
                                                text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                            )
                                            try:
                                                await client.get_channel(
                                                    int(logchanneldata[member.guild.id]["logchannel"])
                                                ).send(embed=embed)
                                            except:
                                                pass
                            else:
                                if enabled_2:
                                    if member.guild.id in passbotsdata:
                                        if "rights" in passbotsdata[member.guild.id]:
                                            if member.id not in passbotsdata[member.guild.id]["rights"]:
                                                # await asyncio.sleep(2)
                                                await member.ban(
                                                    reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                    delete_message_days=1,
                                                )
                                                # await asyncio.sleep(5)
                                                embed = discord.Embed(
                                                    description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                    color=0xFCC21B,
                                                )
                                                if member.public_flags.http_interactions_bot:
                                                    http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                                else:
                                                    http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                                if member.public_flags.verified_bot:
                                                    verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                else:
                                                    verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                if member.public_flags.spammer:
                                                    spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                else:
                                                    spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                embed.add_field(
                                                    name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                    value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                    inline=False,
                                                )
                                                embed.set_author(
                                                    name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                                )
                                                # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                                embed.set_thumbnail(
                                                    url=member.avatar.replace(
                                                        size=1024)
                                                )
                                                embed.set_footer(
                                                    text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                                )
                                                try:
                                                    await client.get_channel(
                                                        int(logchanneldata[member.guild.id]["logchannel"])
                                                    ).send(embed=embed)
                                                except:
                                                    pass
                                            else:
                                                if member.guild.id in passbotsdata:
                                                    if "rights" in passbotsdata[member.guild.id]:
                                                        if member.id in passbotsdata[member.guild.id]["rights"]:
                                                            passbots.delete(member.guild.id, {"rights": member.id})
                                                embed = discord.Embed(
                                                    description=f"<:arrow:847308468091879434> **{get_language(member.guild.id,'Пригласил бота:')}** {entry.user}\nㅤ **ID:** `{entry.user.id}`",
                                                    color=0xCC1A1D,
                                                )
                                                if member.public_flags.http_interactions_bot:
                                                    http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                                else:
                                                    http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                                if member.public_flags.verified_bot:
                                                    verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                else:
                                                    verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                if member.public_flags.spammer:
                                                    spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                else:
                                                    spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                embed.add_field(
                                                    name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                    value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                    inline=False,
                                                )
                                                embed.set_author(
                                                    name=f"{get_language(member.guild.id, 'Пропуск')} {member} {get_language(member.guild.id, 'истек!')}",
                                                    icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                )
                                                embed.set_footer(
                                                    text=f"ID: {member.id}")
                                                try:
                                                    await client.get_channel(
                                                        int(logchanneldata[member.guild.id]["logchannel"])
                                                    ).send(embed=embed)
                                                except:
                                                    pass
                                        else:
                                            # await asyncio.sleep(2)
                                            await member.ban(
                                                reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                delete_message_days=1,
                                            )
                                            # await asyncio.sleep(5)
                                            embed = discord.Embed(
                                                description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                                color=0xFCC21B,
                                            )
                                            if member.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                            if member.public_flags.verified_bot:
                                                verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if member.public_flags.spammer:
                                                spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                                inline=False,
                                            )
                                            embed.set_author(
                                                name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                            )
                                            # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                            embed.set_thumbnail(
                                                url=member.avatar.replace(
                                                    size=1024)
                                            )
                                            embed.set_footer(
                                                text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                            )
                                            try:
                                                await client.get_channel(
                                                    int(logchanneldata[member.guild.id]["logchannel"])
                                                ).send(embed=embed)
                                            except:
                                                pass
                                    else:
                                        # await asyncio.sleep(2)
                                        await member.ban(
                                            reason=f"{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                            delete_message_days=1,
                                        )
                                        # await asyncio.sleep(5)
                                        embed = discord.Embed(
                                            description=f"{get_language(member.guild.id,'Видимо бота нет в белом списке или он не игнорируется.')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {member.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {member.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                                            color=0xFCC21B,
                                        )
                                        if member.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                        if member.public_flags.verified_bot:
                                            verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if member.public_flags.spammer:
                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{member} {get_language(member.guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        # embed.add_field(name='<:arrow:847308468091879434> Приглашал бота:', value=f'{entry.user.mention}\n{entry.user}', inline=False)
                                        embed.set_thumbnail(
                                            url=member.avatar.replace(
                                                size=1024)
                                        )
                                        embed.set_footer(
                                            text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                                        )
                                        try:
                                            await client.get_channel(
                                                int(logchanneldata[member.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                        else:
                            embed = discord.Embed(
                                description=f"<:arrow:847308468091879434> **{get_language(member.guild.id,'Пригласил бота:')}** {entry.user}\nㅤ **ID:** `{entry.user.id}`",
                                color=discord.Colour.green(),
                            )
                            if member.public_flags.http_interactions_bot:
                                http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                            else:
                                http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                            if member.public_flags.verified_bot:
                                verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                            else:
                                verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                            if member.public_flags.spammer:
                                spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                            else:
                                spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                            embed.add_field(
                                name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                                inline=False,
                            )
                            embed.set_author(
                                name=f"{member} {get_language(member.guild.id,'находится в белом списке!')}",
                                icon_url="https://cdn.discordapp.com/attachments/713751423128698950/904452846664183858/wl_bots.png",
                            )
                            embed.set_thumbnail(
                                url=member.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(member.guild.id,'ID бота:')} {member.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(logchanneldata[member.guild.id]["logchannel"])
                                ).send(embed=embed)
                            except:
                                pass
                else:
                    async for entry in member.guild.audit_logs(
                        limit=1, action=discord.AuditLogAction.bot_add
                    ):
                        await member.ban(
                            reason=f"{get_language(member.guild.id,'[HARD-AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                            delete_message_days=1,
                        )
                        # await asyncio.sleep(5)
                        embed = discord.Embed(
                            description=f"**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[HARD-AntiBot]ㅤПригласил бота:')} {entry.user}ㅤ(ID: {entry.user.id})",
                            color=0xFCC21B,
                        )
                        if member.public_flags.http_interactions_bot:
                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                        else:
                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                        if member.public_flags.verified_bot:
                            verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                        else:
                            verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                        if member.public_flags.spammer:
                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                        else:
                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                        embed.add_field(
                            name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                            value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(member.joined_at.timestamp())}:D> *(<t:{int(member.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(member.created_at.timestamp())}:D> *(<t:{int(member.created_at.timestamp())}:R>)*",
                            inline=False,
                        )
                        embed.set_author(
                            name=f"{member} {get_language(member.guild.id,'был забанен функцией HARD-AntiBot')}",
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
                                int(logchanneldata[member.guild.id]["logchannel"])
                            ).send(embed=embed)
                        except:
                            pass
            except:
                pass

# Удаление канала
@client.event
async def on_guild_channel_delete(channel):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[channel.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            async for entry in channel.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_delete
            ):
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != channel.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if channel.guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[channel.guild.id]:
                            if entry.user.id not in ignorebotsdata[channel.guild.id]["rights"]:
                                vega = client.get_guild(channel.guild.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        if isinstance(channel, discord.CategoryChannel):
                                            await channel.clone(
                                                name=None,
                                                reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                            )
                                        elif not channel.category:
                                            await channel.clone(
                                                name=None,
                                                reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                            )
                                        else:
                                            if isinstance(channel, discord.TextChannel):
                                                await channel.guild.create_text_channel(
                                                    category=get(
                                                        channel.guild.categories,
                                                        name=channel.category.name,
                                                    ),
                                                    name=channel.name,
                                                    topic=channel.topic,
                                                    nsfw=channel.nsfw,
                                                    overwrites=channel.overwrites,
                                                    position=channel.position,
                                                    slowmode_delay=channel.slowmode_delay,
                                                )
                                            elif isinstance(channel, discord.VoiceChannel):
                                                await channel.guild.create_voice_channel(
                                                    category=get(
                                                        channel.guild.categories,
                                                        name=channel.category.name,
                                                    ),
                                                    name=channel.name,
                                                    bitrate=channel.bitrate,
                                                    overwrites=channel.overwrites,
                                                    position=channel.position,
                                                    user_limit=channel.user_limit,
                                                )
                                            await channel.edit(
                                                category=get(
                                                    channel.guild.categories, name=channel.category.name
                                                )
                                            )
                                except:
                                    if isinstance(channel, discord.CategoryChannel):
                                        await channel.clone(
                                            name=None,
                                            reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                        )
                                    elif not channel.category:
                                        await channel.clone(
                                            name=None,
                                            reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                        )
                                    else:
                                        if isinstance(channel, discord.TextChannel):
                                            await channel.guild.create_text_channel(
                                                category=get(
                                                    channel.guild.categories,
                                                    name=channel.category.name,
                                                ),
                                                name=channel.name,
                                                topic=channel.topic,
                                                nsfw=channel.nsfw,
                                                overwrites=channel.overwrites,
                                                position=channel.position,
                                                slowmode_delay=channel.slowmode_delay,
                                            )
                                        elif isinstance(channel, discord.VoiceChannel):
                                            await channel.guild.create_voice_channel(
                                                category=get(
                                                    channel.guild.categories,
                                                    name=channel.category.name,
                                                ),
                                                name=channel.name,
                                                bitrate=channel.bitrate,
                                                overwrites=channel.overwrites,
                                                position=channel.position,
                                                user_limit=channel.user_limit,
                                            )
                                        await channel.edit(
                                            category=get(
                                                channel.guild.categories, name=channel.category.name
                                            )
                                        )
                                if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(
                                                int(logchanneldata[channel.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                        else:
                            vega = client.get_guild(channel.guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    if isinstance(channel, discord.CategoryChannel):
                                        await channel.clone(
                                            name=None,
                                            reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                        )
                                    elif not channel.category:
                                        await channel.clone(
                                            name=None,
                                            reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                        )
                                    else:
                                        if isinstance(channel, discord.TextChannel):
                                            await channel.guild.create_text_channel(
                                                category=get(
                                                    channel.guild.categories,
                                                    name=channel.category.name,
                                                ),
                                                name=channel.name,
                                                topic=channel.topic,
                                                nsfw=channel.nsfw,
                                                overwrites=channel.overwrites,
                                                position=channel.position,
                                                slowmode_delay=channel.slowmode_delay,
                                            )
                                        elif isinstance(channel, discord.VoiceChannel):
                                            await channel.guild.create_voice_channel(
                                                category=get(
                                                    channel.guild.categories,
                                                    name=channel.category.name,
                                                ),
                                                name=channel.name,
                                                bitrate=channel.bitrate,
                                                overwrites=channel.overwrites,
                                                position=channel.position,
                                                user_limit=channel.user_limit,
                                            )
                                        await channel.edit(
                                            category=get(
                                                channel.guild.categories, name=channel.category.name
                                            )
                                        )
                            except:
                                if isinstance(channel, discord.CategoryChannel):
                                    await channel.clone(
                                        name=None,
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                    )
                                elif not channel.category:
                                    await channel.clone(
                                        name=None,
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                    )
                                else:
                                    if isinstance(channel, discord.TextChannel):
                                        await channel.guild.create_text_channel(
                                            category=get(
                                                channel.guild.categories,
                                                name=channel.category.name,
                                            ),
                                            name=channel.name,
                                            topic=channel.topic,
                                            nsfw=channel.nsfw,
                                            overwrites=channel.overwrites,
                                            position=channel.position,
                                            slowmode_delay=channel.slowmode_delay,
                                        )
                                    elif isinstance(channel, discord.VoiceChannel):
                                        await channel.guild.create_voice_channel(
                                            category=get(
                                                channel.guild.categories,
                                                name=channel.category.name,
                                            ),
                                            name=channel.name,
                                            bitrate=channel.bitrate,
                                            overwrites=channel.overwrites,
                                            position=channel.position,
                                            user_limit=channel.user_limit,
                                        )
                                    await channel.edit(
                                        category=get(
                                            channel.guild.categories, name=channel.category.name
                                        )
                                    )
                            if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(logchanneldata[channel.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(channel.guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                if isinstance(channel, discord.CategoryChannel):
                                    await channel.clone(
                                        name=None,
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                    )
                                elif not channel.category:
                                    await channel.clone(
                                        name=None,
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                    )
                                else:
                                    if isinstance(channel, discord.TextChannel):
                                        await channel.guild.create_text_channel(
                                            category=get(
                                                channel.guild.categories,
                                                name=channel.category.name,
                                            ),
                                            name=channel.name,
                                            topic=channel.topic,
                                            nsfw=channel.nsfw,
                                            overwrites=channel.overwrites,
                                            position=channel.position,
                                            slowmode_delay=channel.slowmode_delay,
                                        )
                                    elif isinstance(channel, discord.VoiceChannel):
                                        await channel.guild.create_voice_channel(
                                            category=get(
                                                channel.guild.categories,
                                                name=channel.category.name,
                                            ),
                                            name=channel.name,
                                            bitrate=channel.bitrate,
                                            overwrites=channel.overwrites,
                                            position=channel.position,
                                            user_limit=channel.user_limit,
                                        )
                                    await channel.edit(
                                        category=get(
                                            channel.guild.categories, name=channel.category.name
                                        )
                                    )
                        except:
                            if isinstance(channel, discord.CategoryChannel):
                                await channel.clone(
                                    name=None,
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                )
                            elif not channel.category:
                                await channel.clone(
                                    name=None,
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                )
                            else:
                                if isinstance(channel, discord.TextChannel):
                                    await channel.guild.create_text_channel(
                                        category=get(
                                            channel.guild.categories,
                                            name=channel.category.name,
                                        ),
                                        name=channel.name,
                                        topic=channel.topic,
                                        nsfw=channel.nsfw,
                                        overwrites=channel.overwrites,
                                        position=channel.position,
                                        slowmode_delay=channel.slowmode_delay,
                                    )
                                elif isinstance(channel, discord.VoiceChannel):
                                    await channel.guild.create_voice_channel(
                                        category=get(
                                            channel.guild.categories,
                                            name=channel.category.name,
                                        ),
                                        name=channel.name,
                                        bitrate=channel.bitrate,
                                        overwrites=channel.overwrites,
                                        position=channel.position,
                                        user_limit=channel.user_limit,
                                    )
                                await channel.edit(
                                    category=get(
                                        channel.guild.categories, name=channel.category.name
                                    )
                                )
                        if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Удаление каналов!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[channel.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[channel.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            try:
                enabled_2 = editserverdata[channel.guild.id]["enabled"]
            except KeyError:
                enabled_2 = False

            async for entry in channel.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_delete
            ):
                if (
                    entry.user != channel.guild.owner
                    and enabled
                    and enabled_2
                    and not entry.user.bot
                ):
                    vega = client.get_guild(channel.guild.id).me
                    try:
                        if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                with open('json/msg_appeal.json', 'r') as f:
                                    ma = json.load(f)
                                text = ma[str(channel.guild.id)]["appeal"]
                                embed = discord.Embed(
                                    title=f"{get_language(channel.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                    color=0xFF2B2B,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'На сервере:')}",
                                    value=f"{channel.guild.name}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'Модератором:')}",
                                    value=f"VEGA ⦡#7724",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'По причине:')}",
                                    value=f"{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')}\n`{get_language(channel.guild.id,'Редактирование сервера запрещено!')}`",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'Владелец сервера:')}",
                                    value=f"{channel.guild.owner}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'Апелляция:')}",
                                    value=f"{text}",
                                    inline=False,
                                )
                                await entry.user.send(embed=embed)
                                await entry.user.ban(
                                    reason=f"{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')}\n\n**{get_language(channel.guild.id,'Информация об участнике:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                    color=0xFCC21B,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiCrash')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(channel.guild.id,'ID участника:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[channel.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                            except:
                                pass
                        if vega.top_role >= entry.user.top_role:
                            if isinstance(channel, discord.CategoryChannel):
                                await channel.clone(
                                    name=None,
                                    reason=f"{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')}",
                                )
                                return
                            elif not channel.category:
                                await channel.clone(
                                    name=None,
                                    reason=f"{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')}",
                                )
                                return
                            else:
                                if isinstance(channel, discord.TextChannel):
                                    await channel.guild.create_text_channel(
                                        category=get(
                                            channel.guild.categories,
                                            name=channel.category.name,
                                        ),
                                        name=channel.name,
                                        topic=channel.topic,
                                        nsfw=channel.nsfw,
                                        overwrites=channel.overwrites,
                                        position=channel.position,
                                        slowmode_delay=channel.slowmode_delay,
                                    )
                                    return
                                elif isinstance(channel, discord.VoiceChannel):
                                    await channel.guild.create_voice_channel(
                                        category=get(
                                            channel.guild.categories,
                                            name=channel.category.name,
                                        ),
                                        name=channel.name,
                                        bitrate=channel.bitrate,
                                        overwrites=channel.overwrites,
                                        position=channel.position,
                                        user_limit=channel.user_limit,
                                    )
                                    return
                                await channel.edit(
                                    category=get(
                                        channel.guild.categories, name=channel.category.name
                                    )
                                )
                                return
                    except:
                        if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                with open('json/msg_appeal.json', 'r') as f:
                                    ma = json.load(f)
                                text = ma[str(channel.guild.id)]["appeal"]
                                embed = discord.Embed(
                                    title=f"{get_language(channel.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                    color=0xFF2B2B,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'На сервере:')}",
                                    value=f"{channel.guild.name}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'Модератором:')}",
                                    value=f"VEGA ⦡#7724",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'По причине:')}",
                                    value=f"{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')}\n`{get_language(channel.guild.id,'Редактирование сервера запрещено!')}`",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'Владелец сервера:')}",
                                    value=f"{channel.guild.owner}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(channel.guild.id,'Апелляция:')}",
                                    value=f"{text}",
                                    inline=False,
                                )
                                await entry.user.send(embed=embed)
                                await entry.user.ban(
                                    reason=f"{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')}\n\n**{get_language(channel.guild.id,'Информация об участнике:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                    color=0xFCC21B,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiCrash')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(channel.guild.id,'ID участника:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[channel.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                            except:
                                pass
                        if isinstance(channel, discord.CategoryChannel):
                            await channel.clone(
                                name=None,
                                reason=f"{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')}",
                            )
                            return
                        elif not channel.category:
                            await channel.clone(
                                name=None,
                                reason=f"{get_language(channel.guild.id,'[AntiCrash] Удаление каналов!')}",
                            )
                            return
                        else:
                            if isinstance(channel, discord.TextChannel):
                                await channel.guild.create_text_channel(
                                    category=get(
                                        channel.guild.categories,
                                        name=channel.category.name,
                                    ),
                                    name=channel.name,
                                    topic=channel.topic,
                                    nsfw=channel.nsfw,
                                    overwrites=channel.overwrites,
                                    position=channel.position,
                                    slowmode_delay=channel.slowmode_delay,
                                )
                                return
                            elif isinstance(channel, discord.VoiceChannel):
                                await channel.guild.create_voice_channel(
                                    category=get(
                                        channel.guild.categories,
                                        name=channel.category.name,
                                    ),
                                    name=channel.name,
                                    bitrate=channel.bitrate,
                                    overwrites=channel.overwrites,
                                    position=channel.position,
                                    user_limit=channel.user_limit,
                                )
                                return
                            await channel.edit(
                                category=get(
                                    channel.guild.categories, name=channel.category.name
                                )
                            )
                            return
        except:
            pass

# Создание канала
@client.event
async def on_guild_channel_create(channel):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[channel.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            async for entry in channel.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_create
            ):
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != channel.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if channel.guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[channel.guild.id]:
                            if not entry.user.id in ignorebotsdata[channel.guild.id]["rights"]:
                                vega = client.get_guild(channel.guild.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        await channel.delete(
                                            reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}",
                                        )
                                except:
                                    await channel.delete(
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}",
                                    )
                                if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(
                                                int(logchanneldata[channel.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                        else:
                            vega = client.get_guild(channel.guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await channel.delete(
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}",
                                    )
                            except:
                                await channel.delete(
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}",
                                )
                            if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(logchanneldata[channel.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(channel.guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await channel.delete(
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}",
                                )
                        except:
                            await channel.delete(
                                reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}",
                            )
                        if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Создание каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Создание каналов!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[channel.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[channel.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            try:
                enabled_2 = editserverdata[channel.guild.id]["enabled"]
            except KeyError:
                enabled_2 = False

            async for entry in channel.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_create
            ):
                if (
                    entry.user != channel.guild.owner
                    and enabled
                    and enabled_2
                    and not entry.user.bot
                ):
                    vega = client.get_guild(channel.guild.id).me
                    try:
                        if vega.top_role >= entry.user.top_role:
                            await channel.delete(
                                reason=f"{get_language(channel.guild.id,'[AntiCrash] Создание каналов!')}",
                            )
                    except:
                        await channel.delete(
                            reason=f"{get_language(channel.guild.id,'[AntiCrash] Создание каналов!')}",
                        )
                    if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                        try:
                            with open('json/msg_appeal.json', 'r') as f:
                                ma = json.load(f)
                            text = ma[str(channel.guild.id)]["appeal"]
                            embed = discord.Embed(
                                title=f"{get_language(channel.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                color=0xFF2B2B,
                            )
                            embed.add_field(
                                name=f"{get_language(channel.guild.id,'На сервере:')}",
                                value=f"{channel.guild.name}",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(channel.guild.id,'Модератором:')}",
                                value=f"VEGA ⦡#7724",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(channel.guild.id,'По причине:')}",
                                value=f"{get_language(channel.guild.id,'[AntiCrash] Создание каналов!')}\n`{get_language(channel.guild.id,'Редактирование сервера запрещено!')}`",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(channel.guild.id,'Владелец сервера:')}",
                                value=f"{channel.guild.owner}",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(channel.guild.id,'Апелляция:')}",
                                value=f"{text}",
                                inline=False,
                            )
                            try:
                                await entry.user.send(embed=embed)
                            except:
                                pass

                            await entry.user.ban(
                                reason=f"{get_language(channel.guild.id,'[AntiCrash] Создание каналов!')} {get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}",
                                delete_message_days=1,
                            )
                            
                            embed = discord.Embed(
                                description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiCrash] Создание каналов!')}\n\n**{get_language(channel.guild.id,'Информация об участнике:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                color=0xFCC21B,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiCrash')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(channel.guild.id,'ID участника:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(logchanneldata[channel.guild.id]["logchannel"])
                                ).send(embed=embed)
                            except:
                                pass
                            return
                        except:
                            pass
        except:
            pass

# Обновление канала
@client.event
async def on_guild_channel_update(before, after):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[after.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            async for entry in after.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_update
            ):
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != after.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if after.guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[after.guild.id]:
                            if not entry.user.id in ignorebotsdata[after.guild.id]["rights"]:
                                vega = client.get_guild(after.guild.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        if isinstance(after, discord.TextChannel):
                                            # await after.guild.update(
                                            await after.edit(
                                                name=before.name,
                                                type=before.type,
                                                position=before.position,
                                                nsfw=before.nsfw,
                                                slowmode_delay=before.slowmode_delay,
                                                overwrites=before.overwrites,
                                                topic=before.topic,
                                                default_auto_archive_duration=before.default_auto_archive_duration,
                                                reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                            )
                                        else:
                                            if isinstance(after, discord.VoiceChannel):
                                                await after.edit(
                                                    name=before.name,
                                                    type=before.type,
                                                    position=before.position,
                                                    overwrites=before.overwrites,
                                                    bitrate=before.bitrate,
                                                    rtc_region=before.rtc_region,
                                                    video_quality_mode=before.video_quality_mode,
                                                    reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                                )
                                except:
                                    if isinstance(after, discord.TextChannel):
                                        # await after.guild.update(
                                        await after.edit(
                                            name=before.name,
                                            type=before.type,
                                            position=before.position,
                                            nsfw=before.nsfw,
                                            slowmode_delay=before.slowmode_delay,
                                            overwrites=before.overwrites,
                                            topic=before.topic,
                                            default_auto_archive_duration=before.default_auto_archive_duration,
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                        )
                                    else:
                                        if isinstance(after, discord.VoiceChannel):
                                            await after.edit(
                                                name=before.name,
                                                type=before.type,
                                                position=before.position,
                                                overwrites=before.overwrites,
                                                bitrate=before.bitrate,
                                                rtc_region=before.rtc_region,
                                                video_quality_mode=before.video_quality_mode,
                                                reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                            )
                                if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(after.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(after.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(after.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(after.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(after.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(after.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(after.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(after.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(after.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(int(logchanneldata[after.guild.id]["logchannel"])).send(
                                                embed=embed
                                            )
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                        else:
                            vega = client.get_guild(after.guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    if isinstance(after, discord.TextChannel):
                                        # await after.guild.update(
                                        await after.edit(
                                            name=before.name,
                                            type=before.type,
                                            position=before.position,
                                            nsfw=before.nsfw,
                                            slowmode_delay=before.slowmode_delay,
                                            overwrites=before.overwrites,
                                            topic=before.topic,
                                            default_auto_archive_duration=before.default_auto_archive_duration,
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                        )
                                    else:
                                        if isinstance(after, discord.VoiceChannel):
                                            await after.edit(
                                                name=before.name,
                                                type=before.type,
                                                position=before.position,
                                                overwrites=before.overwrites,
                                                bitrate=before.bitrate,
                                                rtc_region=before.rtc_region,
                                                video_quality_mode=before.video_quality_mode,
                                                reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                            )
                            except:
                                if isinstance(after, discord.TextChannel):
                                    # await after.guild.update(
                                    await after.edit(
                                        name=before.name,
                                        type=before.type,
                                        position=before.position,
                                        nsfw=before.nsfw,
                                        slowmode_delay=before.slowmode_delay,
                                        overwrites=before.overwrites,
                                        topic=before.topic,
                                        default_auto_archive_duration=before.default_auto_archive_duration,
                                        reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                    )
                                else:
                                    if isinstance(after, discord.VoiceChannel):
                                        await after.edit(
                                            name=before.name,
                                            type=before.type,
                                            position=before.position,
                                            overwrites=before.overwrites,
                                            bitrate=before.bitrate,
                                            rtc_region=before.rtc_region,
                                            video_quality_mode=before.video_quality_mode,
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                        )
                            if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(after.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(after.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(after.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(after.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(after.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(after.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(after.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(after.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(after.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(int(logchanneldata[after.guild.id]["logchannel"])).send(
                                            embed=embed
                                        )
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(after.guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                if isinstance(after, discord.TextChannel):
                                    # await after.guild.update(
                                    await after.edit(
                                        name=before.name,
                                        type=before.type,
                                        position=before.position,
                                        nsfw=before.nsfw,
                                        slowmode_delay=before.slowmode_delay,
                                        overwrites=before.overwrites,
                                        topic=before.topic,
                                        default_auto_archive_duration=before.default_auto_archive_duration,
                                        reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                    )
                                else:
                                    if isinstance(after, discord.VoiceChannel):
                                        await after.edit(
                                            name=before.name,
                                            type=before.type,
                                            position=before.position,
                                            overwrites=before.overwrites,
                                            bitrate=before.bitrate,
                                            rtc_region=before.rtc_region,
                                            video_quality_mode=before.video_quality_mode,
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                        )
                        except:
                            if isinstance(after, discord.TextChannel):
                                # await after.guild.update(
                                await after.edit(
                                    name=before.name,
                                    type=before.type,
                                    position=before.position,
                                    nsfw=before.nsfw,
                                    slowmode_delay=before.slowmode_delay,
                                    overwrites=before.overwrites,
                                    topic=before.topic,
                                    default_auto_archive_duration=before.default_auto_archive_duration,
                                    reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                )
                            else:
                                if isinstance(after, discord.VoiceChannel):
                                    await after.edit(
                                        name=before.name,
                                        type=before.type,
                                        position=before.position,
                                        overwrites=before.overwrites,
                                        bitrate=before.bitrate,
                                        rtc_region=before.rtc_region,
                                        video_quality_mode=before.video_quality_mode,
                                        reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                    )
                        if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(after.guild.id,'[AntiBot] Обновление каналов!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление каналов!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(after.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(after.guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(after.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(after.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(after.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(after.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(after.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(after.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(after.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(int(logchanneldata[after.guild.id]["logchannel"])).send(
                                        embed=embed
                                    )
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[after.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            try:
                enabled_2 = editserverdata[after.guild.id]["enabled"]
            except KeyError:
                enabled_2 = False

            async for entry in after.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.channel_update
            ):
                if (
                    entry.user != after.guild.owner
                    and enabled
                    and enabled_2
                    and not entry.user.bot
                ):
                    vega = client.get_guild(after.guild.id).me
                    try:
                        if vega.top_role >= entry.user.top_role:
                            if isinstance(after, discord.TextChannel):
                                # await after.guild.update(
                                await after.edit(
                                    name=before.name,
                                    type=before.type,
                                    position=before.position,
                                    nsfw=before.nsfw,
                                    slowmode_delay=before.slowmode_delay,
                                    overwrites=before.overwrites,
                                    topic=before.topic,
                                    default_auto_archive_duration=before.default_auto_archive_duration,
                                    reason=f"{get_language(after.guild.id,'[AntiCrash] Обновление каналов!')}",
                                )
                            else:
                                if isinstance(after, discord.VoiceChannel):
                                    await after.edit(
                                        name=before.name,
                                        type=before.type,
                                        position=before.position,
                                        overwrites=before.overwrites,
                                        bitrate=before.bitrate,
                                        rtc_region=before.rtc_region,
                                        video_quality_mode=before.video_quality_mode,
                                        reason=f"{get_language(after.guild.id,'[AntiCrash] Обновление каналов!')}",
                                    )
                    except:
                        if isinstance(after, discord.TextChannel):
                            # await after.guild.update(
                            await after.edit(
                                name=before.name,
                                type=before.type,
                                position=before.position,
                                nsfw=before.nsfw,
                                slowmode_delay=before.slowmode_delay,
                                overwrites=before.overwrites,
                                topic=before.topic,
                                default_auto_archive_duration=before.default_auto_archive_duration,
                                reason=f"{get_language(after.guild.id,'[AntiCrash] Обновление каналов!')}",
                            )
                        else:
                            if isinstance(after, discord.VoiceChannel):
                                await after.edit(
                                    name=before.name,
                                    type=before.type,
                                    position=before.position,
                                    overwrites=before.overwrites,
                                    bitrate=before.bitrate,
                                    rtc_region=before.rtc_region,
                                    video_quality_mode=before.video_quality_mode,
                                    reason=f"{get_language(after.guild.id,'[AntiCrash] Обновление каналов!')}",
                                )
                    if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                        try:
                            with open('json/msg_appeal.json', 'r') as f:
                                ma = json.load(f)
                            text = ma[str(after.guild.id)]["appeal"]
                            embed = discord.Embed(
                                title=f"{get_language(after.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                color=0xFF2B2B,
                            )
                            embed.add_field(
                                name=f"{get_language(after.guild.id,'На сервере:')}",
                                value=f"{after.guild.name}",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(after.guild.id,'Модератором:')}",
                                value=f"VEGA ⦡#7724",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(after.guild.id,'По причине:')}",
                                value=f"{get_language(after.guild.id,'[AntiCrash] Обновление каналов!')}\n`{get_language(after.guild.id,'Редактирование сервера запрещено!')}`",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(after.guild.id,'Владелец сервера:')}",
                                value=f"{after.guild.owner}",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(after.guild.id,'Апелляция:')}",
                                value=f"{text}",
                                inline=False,
                            )
                            await entry.user.send(embed=embed)
                            await entry.user.ban(
                                reason=f"{get_language(after.guild.id,'[AntiCrash] Обновление каналов!')} {get_language(after.guild.id,'Подозрительные действия со стороны участника!')}",
                                delete_message_days=1,
                            )
                            
                            embed = discord.Embed(
                                description=f"{get_language(after.guild.id,'Подозрительные действия со стороны участника!')}\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiCrash] Обновление каналов!')}\n\n**{get_language(after.guild.id,'Информация об участнике:')}**\n{get_language(after.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                color=0xFCC21B,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiCrash')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(after.guild.id,'ID участника:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(logchanneldata[after.guild.id]["logchannel"])
                                ).send(embed=embed)
                            except:
                                pass
                            return
                        except:
                            pass
        except:
            pass


# Удаление роли
@client.event
async def on_guild_role_delete(role):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[role.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            async for entry in role.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_delete
            ):
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != role.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if role.guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[role.guild.id]:
                            if entry.user.id not in ignorebotsdata[role.guild.id]["rights"]:
                                if not role.managed:
                                    vega = client.get_guild(role.guild.id).me
                                    try:
                                        if vega.top_role >= entry.user.top_role:
                                            await role.guild.create_role(
                                                name=role.name,
                                                permissions=role.permissions,
                                                colour=role.colour,
                                                hoist=role.hoist,
                                                mentionable=role.mentionable,
                                                reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}",
                                            )
                                    except:
                                        await role.guild.create_role(
                                            name=role.name,
                                            permissions=role.permissions,
                                            colour=role.colour,
                                            hoist=role.hoist,
                                            mentionable=role.mentionable,
                                            reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}",
                                        )
                                    if entry.user in role.guild.members and vega.top_role >= entry.user.top_role:
                                        try:
                                            await entry.user.ban(
                                                reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны бота!')}",
                                                delete_message_days=1,
                                            )
                                            
                                            embed = discord.Embed(
                                                description=f"{get_language(role.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(role.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(role.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}",
                                                color=0xFCC21B,
                                            )
                                            if entry.user.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(role.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(role.guild.id,'Не использует HTTP взаимодействия')}"
                                            if entry.user.public_flags.verified_bot:
                                                verification_bot = f"{get_language(role.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(role.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if entry.user.public_flags.spammer:
                                                spamm_bot = f"{get_language(role.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(role.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(role.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(role.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(role.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(role.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(role.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                                inline=False,
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
                                                    int(logchanneldata[role.guild.id]["logchannel"])
                                                ).send(embed=embed)
                                            except:
                                                pass
                                            return
                                        except:
                                            pass
                                else:
                                    print(f"[ ИНФО ] Роль {role} интегрирована.")
                        else:
                            if not role.managed:
                                vega = client.get_guild(role.guild.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        await role.guild.create_role(
                                            name=role.name,
                                            permissions=role.permissions,
                                            colour=role.colour,
                                            hoist=role.hoist,
                                            mentionable=role.mentionable,
                                            reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}",
                                        )
                                except:
                                    await role.guild.create_role(
                                        name=role.name,
                                        permissions=role.permissions,
                                        colour=role.colour,
                                        hoist=role.hoist,
                                        mentionable=role.mentionable,
                                        reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}",
                                    )
                                if entry.user in role.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(role.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(role.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(role.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(role.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(role.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(role.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(role.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(role.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(role.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(role.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(role.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(role.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(role.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(role.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
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
                                                int(logchanneldata[role.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                            else:
                                print(f"[ ИНФО ] Роль {role} интегрирована.")
                    else:
                        if not role.managed:
                            vega = client.get_guild(role.guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await role.guild.create_role(
                                        name=role.name,
                                        permissions=role.permissions,
                                        colour=role.colour,
                                        hoist=role.hoist,
                                        mentionable=role.mentionable,
                                        reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}",
                                    )
                            except:
                                await role.guild.create_role(
                                    name=role.name,
                                    permissions=role.permissions,
                                    colour=role.colour,
                                    hoist=role.hoist,
                                    mentionable=role.mentionable,
                                    reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}",
                                )
                            if entry.user in role.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(role.guild.id,'[AntiBot] Удаление ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(role.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(role.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(role.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiBot] Удаление ролей!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(role.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(role.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(role.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(role.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(role.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(role.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(role.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(role.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(role.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(role.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(role.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
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
                                            int(logchanneldata[role.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                        else:
                            print(f"[ ИНФО ] Роль {role} интегрирована.")
        except:
            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[role.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            try:
                enabled_2 = editserverdata[role.guild.id]["enabled"]
            except KeyError:
                enabled_2 = False

            async for entry in role.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_delete
            ):
                if (
                    entry.user != role.guild.owner
                    and enabled
                    and enabled_2
                    and not entry.user.bot
                ):
                    if not role.managed:
                        vega = client.get_guild(role.guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await role.guild.create_role(
                                    name=role.name,
                                    permissions=role.permissions,
                                    colour=role.colour,
                                    hoist=role.hoist,
                                    mentionable=role.mentionable,
                                    reason=f"{get_language(role.guild.id,'[AntiCrash] Удаление ролей!')}",
                                )
                        except:
                            await role.guild.create_role(
                                name=role.name,
                                permissions=role.permissions,
                                colour=role.colour,
                                hoist=role.hoist,
                                mentionable=role.mentionable,
                                reason=f"{get_language(role.guild.id,'[AntiCrash] Удаление ролей!')}",
                            )
                        if entry.user in role.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                with open('json/msg_appeal.json', 'r') as f:
                                    ma = json.load(f)
                                text = ma[str(role.guild.id)]["appeal"]
                                embed = discord.Embed(
                                    title=f"{get_language(role.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                    color=0xFF2B2B,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'На сервере:')}",
                                    value=f"{role.guild.name}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'Модератором:')}",
                                    value=f"VEGA ⦡#7724",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'По причине:')}",
                                    value=f"{get_language(role.guild.id,'[AntiCrash] Удаление ролей!')}\n`{get_language(role.guild.id,'Редактирование сервера запрещено!')}`",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'Владелец сервера:')}",
                                    value=f"{role.guild.owner}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'Апелляция:')}",
                                    value=f"{text}",
                                    inline=False,
                                )
                                await entry.user.send(embed=embed)
                                await entry.user.ban(
                                    reason=f"{get_language(role.guild.id,'[AntiCrash] Удаление ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны участника!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(role.guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiCrash] Удаление ролей!')}\n\n**{get_language(role.guild.id,'Информация об участнике:')}**\n{get_language(role.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                    color=0xFCC21B,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(role.guild.id,'был забанен функцией AntiCrash')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024)
                                )
                                embed.set_footer(
                                    text=f"{get_language(role.guild.id,'ID участника:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[role.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass


# Создание роли
@client.event
async def on_guild_role_create(role):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[role.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            async for entry in role.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_create
            ):
                """if role.managed:
                    try:
                        # Вега отберет права у любого бота с интегрированой ролью
                        tmr = gdata("vega", "temp_role")
                        if str(role.guild.id) not in tmr:
                            tmr.update({str(role.guild.id): ""})
                        if str(role.id) not in tmr[str(role.guild.id)]:
                            tmr.update(
                                {
                                    str(role.guild.id): tmr[
                                        str(role.guild.id)
                                    ]
                                    + str(f"{role.id},")
                                    + " "
                                }
                            )
                            wdata("vega", "temp_role", tmr)
                    except:
                        pass"""
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != role.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if role.guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[role.guild.id]:
                            if entry.user.id not in ignorebotsdata[role.guild.id]["rights"]:
                                if not role.managed:
                                    vega = client.get_guild(role.guild.id).me
                                    try:
                                        if vega.top_role >= entry.user.top_role:
                                            await role.delete(
                                                reason=f"{get_language(role.guild.id,'[AntiBot] Создание ролей!')}",
                                            )
                                    except:
                                        await role.delete(
                                            reason=f"{get_language(role.guild.id,'[AntiBot] Создание ролей!')}",
                                        )
                                    if entry.user in role.guild.members and vega.top_role >= entry.user.top_role:
                                        try:
                                            await entry.user.ban(
                                                reason=f"{get_language(role.guild.id,'[AntiBot] Создание ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны бота!')}",
                                                delete_message_days=1,
                                            )
                                            
                                            embed = discord.Embed(
                                                description=f"{get_language(role.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(role.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(role.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiBot] Создание ролей!')}",
                                                color=0xFCC21B,
                                            )
                                            if entry.user.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(role.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(role.guild.id,'Не использует HTTP взаимодействия')}"
                                            if entry.user.public_flags.verified_bot:
                                                verification_bot = f"{get_language(role.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(role.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if entry.user.public_flags.spammer:
                                                spamm_bot = f"{get_language(role.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(role.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(role.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(role.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(role.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(role.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(role.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                                inline=False,
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
                                                    int(logchanneldata[role.guild.id]["logchannel"])
                                                ).send(embed=embed)
                                            except:
                                                pass
                                            return
                                        except:
                                            pass
                                else:
                                    pass
                        else:
                            if not role.managed:
                                vega = client.get_guild(role.guild.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        await role.delete(
                                            reason=f"{get_language(role.guild.id,'[AntiBot] Создание ролей!')}",
                                        )
                                except:
                                    await role.delete(
                                        reason=f"{get_language(role.guild.id,'[AntiBot] Создание ролей!')}",
                                    )
                                if entry.user in role.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(role.guild.id,'[AntiBot] Создание ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(role.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(role.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(role.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiBot] Создание ролей!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(role.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(role.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(role.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(role.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(role.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(role.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(role.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(role.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(role.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(role.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(role.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
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
                                                int(logchanneldata[role.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                            else:
                                pass
                    else:
                        if not role.managed:
                            vega = client.get_guild(role.guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await role.delete(
                                        reason=f"{get_language(role.guild.id,'[AntiBot] Создание ролей!')}",
                                    )
                            except:
                                await role.delete(
                                    reason=f"{get_language(role.guild.id,'[AntiBot] Создание ролей!')}",
                                )
                            if entry.user in role.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(role.guild.id,'[AntiBot] Создание ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(role.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(role.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(role.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiBot] Создание ролей!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(role.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(role.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(role.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(role.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(role.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(role.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(role.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(role.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(role.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(role.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(role.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
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
                                            int(logchanneldata[role.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                        else:
                            pass
        except:
            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[role.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            try:
                enabled_2 = editserverdata[role.guild.id]["enabled"]
            except KeyError:
                enabled_2 = False

            async for entry in role.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_create
            ):
                if (
                    entry.user != role.guild.owner
                    and enabled
                    and enabled_2
                    and not entry.user.bot
                ):
                    if not role.managed:
                        vega = client.get_guild(role.guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await role.delete(
                                    reason=f"{get_language(role.guild.id,'[AntiCrash] Создание ролей!')}",
                                )
                        except:
                            await role.delete(
                                reason=f"{get_language(role.guild.id,'[AntiCrash] Создание ролей!')}",
                            )
                        if entry.user in role.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                with open('json/msg_appeal.json', 'r') as f:
                                    ma = json.load(f)
                                text = ma[str(role.guild.id)]["appeal"]
                                embed = discord.Embed(
                                    title=f"{get_language(role.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                    color=0xFF2B2B,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'На сервере:')}",
                                    value=f"{role.guild.name}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'Модератором:')}",
                                    value=f"VEGA ⦡#7724",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'По причине:')}",
                                    value=f"{get_language(role.guild.id,'[AntiCrash] Создание ролей!')}\n`{get_language(role.guild.id,'Редактирование сервера запрещено!')}`",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'Владелец сервера:')}",
                                    value=f"{role.guild.owner}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(role.guild.id,'Апелляция:')}",
                                    value=f"{text}",
                                    inline=False,
                                )
                                await entry.user.send(embed=embed)
                                await entry.user.ban(
                                    reason=f"{get_language(role.guild.id,'[AntiCrash] Создание ролей!')} {get_language(role.guild.id,'Подозрительные действия со стороны участника!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(role.guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(role.guild.id,'Причина:')}**\n{get_language(role.guild.id,'[AntiCrash] Создание ролей!')}\n\n**{get_language(role.guild.id,'Информация об участнике:')}**\n{get_language(role.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                    color=0xFCC21B,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(role.guild.id,'был забанен функцией AntiCrash')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024)
                                )
                                embed.set_footer(
                                    text=f"{get_language(role.guild.id,'ID участника:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[role.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass


# Обновление роли
@client.event
async def on_guild_role_update(before, after):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[after.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            async for entry in after.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_update
            ):
                if (
                    entry.user != after.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    
                    tmr = gdata("vega", "temp_role")
                    vega = client.get_guild(after.guild.id).me
                    if (
                        entry.user.id not in wlbotsdata[0]["Bots"]
                    ):
                        if after.guild.id in ignorebotsdata:
                            if "rights" in ignorebotsdata[after.guild.id]:
                                if entry.user.id not in ignorebotsdata[after.guild.id]["rights"]:
                                    rposition = before.position != after.position
                                    rposition2 = before.position == after.position
                                    if (
                                        rposition and before.colour != after.colour
                                        or rposition and before.mentionable != after.mentionable
                                        or rposition and before.hoist != after.hoist
                                        or rposition and before.name != after.name
                                        or rposition and before.permissions != after.permissions
                                        or rposition2 and before.colour != after.colour
                                        or rposition2 and before.mentionable != after.mentionable
                                        or rposition2 and before.hoist != after.hoist
                                        or rposition2 and before.name != after.name
                                        or rposition2 and before.permissions != after.permissions
                                    ):
                                        try:
                                            try:
                                                await after.edit(
                                                    colour=before.colour,
                                                    mentionable=before.mentionable,
                                                    hoist=before.hoist,
                                                    name=before.name,
                                                    permissions=before.permissions,
                                                    position=before.position,
                                                    reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей!')}",
                                                )
                                            except:
                                                await after.edit(
                                                    colour=before.colour,
                                                    mentionable=before.mentionable,
                                                    hoist=before.hoist,
                                                    name=before.name,
                                                    permissions=before.permissions,
                                                    reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей!')}",
                                                )
                                        except:
                                            pass
                                        if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                                            try:
                                                await entry.user.ban(
                                                    reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                                                    delete_message_days=1,
                                                )
                                                
                                                embed = discord.Embed(
                                                    description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление ролей!')}",
                                                    color=0xFCC21B,
                                                )
                                                if entry.user.public_flags.http_interactions_bot:
                                                    http_interactions_bot_bot = f"{get_language(after.guild.id,'Использует только HTTP взаимодействия')}"
                                                else:
                                                    http_interactions_bot_bot = f"{get_language(after.guild.id,'Не использует HTTP взаимодействия')}"
                                                if entry.user.public_flags.verified_bot:
                                                    verification_bot = f"{get_language(after.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                                else:
                                                    verification_bot = f"{get_language(after.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                                if entry.user.public_flags.spammer:
                                                    spamm_bot = f"{get_language(after.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                                else:
                                                    spamm_bot = f"{get_language(after.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                                embed.add_field(
                                                    name=f":information_source: {get_language(after.guild.id,'Информация о боте:')}",
                                                    value=f"{http_interactions_bot_bot}\n**{get_language(after.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(after.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                                    inline=False,
                                                )
                                                embed.set_author(
                                                    name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                                )
                                                embed.set_thumbnail(
                                                    url=entry.user.avatar.replace(size=1024))
                                                embed.set_footer(
                                                    text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                                                )
                                                try:
                                                    await client.get_channel(int(logchanneldata[after.guild.id]["logchannel"])).send(
                                                        embed=embed
                                                    )
                                                except:
                                                    pass
                                            except:
                                                pass
                                            try:
                                                tmr.update(
                                                    {
                                                        str(after.guild.id): tmr[
                                                            str(after.guild.id)
                                                        ].replace(
                                                            str(f"{after.id}, "),
                                                            "",
                                                        )
                                                    }
                                                )
                                                wdata("vega", "temp_role", tmr)
                                            except:
                                                pass

                                    """elif (
                                        rposition and not before.colour != after.colour
                                        and not  before.mentionable != after.mentionable
                                        and not before.hoist != after.hoist
                                        and not before.name != after.name
                                        and not before.permissions != after.permissions
                                    ):
                                        #print("\033[36m [ ИНФО ]  Положение роли небыло изменено!")
                                        pass
                                        try:
                                            await after.edit(
                                                position=before.position,
                                                reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей! (Произошло обратное изменение позиции роли.) Кто-то изменяет позицию роли!')}",
                                            )
                                        except:
                                            pass
                                    try:
                                    if (
                                        str(after.id) in tmr[str(after.guild.id)]
                                        and after.managed
                                    ):
                                        # Вега вернет обновленные права интегрированной роли
                                        await after.edit(
                                            permissions=discord.Permissions(),
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Временная защита! (Отобрал права)')}",
                                        )
                                        await asyncio.sleep(10)
                                        try:
                                            tmr.update(
                                                {
                                                    str(after.guild.id): tmr[
                                                        str(after.guild.id)
                                                    ].replace(
                                                        str(f"{after.id}, "),
                                                        "",
                                                    )
                                                }
                                            )
                                            wdata("vega", "temp_role", tmr)
                                        except:
                                            pass
                                        try:
                                            await after.edit(
                                                permissions=before.permissions,
                                                reason=f"{get_language(after.guild.id,'[AntiBot] Временная защита! (Вернул права)')}",
                                            )
                                        except:
                                            pass"""
                            else:
                                rposition = before.position != after.position
                                rposition2 = before.position == after.position
                                if (
                                    rposition and before.colour != after.colour
                                    or rposition and before.mentionable != after.mentionable
                                    or rposition and before.hoist != after.hoist
                                    or rposition and before.name != after.name
                                    or rposition and before.permissions != after.permissions
                                    or rposition2 and before.colour != after.colour
                                    or rposition2 and before.mentionable != after.mentionable
                                    or rposition2 and before.hoist != after.hoist
                                    or rposition2 and before.name != after.name
                                    or rposition2 and before.permissions != after.permissions
                                ):
                                    try:
                                        try:
                                            await after.edit(
                                                colour=before.colour,
                                                mentionable=before.mentionable,
                                                hoist=before.hoist,
                                                name=before.name,
                                                permissions=before.permissions,
                                                position=before.position,
                                                reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей!')}",
                                            )
                                        except:
                                            await after.edit(
                                                colour=before.colour,
                                                mentionable=before.mentionable,
                                                hoist=before.hoist,
                                                name=before.name,
                                                permissions=before.permissions,
                                                reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей!')}",
                                            )
                                    except:
                                        pass
                                    if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                                        try:
                                            await entry.user.ban(
                                                reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                                                delete_message_days=1,
                                            )
                                            
                                            embed = discord.Embed(
                                                description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление ролей!')}",
                                                color=0xFCC21B,
                                            )
                                            if entry.user.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(after.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(after.guild.id,'Не использует HTTP взаимодействия')}"
                                            if entry.user.public_flags.verified_bot:
                                                verification_bot = f"{get_language(after.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(after.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if entry.user.public_flags.spammer:
                                                spamm_bot = f"{get_language(after.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(after.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(after.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(after.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(after.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                                inline=False,
                                            )
                                            embed.set_author(
                                                name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                            )
                                            embed.set_thumbnail(
                                                url=entry.user.avatar.replace(size=1024))
                                            embed.set_footer(
                                                text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                                            )
                                            try:
                                                await client.get_channel(int(logchanneldata[after.guild.id]["logchannel"])).send(
                                                    embed=embed
                                                )
                                            except:
                                                pass
                                        except:
                                            pass
                                        try:
                                            tmr.update(
                                                {
                                                    str(after.guild.id): tmr[
                                                        str(after.guild.id)
                                                    ].replace(
                                                        str(f"{after.id}, "),
                                                        "",
                                                    )
                                                }
                                            )
                                            wdata("vega", "temp_role", tmr)
                                        except:
                                            pass
                        else:
                            rposition = before.position != after.position
                            rposition2 = before.position == after.position
                            if (
                                rposition and before.colour != after.colour
                                or rposition and before.mentionable != after.mentionable
                                or rposition and before.hoist != after.hoist
                                or rposition and before.name != after.name
                                or rposition and before.permissions != after.permissions
                                or rposition2 and before.colour != after.colour
                                or rposition2 and before.mentionable != after.mentionable
                                or rposition2 and before.hoist != after.hoist
                                or rposition2 and before.name != after.name
                                or rposition2 and before.permissions != after.permissions
                            ):
                                try:
                                    try:
                                        await after.edit(
                                            colour=before.colour,
                                            mentionable=before.mentionable,
                                            hoist=before.hoist,
                                            name=before.name,
                                            permissions=before.permissions,
                                            position=before.position,
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей!')}",
                                        )
                                    except:
                                        await after.edit(
                                            colour=before.colour,
                                            mentionable=before.mentionable,
                                            hoist=before.hoist,
                                            name=before.name,
                                            permissions=before.permissions,
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей!')}",
                                        )
                                except:
                                    pass
                                if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление ролей!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(after.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(after.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(after.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(after.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(after.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(after.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(after.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(after.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(after.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(int(logchanneldata[after.guild.id]["logchannel"])).send(
                                                embed=embed
                                            )
                                        except:
                                            pass
                                    except:
                                        pass
                                    try:
                                        tmr.update(
                                            {
                                                str(after.guild.id): tmr[
                                                    str(after.guild.id)
                                                ].replace(
                                                    str(f"{after.id}, "),
                                                    "",
                                                )
                                            }
                                        )
                                        wdata("vega", "temp_role", tmr)
                                    except:
                                        pass
        except:
            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[after.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            try:
                enabled_2 = editserverdata[after.guild.id]["enabled"]
            except KeyError:
                enabled_2 = False

            async for entry in after.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.role_update
            ):
                if (
                    entry.user != after.guild.owner
                    and enabled
                    and enabled_2
                    and not entry.user.bot
                ):
                    vega = client.get_guild(after.guild.id).me
                    rposition = before.position != after.position
                    rposition2 = before.position == after.position
                    if (
                        rposition and before.colour != after.colour
                        or rposition and before.mentionable != after.mentionable
                        or rposition and before.hoist != after.hoist
                        or rposition and before.name != after.name
                        or rposition and before.permissions != after.permissions
                        or rposition2 and before.colour != after.colour
                        or rposition2 and before.mentionable != after.mentionable
                        or rposition2 and before.hoist != after.hoist
                        or rposition2 and before.name != after.name
                        or rposition2 and before.permissions != after.permissions
                    ):
                        try:
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await after.edit(
                                        colour=before.colour,
                                        mentionable=before.mentionable,
                                        hoist=before.hoist,
                                        name=before.name,
                                        permissions=before.permissions,
                                        position=before.position,
                                        reason=f"{get_language(before.guild.id,'[AntiCrash] Обновление ролей!')}",
                                    )
                            except:
                                if vega.top_role >= entry.user.top_role:
                                    await after.edit(
                                        colour=before.colour,
                                        mentionable=before.mentionable,
                                        hoist=before.hoist,
                                        name=before.name,
                                        permissions=before.permissions,
                                        reason=f"{get_language(before.guild.id,'[AntiCrash] Обновление ролей!')}",
                                    )
                        except:
                            try:
                                await after.edit(
                                    colour=before.colour,
                                    mentionable=before.mentionable,
                                    hoist=before.hoist,
                                    name=before.name,
                                    permissions=before.permissions,
                                    position=before.position,
                                    reason=f"{get_language(before.guild.id,'[AntiCrash] Обновление ролей!')}",
                                )
                            except:
                                await after.edit(
                                    colour=before.colour,
                                    mentionable=before.mentionable,
                                    hoist=before.hoist,
                                    name=before.name,
                                    permissions=before.permissions,
                                    reason=f"{get_language(before.guild.id,'[AntiCrash] Обновление ролей!')}",
                                )
                        if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                with open('json/msg_appeal.json', 'r') as f:
                                    ma = json.load(f)
                                text = ma[str(after.guild.id)]["appeal"]
                                embed = discord.Embed(
                                    title=f"{get_language(after.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                    color=0xFF2B2B,
                                )
                                embed.add_field(
                                    name=f"{get_language(after.guild.id,'На сервере:')}",
                                    value=f"{after.guild.name}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(after.guild.id,'Модератором:')}",
                                    value=f"VEGA ⦡#7724",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(after.guild.id,'По причине:')}",
                                    value=f"{get_language(after.guild.id,'[AntiCrash] Обновление ролей!')}\n`{get_language(after.guild.id,'Редактирование сервера запрещено!')}`",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(after.guild.id,'Владелец сервера:')}",
                                    value=f"{after.guild.owner}",
                                    inline=False,
                                )
                                embed.add_field(
                                    name=f"{get_language(after.guild.id,'Апелляция:')}",
                                    value=f"{text}",
                                    inline=False,
                                )
                                await entry.user.send(embed=embed)
                                await entry.user.ban(
                                    reason=f"{get_language(after.guild.id,'[AntiCrash] Обновление ролей!')} {get_language(after.guild.id,'Подозрительные действия со стороны участника!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(after.guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiCrash] Обновление ролей!')}\n\n**{get_language(after.guild.id,'Информация об участнике:')}**\n{get_language(after.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                    color=0xFCC21B,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiCrash')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024)
                                )
                                embed.set_footer(
                                    text=f"{get_language(after.guild.id,'ID участника:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[after.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass


# Бан пользователя
@client.event
async def on_member_ban(guild, user):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[guild.id]["enabled"]
        except KeyError:
            enabled = False
        
        
        async for entry in guild.audit_logs(
            limit=1, action=discord.AuditLogAction.ban
        ):
            if (
                not entry.user.id in wlbotsdata[0]["Bots"]
                and entry.user != guild.owner
                and enabled
                and entry.user.bot
            ):
                if guild.id in ignorebotsdata:
                    if "rights" in ignorebotsdata[guild.id]:
                        if entry.user.id not in ignorebotsdata[guild.id]["rights"]:
                            vega = client.get_guild(guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await guild.unban(user)
                            except:
                                await guild.unban(user)
                            if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(guild.id,'[AntiBot] Бан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    embed = discord.Embed(
                                        description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Бан пользователя!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                            embed=embed
                                        )
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await guild.unban(user)
                        except:
                            await guild.unban(user)
                        if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(guild.id,'[AntiBot] Бан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                embed = discord.Embed(
                                    description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Бан пользователя!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                        embed=embed
                                    )
                                except:
                                    pass
                                return
                            except:
                                pass
                else:
                    vega = client.get_guild(guild.id).me
                    try:
                        if vega.top_role >= entry.user.top_role:
                            await guild.unban(user)
                    except:
                        await guild.unban(user)
                    if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                        try:
                            await entry.user.ban(
                                reason=f"{get_language(guild.id,'[AntiBot] Бан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                delete_message_days=1,
                            )
                            embed = discord.Embed(
                                description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Бан пользователя!')}",
                                color=0xFCC21B,
                            )
                            if entry.user.public_flags.http_interactions_bot:
                                http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                            else:
                                http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                            if entry.user.public_flags.verified_bot:
                                verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                            else:
                                verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                            if entry.user.public_flags.spammer:
                                spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                            else:
                                spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                            embed.add_field(
                                name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                inline=False,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                    embed=embed
                                )
                            except:
                                pass
                            return
                        except:
                            pass

            # \/  Кто забанил бота  \/
            elif entry.target.bot and entry.user != client.get_user(
                795551166393876481
            ):
                embed = discord.Embed(
                    description=f"**{get_language(guild.id,'Пользователем:')}** {entry.user}\n**ID:** `{entry.user.id}`",
                    color=0xFF2B2B,
                )
                if entry.user.public_flags.http_interactions_bot:
                    http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                else:
                    http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                if entry.user.public_flags.verified_bot:
                    verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                else:
                    verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                if entry.user.public_flags.spammer:
                    spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                else:
                    spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                embed.add_field(
                    name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                    value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                    inline=False,
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
                    await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                        embed=embed
                    )
                except:
                    pass
            else:
                pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            enabled_2 = editserverdata[guild.id]["enabled"]
        except KeyError:
            enabled_2 = False
        async for entry in guild.audit_logs(
            limit=1, action=discord.AuditLogAction.ban
        ):
            if (
                entry.user != guild.owner
                and enabled
                and enabled_2
                and not entry.user.bot
            ):
                if guild.id in wluserdata:
                    if "members" in wluserdata[guild.id]:
                        if entry.user.id not in wluserdata[guild.id]["members"]:
                            vega = client.get_guild(guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await guild.unban(user)
                            except:
                                await guild.unban(user)
                            if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    with open('json/msg_appeal.json', 'r') as f:
                                        ma = json.load(f)
                                    text = ma[str(guild.id)]["appeal"]
                                    embed = discord.Embed(
                                        title=f"{get_language(guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                        color=0xFF2B2B,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'На сервере:')}",
                                        value=f"{guild.name}",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'Модератором:')}",
                                        value=f"VEGA ⦡#7724",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'По причине:')}",
                                        value=f"{get_language(guild.id,'[AntiCrash] Бан пользователя!')}\n`{get_language(guild.id,'Вас нет в белом списке!')}`",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'Владелец сервера:')}",
                                        value=f"{guild.owner}",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'Апелляция:')}",
                                        value=f"{text}",
                                        inline=False,
                                    )
                                    await entry.user.send(embed=embed)
                                    await entry.user.ban(
                                        reason=f"{get_language(guild.id,'[AntiCrash] Бан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны участника!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiCrash] Бан пользователя!')}\n\n**{get_language(guild.id,'Информация об участнике:')}**\n{get_language(guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                        color=0xFCC21B,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiCrash')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024)
                                    )
                                    embed.set_footer(
                                        text=f"{get_language(guild.id,'ID участника:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(logchanneldata[guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                   

# Разбан пользователя
@client.event
async def on_member_unban(guild, user):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[guild.id]["enabled"]
        except KeyError:
            enabled = False
        async for entry in guild.audit_logs(
            limit=1, action=discord.AuditLogAction.unban
        ):
            
            if (
                not entry.user.id in wlbotsdata[0]["Bots"]
                and entry.user != guild.owner
                and enabled
                and entry.user.bot
            ):
                if guild.id in ignorebotsdata:
                    if "rights" in ignorebotsdata[guild.id]:
                        if entry.user.id not in ignorebotsdata[guild.id]["rights"]:
                            vega = client.get_guild(guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await guild.ban(user)
                            except:
                                await guild.ban(user)
                            if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(guild.id,'[AntiBot] Разбан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Разбан пользователя!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                            embed=embed
                                        )
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await guild.ban(user)
                        except:
                            await guild.ban(user)
                        if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(guild.id,'[AntiBot] Разбан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Разбан пользователя!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                        embed=embed
                                    )
                                except:
                                    pass
                                return
                            except:
                                pass
                else:
                    vega = client.get_guild(guild.id).me
                    try:
                        if vega.top_role >= entry.user.top_role:
                            await guild.ban(user)
                    except:
                        await guild.ban(user)
                    if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                        try:
                            await entry.user.ban(
                                reason=f"{get_language(guild.id,'[AntiBot] Разбан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                delete_message_days=1,
                            )
                            
                            embed = discord.Embed(
                                description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Разбан пользователя!')}",
                                color=0xFCC21B,
                            )
                            if entry.user.public_flags.http_interactions_bot:
                                http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                            else:
                                http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                            if entry.user.public_flags.verified_bot:
                                verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                            else:
                                verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                            if entry.user.public_flags.spammer:
                                spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                            else:
                                spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                            embed.add_field(
                                name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                inline=False,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                    embed=embed
                                )
                            except:
                                pass
                            return
                        except:
                            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            enabled_2 = editserverdata[guild.id]["enabled"]
        except KeyError:
            enabled_2 = False

        async for entry in guild.audit_logs(
            limit=1, action=discord.AuditLogAction.unban
        ):
            if (
                entry.user != guild.owner
                and enabled
                and enabled_2
                and not entry.user.bot
            ):
                if guild.id in wluserdata:
                    if "members" in wluserdata[guild.id]:
                        if entry.user.id not in wluserdata[guild.id]["members"]:
                            vega = client.get_guild(guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await guild.ban(user)
                            except:
                                await guild.ban(user)
                            if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    with open('json/msg_appeal.json', 'r') as f:
                                        ma = json.load(f)
                                    text = ma[str(guild.id)]["appeal"]
                                    embed = discord.Embed(
                                        title=f"{get_language(guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                        color=0xFF2B2B,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'На сервере:')}",
                                        value=f"{guild.name}",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'Модератором:')}",
                                        value=f"VEGA ⦡#7724",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'По причине:')}",
                                        value=f"{get_language(guild.id,'[AntiCrash] Разбан пользователя!')}\n`{get_language(guild.id,'Вас нет в белом списке!')}`",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'Владелец сервера:')}",
                                        value=f"{guild.owner}",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(guild.id,'Апелляция:')}",
                                        value=f"{text}",
                                        inline=False,
                                    )
                                    await entry.user.send(embed=embed)
                                    await entry.user.ban(
                                        reason=f"{get_language(guild.id,'[AntiCrash] Разбан пользователя!')} {get_language(guild.id,'Подозрительные действия со стороны участника!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiCrash] Разбан пользователя!')}\n\n**{get_language(guild.id,'Информация об участнике:')}**\n{get_language(guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                        color=0xFCC21B,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiCrash')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024)
                                    )
                                    embed.set_footer(
                                        text=f"{get_language(guild.id,'ID участника:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(logchanneldata[guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass


# Обновление пользователя
@client.event
async def on_member_update(before, after):
    # Проверка роли мута и ее выдача
    """try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        pass
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
                elif mr not in [r.id for r in before.roles] and mr in [
                    r.id for r in after.roles
                ]:
                    mu2 += str(after.id) + " "
                    mu[str(after.guild.id)] = mu2
                    wdata("vega", "mute_users", mu)"""

    # Антибот и Антикраш
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[after.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            async for entry in after.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.member_role_update
            ):
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != after.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if after.guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[after.guild.id]:
                            if entry.user.id not in ignorebotsdata[after.guild.id]["rights"]:
                                vega = client.get_guild(after.guild.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        await after.edit(
                                            role=before.role,
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')}",
                                        )
                                except:
                                    await after.edit(
                                        role=before.role,
                                        reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')}",
                                    )
                                if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(after.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(after.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(after.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(after.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(after.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(after.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(after.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(after.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(after.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(int(logchanneldata[after.guild.id]["logchannel"])).send(
                                                embed=embed
                                            )
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                        else:
                            vega = client.get_guild(after.guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await after.edit(
                                        role=before.role,
                                        reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')}",
                                    )
                            except:
                                await after.edit(
                                    role=before.role,
                                    reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')}",
                                )
                            if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(after.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(after.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(after.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(after.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(after.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(after.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(after.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(after.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(after.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(int(logchanneldata[after.guild.id]["logchannel"])).send(
                                            embed=embed
                                        )
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(after.guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await after.edit(
                                    role=before.role,
                                    reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')}",
                                )
                        except:
                            await after.edit(
                                role=before.role,
                                reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')}",
                            )
                        if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')} {get_language(after.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(after.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiBot] Обновление ролей у пользователя!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(after.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(after.guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(after.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(after.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(after.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(after.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(after.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(after.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(after.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(after.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(int(logchanneldata[after.guild.id]["logchannel"])).send(
                                        embed=embed
                                    )
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[after.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            try:
                enabled_2 = editserverdata[after.guild.id]["enabled"]
            except KeyError:
                enabled_2 = False

            async for entry in after.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.member_role_update
            ):
                if (
                    entry.user != after.guild.owner
                    and enabled
                    and enabled_2
                    and not entry.user.bot
                ):
                    if after.guild.id in wluserdata:
                        if "members" in wluserdata[after.guild.id]:
                            if entry.user.id not in wluserdata[after.guild.id]["members"]:
                                vega = client.get_guild(after.guild.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        await after.edit(
                                            roles=before.roles,
                                            reason=f"{get_language(before.guild.id,'[AntiCrash] Обновление ролей у участника!')}",
                                        )
                                except:
                                    await after.edit(
                                        roles=before.roles,
                                        reason=f"{get_language(before.guild.id,'[AntiCrash] Обновление ролей у участника!')}",
                                    )
                                if entry.user in after.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        with open('json/msg_appeal.json', 'r') as f:
                                            ma = json.load(f)
                                        text = ma[str(after.guild.id)]["appeal"]
                                        embed = discord.Embed(
                                            title=f"{get_language(after.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                            color=0xFF2B2B,
                                        )
                                        embed.add_field(
                                            name=f"{get_language(after.guild.id,'На сервере:')}",
                                            value=f"{after.guild.name}",
                                            inline=False,
                                        )
                                        embed.add_field(
                                            name=f"{get_language(after.guild.id,'Модератором:')}",
                                            value=f"VEGA ⦡#7724",
                                            inline=False,
                                        )
                                        embed.add_field(
                                            name=f"{get_language(after.guild.id,'По причине:')}",
                                            value=f"{get_language(after.guild.id,'[AntiCrash] Обновление ролей у участника!')}\n`{get_language(after.guild.id,'Вас нет в белом списке!')}`",
                                            inline=False,
                                        )
                                        embed.add_field(
                                            name=f"{get_language(after.guild.id,'Владелец сервера:')}",
                                            value=f"{after.guild.owner}",
                                            inline=False,
                                        )
                                        embed.add_field(
                                            name=f"{get_language(after.guild.id,'Апелляция:')}",
                                            value=f"{text}",
                                            inline=False,
                                        )
                                        await entry.user.send(embed=embed)
                                        await entry.user.ban(
                                            reason=f"{get_language(after.guild.id,'[AntiCrash] Обновление ролей у участника!')} {get_language(after.guild.id,'Подозрительные действия со стороны участника!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(after.guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(after.guild.id,'Причина:')}**\n{get_language(after.guild.id,'[AntiCrash] Обновление ролей у участника!')}\n\n**{get_language(after.guild.id,'Информация об участнике:')}**\n{get_language(after.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                            color=0xFCC21B,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(after.guild.id,'был забанен функцией AntiCrash')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024)
                                        )
                                        embed.set_footer(
                                            text=f"{get_language(after.guild.id,'ID участника:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(
                                                int(logchanneldata[after.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
        except:
            pass


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
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[after.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            async for entry in after.audit_logs(
                limit=1, action=discord.AuditLogAction.guild_update
            ):
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != after.owner
                    and enabled
                    and entry.user.bot
                ):
                    if after.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[after.id]:
                            if entry.user.id not in ignorebotsdata[after.id]["rights"]:
                                vega = client.get_guild(after.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        await after.edit(
                                            afk_channel=before.afk_channel,
                                            name=before.name,
                                            system_channel=before.system_channel,
                                            afk_timeout=before.afk_timeout,
                                            explicit_content_filter=before.explicit_content_filter,
                                            reason=f"{get_language(before.id,'[AntiBot] Обновление настроек сервера!')}",
                                        )
                                except:
                                    await after.edit(
                                        afk_channel=before.afk_channel,
                                        name=before.name,
                                        system_channel=before.system_channel,
                                        afk_timeout=before.afk_timeout,
                                        explicit_content_filter=before.explicit_content_filter,
                                        reason=f"{get_language(before.id,'[AntiBot] Обновление настроек сервера!')}",
                                    )
                                if entry.user in after.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(after.id,'[AntiBot] Обновление настроек сервера!')} {get_language(after.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(after.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.id,'Причина:')}**\n{get_language(after.id,'[AntiBot] Обновление настроек сервера!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(after.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(after.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(after.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(after.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(after.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(after.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(after.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(after.id,'Верификация:')}** {verification_bot}\n**{get_language(after.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(after.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(after.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(int(logchanneldata[after.id]["logchannel"])).send(
                                                embed=embed
                                            )
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                        else:
                            vega = client.get_guild(after.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await after.edit(
                                        afk_channel=before.afk_channel,
                                        name=before.name,
                                        system_channel=before.system_channel,
                                        afk_timeout=before.afk_timeout,
                                        explicit_content_filter=before.explicit_content_filter,
                                        reason=f"{get_language(before.id,'[AntiBot] Обновление настроек сервера!')}",
                                    )
                            except:
                                await after.edit(
                                    afk_channel=before.afk_channel,
                                    name=before.name,
                                    system_channel=before.system_channel,
                                    afk_timeout=before.afk_timeout,
                                    explicit_content_filter=before.explicit_content_filter,
                                    reason=f"{get_language(before.id,'[AntiBot] Обновление настроек сервера!')}",
                                )
                            if entry.user in after.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(after.id,'[AntiBot] Обновление настроек сервера!')} {get_language(after.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(after.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.id,'Причина:')}**\n{get_language(after.id,'[AntiBot] Обновление настроек сервера!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(after.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(after.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(after.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(after.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(after.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(after.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(after.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(after.id,'Верификация:')}** {verification_bot}\n**{get_language(after.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(after.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(after.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(int(logchanneldata[after.id]["logchannel"])).send(
                                            embed=embed
                                        )
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(after.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await after.edit(
                                    afk_channel=before.afk_channel,
                                    name=before.name,
                                    system_channel=before.system_channel,
                                    afk_timeout=before.afk_timeout,
                                    explicit_content_filter=before.explicit_content_filter,
                                    reason=f"{get_language(before.id,'[AntiBot] Обновление настроек сервера!')}",
                                )
                        except:
                            await after.edit(
                                afk_channel=before.afk_channel,
                                name=before.name,
                                system_channel=before.system_channel,
                                afk_timeout=before.afk_timeout,
                                explicit_content_filter=before.explicit_content_filter,
                                reason=f"{get_language(before.id,'[AntiBot] Обновление настроек сервера!')}",
                            )
                        if entry.user in after.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(after.id,'[AntiBot] Обновление настроек сервера!')} {get_language(after.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(after.id,'Подозрительные действия со стороны бота!')}\n{get_language(after.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(after.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(after.id,'Причина:')}**\n{get_language(after.id,'[AntiBot] Обновление настроек сервера!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(after.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(after.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(after.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(after.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(after.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(after.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(after.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(after.id,'Верификация:')}** {verification_bot}\n**{get_language(after.id,'Спамер?:')}** {spamm_bot}\n**{get_language(after.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(after.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(after.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(after.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(int(logchanneldata[after.id]["logchannel"])).send(
                                        embed=embed
                                    )
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[after.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            try:
                enabled_2 = editserverdata[after.id]["enabled"]
            except KeyError:
                enabled_2 = False

            async for entry in after.audit_logs(
                limit=1, action=discord.AuditLogAction.guild_update
            ):
                if (
                    entry.user != after.owner
                    and enabled
                    and enabled_2
                    and not entry.user.bot
                ):
                    vega = client.get_guild(after.id).me
                    try:
                        if vega.top_role >= entry.user.top_role:
                            await after.edit(
                                afk_channel=before.afk_channel,
                                name=before.name,
                                system_channel=before.system_channel,
                                afk_timeout=before.afk_timeout,
                                explicit_content_filter=before.explicit_content_filter,
                                reason=f"{get_language(before.id,'[AntiCrash] Обновление настроек сервера!')}",
                            )
                    except:
                        await after.edit(
                            afk_channel=before.afk_channel,
                            name=before.name,
                            system_channel=before.system_channel,
                            afk_timeout=before.afk_timeout,
                            explicit_content_filter=before.explicit_content_filter,
                            reason=f"{get_language(before.id,'[AntiCrash] Обновление настроек сервера!')}",
                        )
                    if entry.user in after.members and vega.top_role >= entry.user.top_role:
                        try:
                            with open('json/msg_appeal.json', 'r') as f:
                                ma = json.load(f)
                            text = ma[str(after.id)]["appeal"]
                            embed = discord.Embed(
                                title=f"{get_language(after.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                color=0xFF2B2B,
                            )
                            embed.add_field(
                                name=f"{get_language(after.id,'На сервере:')}",
                                value=f"{after.name}",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(after.id,'Модератором:')}",
                                value=f"VEGA ⦡#7724",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(after.id,'По причине:')}",
                                value=f"{get_language(after.id,'[AntiCrash] Обновление настроек сервера!')}\n`{get_language(after.id,'Редактирование сервера запрещено!')}`",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(after.id,'Владелец сервера:')}",
                                value=f"{after.owner}",
                                inline=False,
                            )
                            embed.add_field(
                                name=f"{get_language(after.id,'Апелляция:')}",
                                value=f"{text}",
                                inline=False,
                            )
                            await entry.user.send(embed=embed)
                            await entry.user.ban(
                                reason=f"{get_language(after.id,'[AntiCrash] Обновление настроек сервера!')} {get_language(after.id,'Подозрительные действия со стороны участника!')}",
                                delete_message_days=1,
                            )
                            
                            embed = discord.Embed(
                                description=f"{get_language(after.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(after.id,'Причина:')}**\n{get_language(after.id,'[AntiCrash] Обновление настроек сервера!')}\n\n**{get_language(after.id,'Информация об участнике:')}**\n{get_language(after.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                color=0xFCC21B,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(after.id,'был забанен функцией AntiCrash')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024)
                            )
                            embed.set_footer(
                                text=f"{get_language(after.id,'ID участника:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(logchanneldata[after.id]["logchannel"])
                                ).send(embed=embed)
                            except:
                                pass
                            return
                        except:
                            pass
        except:
            pass


# Эмодзи
@client.event
async def on_guild_emojis_update(guild, before, after):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        try:
            enabled = antibotdata[guild.id]["enabled"]
        except KeyError:
            enabled = False

        """Эмодзи редактирован
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
                            await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(embed=embed)
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
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[guild.id]:
                            if entry.user.id not in ignorebotsdata[guild.id]["rights"]:
                                vega = client.get_guild(guild.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        await before.emoji.delete()
                                except:
                                    await before.emoji.delete()
                                if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(guild.id,'[AntiBot] Создание эмодзи!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Создание эмодзи!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                                embed=embed
                                            )
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                        else:
                            vega = client.get_guild(guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await before.emoji.delete()
                            except:
                                await before.emoji.delete()
                            if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(guild.id,'[AntiBot] Создание эмодзи!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Создание эмодзи!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                            embed=embed
                                        )
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await before.emoji.delete()
                        except:
                            await before.emoji.delete()
                        if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(guild.id,'[AntiBot] Создание эмодзи!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Создание эмодзи!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                        embed=embed
                                    )
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass

        # Эмодзи удален
        try:
            async for entry in guild.audit_logs(
                limit=1, action=discord.AuditLogAction.emoji_delete
            ):
                
                if (
                    not str(entry.user.id) in wlbotsdata[0]["Bots"]
                    and entry.user != guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[guild.id]:
                            if entry.user.id not in ignorebotsdata[guild.id]["rights"]:
                                vega = client.get_guild(guild.id).me
                                if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(guild.id,'[AntiBot] Удаление эмодзи!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Удаление эмодзи!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(guild.user.joined_at.timestamp())}:D> *(<t:{int(guild.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                                embed=embed
                                            )
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                        else:
                            vega = client.get_guild(guild.id).me
                            if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(guild.id,'[AntiBot] Удаление эмодзи!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Удаление эмодзи!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(guild.user.joined_at.timestamp())}:D> *(<t:{int(guild.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                            embed=embed
                                        )
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(guild.id).me
                        if entry.user in guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(guild.id,'[AntiBot] Удаление эмодзи!')} {get_language(guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(guild.id,'Причина:')}**\n{get_language(guild.id,'[AntiBot] Удаление эмодзи!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(guild.id,'Верификация:')}** {verification_bot}\n**{get_language(guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(guild.id,'Присоединился:')}** <t:{int(guild.user.joined_at.timestamp())}:D> *(<t:{int(guild.user.joined_at.timestamp())}:R>)*\n**{get_language(guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(int(logchanneldata[guild.id]["logchannel"])).send(
                                        embed=embed
                                    )
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass


# Создание приглашения
@client.event
async def on_invite_create(invite):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        try:
            enabled = antibotdata[invite.guild.id]["enabled"]
        except KeyError:
            enabled = False

        # Приглашение создано
        try:
            async for entry in invite.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.invite_create
            ):
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != invite.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if invite.guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[invite.guild.id]:
                            if entry.user.id not in ignorebotsdata[invite.guild.id]["rights"]:
                                vega = client.get_guild(invite.guild.id).me
                                try:
                                    if vega.top_role >= entry.user.top_role:
                                        await invite.delete()
                                except:
                                    await invite.delete()
                                if entry.user in invite.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(invite.guild.id,'[AntiBot] Создание приглашения!')} {get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(invite.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(invite.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(invite.guild.id,'Причина:')}**\n{get_language(invite.guild.id,'[AntiBot] Создание приглашения!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(invite.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(invite.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(invite.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(invite.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(invite.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(invite.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(invite.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(invite.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(invite.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(invite.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(invite.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(invite.guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(invite.guild.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(
                                                int(logchanneldata[invite.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                        else:
                            vega = client.get_guild(invite.guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await invite.delete()
                            except:
                                await invite.delete()
                            if entry.user in invite.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(invite.guild.id,'[AntiBot] Создание приглашения!')} {get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(invite.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(invite.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(invite.guild.id,'Причина:')}**\n{get_language(invite.guild.id,'[AntiBot] Создание приглашения!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(invite.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(invite.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(invite.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(invite.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(invite.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(invite.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(invite.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(invite.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(invite.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(invite.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(invite.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(invite.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(invite.guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(logchanneldata[invite.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(invite.guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await invite.delete()
                        except:
                            await invite.delete()
                        if entry.user in invite.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(invite.guild.id,'[AntiBot] Создание приглашения!')} {get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(invite.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(invite.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(invite.guild.id,'Причина:')}**\n{get_language(invite.guild.id,'[AntiBot] Создание приглашения!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(invite.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(invite.guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(invite.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(invite.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(invite.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(invite.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(invite.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(invite.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(invite.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(invite.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(invite.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(invite.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(invite.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[invite.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass


# Удаление приглашения
@client.event
async def on_invite_remove(invite):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        try:
            enabled = antibotdata[invite.guild.id]["enabled"]
        except KeyError:
            enabled = False

        # Приглашение удалено
        try:
            async for entry in invite.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.invite_remove
            ):
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != invite.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if invite.guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[invite.guild.id]:
                            if entry.user.id not in ignorebotsdata[invite.guild.id]["rights"]:
                                vega = client.get_guild(invite.guild.id).me
                                if entry.user in invite.guild.members and vega.top_role >= entry.user.top_role:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(invite.guild.id,'[AntiBot] Удаление приглашения!')} {get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(invite.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(invite.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(invite.guild.id,'Причина:')}**\n{get_language(invite.guild.id,'[AntiBot] Удаление приглашения!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(invite.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(invite.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(invite.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(invite.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(invite.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(invite.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(invite.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(invite.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(invite.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(invite.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(invite.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(invite.guild.id,'был забанен функцией AntiBot')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024))
                                        embed.set_footer(
                                            text=f"{get_language(invite.guild.id,'ID бота:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(
                                                int(logchanneldata[invite.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                        else:
                            vega = client.get_guild(invite.guild.id).me
                            if entry.user in invite.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(invite.guild.id,'[AntiBot] Удаление приглашения!')} {get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(invite.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(invite.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(invite.guild.id,'Причина:')}**\n{get_language(invite.guild.id,'[AntiBot] Удаление приглашения!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(invite.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(invite.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(invite.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(invite.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(invite.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(invite.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(invite.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(invite.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(invite.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(invite.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(invite.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(invite.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(invite.guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(logchanneldata[invite.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(invite.guild.id).me
                        if entry.user in invite.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(invite.guild.id,'[AntiBot] Удаление приглашения!')} {get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(invite.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(invite.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(invite.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(invite.guild.id,'Причина:')}**\n{get_language(invite.guild.id,'[AntiBot] Удаление приглашения!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(invite.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(invite.guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(invite.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(invite.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(invite.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(invite.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(invite.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(invite.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(invite.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(invite.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(invite.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(invite.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(invite.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[invite.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
        except:
            pass


# Вебхуки
"""async def webhook():
    await webhook.delete(
        reason=f"{get_language(webhook.guild.id,'[AntiCrash] Создание вебхука!')}",
    )"""
@client.event
async def on_webhooks_update(channel):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[channel.guild.id]["enabled"]
        except KeyError:
            enabled = False
        # Вебхук создан
        async for entry in channel.guild.audit_logs(
            limit=1, action=discord.AuditLogAction.webhook_create
        ):
            
            if (
                not entry.user.id in wlbotsdata[0]["Bots"]
                and entry.user != channel.guild.owner
                and enabled
                and entry.user.bot
            ):
                if channel.guild.id in ignorebotsdata:
                    if "rights" in ignorebotsdata[channel.guild.id]:
                        if entry.user.id not in ignorebotsdata[channel.guild.id]["rights"]:
                            vega = client.get_guild(channel.guild.id).me
                            try:
                                if vega.top_role >= entry.user.top_role:
                                    await channel.webhook.delete(
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}",
                                    )
                            except:
                                await channel.webhook.delete(
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}",
                                )
                            if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(logchanneldata[channel.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(channel.guild.id).me
                        try:
                            if vega.top_role >= entry.user.top_role:
                                await channel.webhook.delete(
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}",
                                )
                        except:
                            await channel.webhook.delete(
                                reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}",
                            )
                        if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[channel.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
                else:
                    vega = client.get_guild(channel.guild.id).me
                    try:
                        if vega.top_role >= entry.user.top_role:
                            await channel.webhook.delete(
                                reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}",
                            )
                    except:
                        await channel.webhook.delete(
                            reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}",
                        )
                    if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                        try:
                            await entry.user.ban(
                                reason=f"{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                delete_message_days=1,
                            )
                            
                            embed = discord.Embed(
                                description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Создание вебхука!')}",
                                color=0xFCC21B,
                            )
                            if entry.user.public_flags.http_interactions_bot:
                                http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                            else:
                                http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                            if entry.user.public_flags.verified_bot:
                                verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                            else:
                                verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                            if entry.user.public_flags.spammer:
                                spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                            else:
                                spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                            embed.add_field(
                                name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                inline=False,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(logchanneldata[channel.guild.id]["logchannel"])
                                ).send(embed=embed)
                            except:
                                pass
                            return
                        except:
                            pass
        
        # Вебхук удален
        async for entry in channel.guild.audit_logs(
            limit=1, action=discord.AuditLogAction.webhook_delete
        ):
            
            if (
                not str(entry.user.id) in wlbotsdata[0]["Bots"]
                and entry.user != channel.guild.owner
                and enabled
                and entry.user.bot
            ):
                if channel.guild.id in ignorebotsdata:
                    if "rights" in ignorebotsdata[channel.guild.id]:
                        if entry.user.id not in ignorebotsdata[channel.guild.id]["rights"]:
                            vega = client.get_guild(channel.guild.id).me
                            if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Удаление вебхука!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(logchanneldata[channel.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(channel.guild.id).me
                        if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Удаление вебхука!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[channel.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
                else:
                    vega = client.get_guild(channel.guild.id).me
                    if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                        try:
                            await entry.user.ban(
                                reason=f"{get_language(channel.guild.id,'[AntiBot] Удаление вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                delete_message_days=1,
                            )
                            
                            embed = discord.Embed(
                                description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Удаление вебхука!')}",
                                color=0xFCC21B,
                            )
                            if entry.user.public_flags.http_interactions_bot:
                                http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                            else:
                                http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                            if entry.user.public_flags.verified_bot:
                                verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                            else:
                                verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                            if entry.user.public_flags.spammer:
                                spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                            else:
                                spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                            embed.add_field(
                                name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                inline=False,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(logchanneldata[channel.guild.id]["logchannel"])
                                ).send(embed=embed)
                            except:
                                pass
                            return
                        except:
                            pass
        
        # Вебхук отредактирован
        async for entry in channel.guild.audit_logs(
            limit=1, action=discord.AuditLogAction.webhook_update
        ):
            
            if (
                not str(entry.user.id) in wlbotsdata[0]["Bots"]
                and entry.user != channel.guild.owner
                and enabled
                and entry.user.bot
            ):
                if channel.guild.id in ignorebotsdata:
                    if "rights" in ignorebotsdata[channel.guild.id]:
                        if entry.user.id not in ignorebotsdata[channel.guild.id]["rights"]:
                            vega = client.get_guild(channel.guild.id).me
                            if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(channel.guild.id,'[AntiBot] Редактирование вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    
                                    embed = discord.Embed(
                                        description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Редактирование вебхука!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
                                    )
                                    embed.set_author(
                                        name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                        icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                    )
                                    embed.set_thumbnail(
                                        url=entry.user.avatar.replace(size=1024))
                                    embed.set_footer(
                                        text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                    )
                                    try:
                                        await client.get_channel(
                                            int(logchanneldata[channel.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                    else:
                        vega = client.get_guild(channel.guild.id).me
                        if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                            try:
                                await entry.user.ban(
                                    reason=f"{get_language(channel.guild.id,'[AntiBot] Редактирование вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                    delete_message_days=1,
                                )
                                
                                embed = discord.Embed(
                                    description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Редактирование вебхука!')}",
                                    color=0xFCC21B,
                                )
                                if entry.user.public_flags.http_interactions_bot:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                                else:
                                    http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                                if entry.user.public_flags.verified_bot:
                                    verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                else:
                                    verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                if entry.user.public_flags.spammer:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                else:
                                    spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                embed.add_field(
                                    name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                    value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                    inline=False,
                                )
                                embed.set_author(
                                    name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                    icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                )
                                embed.set_thumbnail(
                                    url=entry.user.avatar.replace(size=1024))
                                embed.set_footer(
                                    text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                                )
                                try:
                                    await client.get_channel(
                                        int(logchanneldata[channel.guild.id]["logchannel"])
                                    ).send(embed=embed)
                                except:
                                    pass
                                return
                            except:
                                pass
                else:
                    vega = client.get_guild(channel.guild.id).me
                    if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                        try:
                            await entry.user.ban(
                                reason=f"{get_language(channel.guild.id,'[AntiBot] Редактирование вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}",
                                delete_message_days=1,
                            )
                            
                            embed = discord.Embed(
                                description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(channel.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(channel.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiBot] Редактирование вебхука!')}",
                                color=0xFCC21B,
                            )
                            if entry.user.public_flags.http_interactions_bot:
                                http_interactions_bot_bot = f"{get_language(channel.guild.id,'Использует только HTTP взаимодействия')}"
                            else:
                                http_interactions_bot_bot = f"{get_language(channel.guild.id,'Не использует HTTP взаимодействия')}"
                            if entry.user.public_flags.verified_bot:
                                verification_bot = f"{get_language(channel.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                            else:
                                verification_bot = f"{get_language(channel.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                            if entry.user.public_flags.spammer:
                                spamm_bot = f"{get_language(channel.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                            else:
                                spamm_bot = f"{get_language(channel.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                            embed.add_field(
                                name=f":information_source: {get_language(channel.guild.id,'Информация о боте:')}",
                                value=f"{http_interactions_bot_bot}\n**{get_language(channel.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(channel.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(channel.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(channel.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                inline=False,
                            )
                            embed.set_author(
                                name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiBot')}",
                                icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                            )
                            embed.set_thumbnail(
                                url=entry.user.avatar.replace(size=1024))
                            embed.set_footer(
                                text=f"{get_language(channel.guild.id,'ID бота:')} {entry.user.id}"
                            )
                            try:
                                await client.get_channel(
                                    int(logchanneldata[channel.guild.id]["logchannel"])
                                ).send(embed=embed)
                            except:
                                pass
                            return
                        except:
                            pass


        # Антикраш участников
        try:
            enabled = user_anticrashdata[channel.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            enabled_2 = editserverdata[channel.guild.id]["enabled"]
        except KeyError:
            enabled_2 = False
        # Вебхук создан
        async for entry in channel.guild.audit_logs(
            limit=1, action=discord.AuditLogAction.webhook_create
        ):
            if (
                entry.user != channel.guild.owner
                and enabled
                and enabled_2
                and not entry.user.bot
            ):
                vega = client.get_guild(channel.guild.id).me
                try:
                    if vega.top_role >= entry.user.top_role:
                        await channel.webhook.delete(
                            reason=f"{get_language(channel.guild.id,'[AntiCrash] Создание вебхука!')}",
                        )
                        # await channel.webhooks()
                except:
                    await channel.webhook.delete(
                        reason=f"{get_language(channel.guild.id,'[AntiCrash] Создание вебхука!')}",
                    )
                    # await webhooks()
                if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                    try:
                        with open('json/msg_appeal.json', 'r') as f:
                            ma = json.load(f)
                        text = ma[str(channel.guild.id)]["appeal"]
                        embed = discord.Embed(
                            title=f"{get_language(channel.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                            color=0xFF2B2B,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'На сервере:')}",
                            value=f"{channel.guild.name}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'Модератором:')}",
                            value=f"VEGA ⦡#7724",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'По причине:')}",
                            value=f"{get_language(channel.guild.id,'[AntiCrash] Создание вебхука!')}\n`{get_language(channel.guild.id,'Редактирование сервера запрещено!')}`",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'Владелец сервера:')}",
                            value=f"{channel.guild.owner}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'Апелляция:')}",
                            value=f"{text}",
                            inline=False,
                        )
                        await entry.user.send(embed=embed)
                        await entry.user.ban(
                            reason=f"{get_language(channel.guild.id,'[AntiCrash] Создание вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}",
                            delete_message_days=1,
                        )
                        
                        embed = discord.Embed(
                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiCrash] Создание вебхука!')}\n\n**{get_language(channel.guild.id,'Информация об участнике:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiCrash')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(
                            url=entry.user.avatar.replace(size=1024)
                        )
                        embed.set_footer(
                            text=f"{get_language(channel.guild.id,'ID участника:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(logchanneldata[channel.guild.id]["logchannel"])
                            ).send(embed=embed)
                        except:
                            pass
                        return
                    except:
                        pass
        # Вебхук удален
        async for entry in channel.guild.audit_logs(
            limit=1, action=discord.AuditLogAction.webhook_delete
        ):
            if (
                entry.user != channel.guild.owner
                and enabled
                and enabled_2
                and not entry.user.bot
            ):
                vega = client.get_guild(channel.guild.id).me
                if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                    try:
                        with open('json/msg_appeal.json', 'r') as f:
                            ma = json.load(f)
                        text = ma[str(channel.guild.id)]["appeal"]
                        embed = discord.Embed(
                            title=f"{get_language(channel.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                            color=0xFF2B2B,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'На сервере:')}",
                            value=f"{channel.guild.name}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'Модератором:')}",
                            value=f"VEGA ⦡#7724",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'По причине:')}",
                            value=f"{get_language(channel.guild.id,'[AntiCrash] Удаление вебхука!')}\n`{get_language(channel.guild.id,'Редактирование сервера запрещено!')}`",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'Владелец сервера:')}",
                            value=f"{channel.guild.owner}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'Апелляция:')}",
                            value=f"{text}",
                            inline=False,
                        )
                        await entry.user.send(embed=embed)
                        await entry.user.ban(
                            reason=f"{get_language(channel.guild.id,'[AntiCrash] Удаление вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}",
                            delete_message_days=1,
                        )
                        
                        embed = discord.Embed(
                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiCrash] Удаление вебхука!')}\n\n**{get_language(channel.guild.id,'Информация об участнике:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiCrash')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(
                            url=entry.user.avatar.replace(size=1024)
                        )
                        embed.set_footer(
                            text=f"{get_language(channel.guild.id,'ID участника:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(logchanneldata[channel.guild.id]["logchannel"])
                            ).send(embed=embed)
                        except:
                            pass
                        return
                    except:
                        pass
        # Вебхук отредактирован
        async for entry in channel.guild.audit_logs(
            limit=1, action=discord.AuditLogAction.webhook_update
        ):
            if (
                entry.user != channel.guild.owner
                and enabled
                and enabled_2
                and not entry.user.bot
            ):
                vega = client.get_guild(channel.guild.id).me
                if entry.user in channel.guild.members and vega.top_role >= entry.user.top_role:
                    try:
                        with open('json/msg_appeal.json', 'r') as f:
                            ma = json.load(f)
                        text = ma[str(channel.guild.id)]["appeal"]
                        embed = discord.Embed(
                            title=f"{get_language(channel.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                            color=0xFF2B2B,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'На сервере:')}",
                            value=f"{channel.guild.name}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'Модератором:')}",
                            value=f"VEGA ⦡#7724",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'По причине:')}",
                            value=f"{get_language(channel.guild.id,'[AntiCrash] Редактирование вебхука!')}\n`{get_language(channel.guild.id,'Редактирование сервера запрещено!')}`",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'Владелец сервера:')}",
                            value=f"{channel.guild.owner}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(channel.guild.id,'Апелляция:')}",
                            value=f"{text}",
                            inline=False,
                        )
                        await entry.user.send(embed=embed)
                        await entry.user.ban(
                            reason=f"{get_language(channel.guild.id,'[AntiCrash] Редактирование вебхука!')} {get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}",
                            delete_message_days=1,
                        )
                        
                        embed = discord.Embed(
                            description=f"{get_language(channel.guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(channel.guild.id,'Причина:')}**\n{get_language(channel.guild.id,'[AntiCrash] Редактирование вебхука!')}\n\n**{get_language(channel.guild.id,'Информация об участнике:')}**\n{get_language(channel.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                            color=0xFCC21B,
                        )
                        embed.set_author(
                            name=f"{entry.user} {get_language(channel.guild.id,'был забанен функцией AntiCrash')}",
                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                        )
                        embed.set_thumbnail(
                            url=entry.user.avatar.replace(size=1024)
                        )
                        embed.set_footer(
                            text=f"{get_language(channel.guild.id,'ID участника:')} {entry.user.id}"
                        )
                        try:
                            await client.get_channel(
                                int(logchanneldata[channel.guild.id]["logchannel"])
                            ).send(embed=embed)
                        except:
                            pass
                        return
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
            if guild.icon != None:
                embed.set_thumbnail(url=guild.icon)
            await client.get_channel(811963689677619230).send(embed=embed)
        except:
            pass
    else:
        pass


# Кик пользователя
@client.event
async def on_member_remove(member):
    try:
        enabled = deactivatedata[0]["Option"]
    except KeyError:
        enabled = False
    if enabled:
        pass
    else:
        # Антибот
        try:
            enabled = antibotdata[member.guild.id]["enabled"]
        except KeyError:
            enabled = False
        
        """p = gdata('vega', 'passbots')
        try:
            # Проверка пропуска
            if str(member.id) in p[str(member.guild.id)]:
                p = gdata('vega', 'passbots')
                p.update({str(member.guild.id):p[str(member.guild.id)].replace(str(f"<@!{member.id}>, "), '')})
                wdata('vega', 'passbots', p)
                embed = discord.Embed(color=0xcc1a1d)
                embed.set_author(name=f"{get_language(member.guild.id, 'Пропуск')} {member} {get_language(member.guild.id, 'истек!')}", icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png")
                embed.set_footer(text=f'ID: {member.id}')
                try:
                    await client.get_channel(int(logchanneldata[member.guild.id]["logchannel"])).send(embed=embed)
                except:
                    pass
            else:
                pass
        except:
            pass"""


        # Кик пользователя
        try:
            async for entry in member.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.kick
            ):
                
                
                if (
                    not entry.user.id in wlbotsdata[0]["Bots"]
                    and entry.user != member.guild.owner
                    and enabled
                    and entry.user.bot
                ):
                    if member.guild.id in ignorebotsdata:
                        if "rights" in ignorebotsdata[member.guild.id]:
                            if entry.user.id not in ignorebotsdata[member.guild.id]["rights"]:
                                vega = client.get_guild(member.guild.id).me
                                if entry.user in member.guild.members and vega.top_role >= entry.user.top_role:
                                    if enabled:
                                        try:
                                            await entry.user.ban(
                                                reason=f"{get_language(member.guild.id,'[AntiBot] Кик пользователя!')} {get_language(member.guild.id,'Подозрительные действия со стороны бота!')}",
                                                delete_message_days=1,
                                            )
                                            embed = discord.Embed(
                                                description=f"{get_language(member.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot] Кик пользователя!')}",
                                                color=0xFCC21B,
                                            )
                                            if entry.user.public_flags.http_interactions_bot:
                                                http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                            else:
                                                http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                            if entry.user.public_flags.verified_bot:
                                                verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                            else:
                                                verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                            if entry.user.public_flags.spammer:
                                                spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                            else:
                                                spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                            embed.add_field(
                                                name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                                value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                                inline=False,
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
                                                    int(logchanneldata[member.guild.id]["logchannel"])
                                                ).send(embed=embed)
                                            except:
                                                pass
                                            return
                                        except:
                                            pass
                        else:
                            vega = client.get_guild(member.guild.id).me
                            if entry.user in member.guild.members and vega.top_role >= entry.user.top_role:
                                if enabled:
                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(member.guild.id,'[AntiBot] Кик пользователя!')} {get_language(member.guild.id,'Подозрительные действия со стороны бота!')}",
                                            delete_message_days=1,
                                        )
                                        embed = discord.Embed(
                                            description=f"{get_language(member.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot] Кик пользователя!')}",
                                            color=0xFCC21B,
                                        )
                                        if entry.user.public_flags.http_interactions_bot:
                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                        else:
                                            http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                        if entry.user.public_flags.verified_bot:
                                            verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                        else:
                                            verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                        if entry.user.public_flags.spammer:
                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                        else:
                                            spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                        embed.add_field(
                                            name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                            value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                            inline=False,
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
                                                int(logchanneldata[member.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                        return
                                    except:
                                        pass
                    else:
                        vega = client.get_guild(member.guild.id).me
                        if entry.user in member.guild.members and vega.top_role >= entry.user.top_role:
                            if enabled:
                                try:
                                    await entry.user.ban(
                                        reason=f"{get_language(member.guild.id,'[AntiBot] Кик пользователя!')} {get_language(member.guild.id,'Подозрительные действия со стороны бота!')}",
                                        delete_message_days=1,
                                    )
                                    embed = discord.Embed(
                                        description=f"{get_language(member.guild.id,'Подозрительные действия со стороны бота!')}\n{get_language(member.guild.id,'**Игнорировать бота:**')} `{prefix}ignore add {entry.user.id}`\n{get_language(member.guild.id,'**Выдать пропуск:**')} `{prefix}pass add {entry.user.id}`\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiBot] Кик пользователя!')}",
                                        color=0xFCC21B,
                                    )
                                    if entry.user.public_flags.http_interactions_bot:
                                        http_interactions_bot_bot = f"{get_language(member.guild.id,'Использует только HTTP взаимодействия')}"
                                    else:
                                        http_interactions_bot_bot = f"{get_language(member.guild.id,'Не использует HTTP взаимодействия')}"
                                    if entry.user.public_flags.verified_bot:
                                        verification_bot = f"{get_language(member.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915>')}"
                                    else:
                                        verification_bot = f"{get_language(member.guild.id,'<:bot_ru1:948668130123735100><:bot_ru2:948668130127933470>')}"
                                    if entry.user.public_flags.spammer:
                                        spamm_bot = f"{get_language(member.guild.id,'<a:vega_check_mark:821700784927801394> Да')}"
                                    else:
                                        spamm_bot = f"{get_language(member.guild.id,'<a:vega_x:810843492266803230> Нет')}"
                                    embed.add_field(
                                        name=f":information_source: {get_language(member.guild.id,'Информация о боте:')}",
                                        value=f"{http_interactions_bot_bot}\n**{get_language(member.guild.id,'Верификация:')}** {verification_bot}\n**{get_language(member.guild.id,'Спамер?:')}** {spamm_bot}\n**{get_language(member.guild.id,'Присоединился:')}** <t:{int(entry.user.joined_at.timestamp())}:D> *(<t:{int(entry.user.joined_at.timestamp())}:R>)*\n**{get_language(member.guild.id,'Создан:')}** <t:{int(entry.user.created_at.timestamp())}:D> *(<t:{int(entry.user.created_at.timestamp())}:R>)*",
                                        inline=False,
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
                                            int(logchanneldata[member.guild.id]["logchannel"])
                                        ).send(embed=embed)
                                    except:
                                        pass
                                    return
                                except:
                                    pass
                
                try:
                    await member.guild.fetch_ban(member)
                    return
                except discord.NotFound:
                    pass
                    """if not entry.user == client.get_user(795551166393876481):
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
                                int(logchanneldata[member.guild.id]["logchannel"])
                            ).send(embed=embed)
                        except:
                            pass"""
        except:
            pass

        # Антикраш участников
        try:
            enabled = user_anticrashdata[member.guild.id]["enabled"]
        except KeyError:
            enabled = False
        try:
            try:
                enabled_2 = editserverdata[member.guild.id]["enabled"]
            except KeyError:
                enabled_2 = False

            async for entry in member.guild.audit_logs(
                limit=1, action=discord.AuditLogAction.kick
            ):
                if (
                    entry.user != member.guild.owner
                    and enabled
                    and enabled_2
                    and not entry.user.bot
                ):
                    if member.guild.id in wluserdata:
                        if "members" in wluserdata[member.guild.id]:
                            if entry.user.id not in wluserdata[member.guild.id]["members"]:
                                vega = client.get_guild(member.guild.id).me
                                if entry.user in member.guild.members and vega.top_role >= entry.user.top_role:
                                    with open('json/msg_appeal.json', 'r') as f:
                                        ma = json.load(f)
                                    text = ma[str(member.guild.id)]["appeal"]
                                    embed = discord.Embed(
                                        title=f"{get_language(member.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                        color=0xFF2B2B,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(member.guild.id,'На сервере:')}",
                                        value=f"{member.guild.name}",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(member.guild.id,'Модератором:')}",
                                        value=f"VEGA ⦡#7724",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(member.guild.id,'По причине:')}",
                                        value=f"{get_language(member.guild.id,'[AntiCrash] Кик пользователя!')}\n`{get_language(member.guild.id,'Вас нет в белом списке!')}`",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(member.guild.id,'Владелец сервера:')}",
                                        value=f"{member.guild.owner}",
                                        inline=False,
                                    )
                                    embed.add_field(
                                        name=f"{get_language(member.guild.id,'Апелляция:')}",
                                        value=f"{text}",
                                        inline=False,
                                    )
                                    try:
                                        await entry.user.send(embed=embed)
                                    except:
                                        pass

                                    try:
                                        await entry.user.ban(
                                            reason=f"{get_language(member.guild.id,'[AntiCrash] Кик пользователя!')} {get_language(member.guild.id,'Подозрительные действия со стороны участника!')}",
                                            delete_message_days=1,
                                        )
                                        
                                        embed = discord.Embed(
                                            description=f"{get_language(member.guild.id,'Подозрительные действия со стороны участника!')}\n\n**{get_language(member.guild.id,'Причина:')}**\n{get_language(member.guild.id,'[AntiCrash] Кик пользователя!')}\n\n**{get_language(member.guild.id,'Информация об участнике:')}**\n{get_language(member.guild.id,'Создан:')} <t:{int(entry.user.created_at.timestamp())}:F>",
                                            color=0xFCC21B,
                                        )
                                        embed.set_author(
                                            name=f"{entry.user} {get_language(member.guild.id,'был забанен функцией AntiCrash')}",
                                            icon_url="https://i.postimg.cc/QxsNmj2Z/attention.gif",
                                        )
                                        embed.set_thumbnail(
                                            url=entry.user.avatar.replace(size=1024)
                                        )
                                        embed.set_footer(
                                            text=f"{get_language(member.guild.id,'ID участника:')} {entry.user.id}"
                                        )
                                        try:
                                            await client.get_channel(
                                                int(logchanneldata[member.guild.id]["logchannel"])
                                            ).send(embed=embed)
                                        except:
                                            pass
                                    except:
                                        pass
                try:
                    await member.guild.fetch_ban(member)
                    return
                except discord.NotFound:
                    pass
        except:
            pass


"""# Авто загрузка белого списка ботов на канал
 VEGA - 806889107594674236
 @client.event
 async def autogetjson():
    while True:
        await asyncio.sleep(7200) #каждые 2 часа загружает файлы
        a = client.get_channel(806889107594674236)
        with open('message.txt', 'w') as f:
            f.write(requests.get('https://vega-bot.ru/data/whitelist.data').text)
        await a.send(file=discord.File('message.txt'))


        await a.send(file=discord.File(f'json/antibot.json'))
        await a.send(file=discord.File(f'json/channel_rights.json'))
        await a.send(file=discord.File(f'json/ignorebots.json'))
        await a.send(file=discord.File(f'json/antiinvite.json'))
        await a.send(file=discord.File(f'json/logchannel.json'))

 client.loop.create_task(autogetjson())


# Скачать json
# VEGA - 806889107594674236
# тест - 806889358740815895
 @client.command()
 @commands.guild_only()
 async def djson(ctx):
    if ctx.author.id == 351020816466575372:
        for file in os.listdir('json/'):
            await client.get_channel(806889107594674236).send(file=discord.File(f'json/{file}'))


# Отправить сообщение пользователю в лс
 @client.command()
 @commands.guild_only()
 async def bd(ctx, user:discord.Member, *, message):
    if ctx.author.id == 351020816466575372:
        msg = ctx.message
        try:
            embed = discord.Embed(title='🛠 Сообщение от Разработчика:', description=f'{message}', color=0x1e1e1e)
            await user.send(embed=embed)
            await msg.add_reaction('<a:vega_check_mark:821700784927801394>')
        except:
            await msg.add_reaction('<a:vega_x:810843492266803230>')


 ban_image = ['https://cdn.discordapp.com/attachments/713751423128698950/804296020149141534/unknown.png']"""


# Работа с сообщениями
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
                await msg.reply(embed=embed, delete_after=12.0)

            # Удаляет сообщения бота, который оффлайн. Нужно получить разрешение аппликации
            """amsgdata = gdata("vega", "antimsg")
            try:
                enabled = amsgdata[str(msg.id)]  # Было msg.guild.id
            except KeyError:
                enabled = False
            if enabled:
                try:
                    if user.bot:
                        
                        if (
                            not user.id in wlbotsdata[0]["Bots"]
                            and user.id not in ignorebotsdata[msg.id]["rights"]
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
                pass"""

        # Антиприглпшения на сервер! Нужно получить разрешение аппликации
        """try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            data = gdata("vega", "antiinvite")
            try:
                enabled = data[str(msg.id)]
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
                            await msg.delete()"""
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
                        await client.get_channel(int(logchanneldata[msg.guild.id]["logchannel"])).send(embed=embed)
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
                    await client.get_channel(int(logchanneldata[msg.guild.id]["logchannel"])).send(embed=embed)
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
