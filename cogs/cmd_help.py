import disnake as discord
import datetime
import datetime
import time

# import word
# import config
# from discord import utils
from disnake.ext import commands
# from bot import *
from helper import *
from cache import *
from enum import Enum

prefix = "/"

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
    hard_antibot = 5
    anticrash = 6
    antiinvite = 7
    antimsg = 8
    ignore = 9
    pаss = 10
    msg_appeal = 11
    edit_server = 12
    wluser = 13
    delchannels = 14
    delroles = 15

class Admin(int, Enum):
    log = 1
    language = 2
    settings = 3
    list = 4
    echo = 5
    emb = 6
    slowmode = 7

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



class class_help(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.guild_permissions(826022179568615445, user_ids={351020816466575372: True})
    # @commands.bot_has_permissions(send_messages=True)
    # @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.slash_command(
        name="help",
        description="Help about commands (Select the group and command) | Справка о командах (Укажите группу и команду)",
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def help(
        self,
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
            # row_i = ActionRow(Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vega-bot.ru/"))
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 5:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} hard-antibot",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Включите или отключите жесткий антибот. VEGA ⦡#7724 будет выгонять любых приглашенных ботов. (Пропуски, игнорируемый и белый список не действуют!)')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}hard-antibot {get_language(ctx.guild.id,'{on}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}hard-antibot on`\n╰ {get_language(ctx.guild.id,'Жесткий антибот включится.')}\n\n`{prefix}hard-antibot off`\n╰ {get_language(ctx.guild.id,'Жесткий антибот отключится.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 6:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} anticrash",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Включите или отключите антикраш от участников. VEGA ⦡ будет банить участников, если включена команда `/edit-server` и если нет участников в белом списке команды `/wluser`.')}\n\
                        {get_language(ctx.guild.id,'**Данная команда будет работать только с включенной командой `/edit-server`! Эти команды взаимосвязаны!**')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}anticrash {get_language(ctx.guild.id,'{on}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}anticrash on`\n╰ {get_language(ctx.guild.id,'Антикраш включится.')}\n\n`{prefix}anticrash off`\n╰ {get_language(ctx.guild.id,'Антикраш отключится.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 7:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 8:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} antimsg",
                        color=0xd81911
                    )
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} antimsg",
                        color=0xd81911
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Включите или отключите автоматическое удаление сообщений оффлайн ботов. VEGA ⦡#7724 будет удалять сообщения неизвестных ботов, которые находятся не в сети.')}",
                        inline=False
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}antimsg {get_language(ctx.guild.id,'{on}')}`",
                        inline=False
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`",
                        inline=False
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}antimsg on`\n╰ {get_language(ctx.guild.id,'Антисообщения включатся.')}\n\n`{prefix}antimsg off`\n╰ {get_language(ctx.guild.id,'Антисообщения отключатся.')}",
                        inline=False
                    )
                    embed.set_image(
                        url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png"
                    )
                    embed.set_author(
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 9:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 10:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 11:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} msg-appeal",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Апелляция: Сообщение с обращением от Владельца сервера, куда обращаться для разбана. Максимальное количество символов в тексте **1024**! Без сообщения не будет работать антикраш!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value="`/msg-appeal {text}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value="`{text}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}msg-appeal {get_language(ctx.guild.id,'Для разбана обращаться в [нашу группу ВК](ссылка)!')}`",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 12:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} edit-server",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Включить или выключить редактирование сервера. Если команда включена, то только Владелец имеет право изменять права/роли/каналы/сервер. Если команда выключена, то все у кого есть права, могут редактировать сервер.')}\n\
                            {get_language(ctx.guild.id,'**Данная команда будет работать только с включенной командой `/anticrash`! Эти команды взаимосвязаны!**')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}edit-server {get_language(ctx.guild.id,'{on}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}edit-server on`\n╰ {get_language(ctx.guild.id,'Запретить редактирование сервера. (Включить)')}\n\n`{prefix}edit-server off`\n╰ {get_language(ctx.guild.id,'Разрешить редактирование сервера. (Выключить)')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 13:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} wluser",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Добавить или удалить участника из белго списка. Если участник есть в белом списке, то VEGA ⦡ будет игнорировать его действия, а именно: бан/кик/изменение ролей у участников. Если изначально не вносить участника в белый список, то VEGA ⦡ будет игнорировать действия (бан/кик/изменение ролей у участников) всех пользователей на сервере.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Владелец')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}wluser {get_language(ctx.guild.id,'{add}')} {get_language(ctx.guild.id,'{ID участника}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}wluser add @user`\n╰ {get_language(ctx.guild.id,'Добавть участника в белый список')}\n\n`{prefix}wluser remove @user`\n╰ {get_language(ctx.guild.id,'Удалить участника из белого списка')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 14:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif owner == 15:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 3:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 4:
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
                        value=f"`{get_language(ctx.guild.id,'{channels}')}`; `{get_language(ctx.guild.id,'{ignores}')}`; `{get_language(ctx.guild.id,'{pass}')}`; `{get_language(ctx.guild.id,'{wl}')}`; `{get_language(ctx.guild.id,'{wluser}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}list channels`\n╰ {get_language(ctx.guild.id,'Список ограниченных каналов.')}\n\n`{prefix}list ignores`\n╰ {get_language(ctx.guild.id,'Список игнорируемых ботов.')}\n\n`{prefix}list pass`\n╰ {get_language(ctx.guild.id,'Боты, у которых есть пропуска на сервер.')}\n\n`{prefix}list wl`\n╰ {get_language(ctx.guild.id,'Белый список ботов.')}\n\n`{prefix}list wluser`\n╰ {get_language(ctx.guild.id,'Белый список участников.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 5:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 6:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif admin == 7:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                """elif admin == 4:
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)"""
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                elif moder == 8:
                    mutime = "{time}"
                    muits_time = "{its_time}"
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'❓ Команда:')} mute",
                        description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                    {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}",
                        color=0xD81911,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Замьютьте нарушителя. Причина не обязательна.')}\n{get_language(ctx.guild.id,'Мьют — тайм-аут участника сервера.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Отправить участников подумать о своем поведении')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Использование:')}",
                        value=f"`{prefix}mute {get_language(ctx.guild.id,'{@пользователь}')} {mutime}:60 SECS  reason:{get_language(ctx.guild.id,'[причина]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргументы:')}",
                        value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{mutime}` {get_language(ctx.guild.id,'или')} `{muits_time}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Примеры:')}",
                        value=f"`{prefix}mute {get_language(ctx.guild.id,'@пользователь')} 60 SECS {get_language(ctx.guild.id,'Спам сообщениями.')}`\n╰ {get_language(ctx.guild.id,'Бот выдаст тайм-аут нарушителю.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        value=f"{get_language(ctx.guild.id,'Снять у нарушителя тайм-аут.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Право у пользователя:')}",
                        value=f"{get_language(ctx.guild.id,'Отправить участников подумать о своем поведении')}",
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
                        value=f"`{prefix}unmute {get_language(ctx.guild.id,'@пользователь')}`\n╰ {get_language(ctx.guild.id,'Бот снимет тайм-аут у нарушителя.')}",
                        inline=False,
                    )
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_author(
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                        name=f"vega-bot.ru",
                        url="https://vega-bot.ru/",
                        icon_url=self.client.get_user(795551166393876481).avatar.replace(
                            size=1024, format="png"
                        ),
                    )
                    embed.set_footer(
                        icon_url=self.client.get_user(351020816466575372).avatar.replace(
                            size=1024
                        ),
                        text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
                    )
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}",
                    description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{prefix}help Info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{prefix}help Owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{prefix}help Admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{prefix}help Moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{prefix}help Fun` — {get_language(ctx.guild.id, 'команды веселья')}.",
                    color=0xE21E1E,
                )
                embed.set_author(
                    name=f"vega-bot.ru",
                    url="https://vega-bot.ru/",
                    icon_url=self.client.get_user(795551166393876481).avatar.replace(
                        size=1024, format="png"
                    ),
                )
                embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                embed.set_footer(
                    icon_url=self.client.get_user(351020816466575372).avatar.replace(
                        size=1024
                    ),
                    text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
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
                    embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                    embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                    await inter.reply(embed=embed, components=[row_i])
                elif option.lower() in ["antimsg"]:
                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} antimsg", color=0xd81911)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Включите или отключите автоматическое удаление сообщений оффлайн ботов. VEGA ⦡#7724 будет удалять сообщения неизвестных ботов, которые находятся не в сети.')}", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}antimsg {get_language(ctx.guild.id,'{on}')}`", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}antimsg on`\n╰ {get_language(ctx.guild.id,'Антисообщения включатся.')}\n\n`{prefix}antimsg off`\n╰ {get_language(ctx.guild.id,'Антисообщения отключатся.')}", inline=False)
                    embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                    embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                    await inter.reply(embed=embed, components=[row_i])
    """

    """
                    elif option.lower() in ["*info"]:
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id, '❓ Группа: Информация')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                            {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}ping` — {get_language(ctx.guild.id, 'пинг бота и состояние шардов.')}\n`{prefix}info` — {get_language(ctx.guild.id,'информация о боте.')}\n`{prefix}stats` — {get_language(ctx.guild.id,'статистика бота.')}\n`{prefix}server` — {get_language(ctx.guild.id,'информация о сервере.')}\n`{prefix}links` — {get_language(ctx.guild.id,'полезные ссылки.')}\n`{prefix}wlbots` — {get_language(ctx.guild.id,'белый список ботов.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                        await inter.reply(embed=embed, components=[row_i])
                    elif option.lower() in ["*fun"]:
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Веселье')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                    ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}8ball` — {get_language(ctx.guild.id,'задать вопрос шару.')}\n`{prefix}avatar` — {get_language(ctx.guild.id,'посмотреть аватар пользователя.')}\n`{prefix}emoji` — {get_language(ctx.guild.id,'посмотреть эмодзи.')}\n`{prefix}random` — {get_language(ctx.guild.id,'рандомное число, от и до.')}\n`{prefix}math` — {get_language(ctx.guild.id,'обычный калькулятор.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                        await inter.reply(embed=embed, components=[row_i])
                    elif option.lower() in ["*owner"]:
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Владельца')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                    ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}reset` — {get_language(ctx.guild.id,'сброс настроек бота.')}\n`{prefix}rgive` — {get_language(ctx.guild.id,'выдать всем роль.')}\n`{prefix}rselect` — {get_language(ctx.guild.id,'забрать у всех роль.')}\n`{prefix}antibot` — {get_language(ctx.guild.id,'функция Антибот.')}\n`{prefix}antiinvite` — {get_language(ctx.guild.id,'функция Анти приглашения.')}\n`{prefix}ignore` — {get_language(ctx.guild.id,'игнорировать ботов.')}\n`{prefix}pass` — {get_language(ctx.guild.id,'пропуск для бота.')}\n`{prefix}delchannels` — {get_language(ctx.guild.id,'удалить спам каналы | категории.')}\n`{prefix}delroles` — {get_language(ctx.guild.id,'удалить спам роли.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                        await inter.reply(embed=embed, components=[row_i])
                    elif option.lower() in ["*admin"]:
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Администратора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                    ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}prefix` — {get_language(ctx.guild.id,'сменить префикс боту.')}\n`{prefix}log` — {get_language(ctx.guild.id,'указать канал логов.')}\n`{prefix}channel` — {get_language(ctx.guild.id,'ограничить команды бота по каналам.')}\n`{prefix}rmute` — {get_language(ctx.guild.id,'указать роль Мьюта.')}\n`{prefix}settings` — {get_language(ctx.guild.id,'настройки бота.')}\n`{prefix}list` — {get_language(ctx.guild.id,'существующие списки.')}\n`{prefix}echo` — {get_language(ctx.guild.id,'текст от лица бота.')}\n`{prefix}emb` — {get_language(ctx.guild.id,'текст в панели от лица бота.')}\n`{prefix}slowmode` — {get_language(ctx.guild.id,'установить медленный режим в канале.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                        await inter.reply(embed=embed, components=[row_i])
                    elif option.lower() in ["*moder"]:
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Модератора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                    ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{prefix}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                        embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{prefix}checkwl` — {get_language(ctx.guild.id,'проверить бота в белом списке.')}\n`{prefix}ban` — {get_language(ctx.guild.id,'забанить пользователя.')}\n`{prefix}unban` — {get_language(ctx.guild.id,'разбанить пользователя.')}\n`{prefix}kick` — {get_language(ctx.guild.id,'кикнуть пользователя.')}\n`{prefix}clear` — {get_language(ctx.guild.id,'очистить чат.')}\n`{prefix}uclear` — {get_language(ctx.guild.id,'очистить сообщения указанного пользователя.')}\n`{prefix}rolen` — {get_language(ctx.guild.id,'посмотреть кол-во пользователей с ролью.')}\n`{prefix}user` — {get_language(ctx.guild.id,'информация о пользователе.')}\n`{prefix}mute` — {get_language(ctx.guild.id,'замьютить пользователя.')}\n`{prefix}unmute` — {get_language(ctx.guild.id,'размьютить пользователя.')}", inline=False)
                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
    """

    """         row = ActionRow(Button(style=ButtonStyle.blurple, emoji="<:info:860380081268588545>", custom_id = '❓'), Button(style=ButtonStyle.blurple, emoji="<:owner:860380081594564688>", custom_id = '👑'),
                    Button(style=ButtonStyle.blurple, emoji="<:admin:860380081536761886>", custom_id = '⚙️'), Button(style=ButtonStyle.blurple, emoji="<:moder:860380081627856906>", custom_id = '🛠'), Button(style=ButtonStyle.blurple, emoji="<:fun:860380081637031936>", custom_id = '🎉'))

                back = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vega-bot.ru/"))
                back1 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад1'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vega-bot.ru/"))                
                back2 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад2'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vega-bot.ru/"))                
                back3 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад3'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vega-bot.ru/"))                
                back4 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад4'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vega-bot.ru/"))                
                back5 = ActionRow(Button(style=ButtonStyle.blurple, label=f"{get_language(ctx.guild.id, 'Назад')}", custom_id = 'Назад5'), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '📚 Документация')}", url="https://never-see.gitbook.io/vega-bot/v/russian/"), Button(style=ButtonStyle.link, label=f"{get_language(ctx.guild.id, '🌐 Сайт')}", url="https://vega-bot.ru/"))                
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
                            embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                            await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuinfo, back])
                            
                            #Меню информации о команде helpmenuinfo
                            def check(inter):
                                return inter.message.id == msg.id

                            while True:
                                try:
                                    inter = await self.client.multiple_wait_for(
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuinfo, back])
                                    elif button_id == "Назад":
                                        embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                        embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed1.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                    elif helpvaluei == "info2":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} info", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Вы можете прочитать информацию о боте VEGA ⦡#7724.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}info`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}info`\n╰ {get_language(ctx.guild.id,'Покажет информацию о боте VEGA ⦡#7724.')}", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                    elif helpvaluei == "info3":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} stats", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value='Посмотреть статистику бота VEGA ⦡#7724.', inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}stats`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}stats`\n╰ Покажет статистику бота VEGA ⦡#7724.", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                    elif helpvaluei == "info4":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} server", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                            {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотреть информацию о сервере. Количество ролей, каналов, пользователей и т.д.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}server`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}serverinfo`\n`{prefix}server-info`', inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}server`\n╰ {get_language(ctx.guild.id,'Покажет информацию о сервере.')}", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                    elif helpvaluei == "info5":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} links", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Бот отправит вам в лс ссылку сервера поддержки и документацию.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}links`", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                    elif helpvaluei == "info6":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} wlbots", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотреть или скачать белый список ботов.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}wlbots`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}wlbots`\n╰ {get_language(ctx.guild.id,'Бот отправит вам белый список.')}", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back1])
                                    
                        elif helpvalue == "👑":
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Владельца')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                            embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}reset` — {get_language(ctx.guild.id,'сброс настроек бота.')}\n`{pre}rgive` — {get_language(ctx.guild.id,'выдать всем роль.')}\n`{pre}rselect` — {get_language(ctx.guild.id,'забрать у всех роль.')}\n`{pre}antibot` — {get_language(ctx.guild.id,'функция Антибот.')}\n`{pre}antimsg` — {get_language(ctx.guild.id,'функция Антисообщения.')}\n`{pre}antiinvite` — {get_language(ctx.guild.id,'функция Анти приглашения.')}\n`{pre}ignore` — {get_language(ctx.guild.id,'игнорировать ботов.')}\n`{pre}pass` — {get_language(ctx.guild.id,'пропуск для бота.')}\n`{pre}delchannels` — {get_language(ctx.guild.id,'удалить спам каналы | категории.')}\n`{pre}delroles` — {get_language(ctx.guild.id,'удалить спам роли.')}", inline=False)
                            embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                            embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                            await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuowner, back])


                            def check(inter):
                                return inter.message.id == msg.id

                            while True:
                                try:
                                    inter = await self.client.multiple_wait_for(
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuowner, back])
                                    elif button_id == "Назад":
                                        embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                        embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed1.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                    elif helpvalueo == "owner8":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} delchannels", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Бот начнет удалять каналы и | или категории с одинаковым названием.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}delchannels {get_language(ctx.guild.id,'{название канала}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{название канала}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}delchannels {get_language(ctx.guild.id,'Тест')}`\n╰ {get_language(ctx.guild.id,'Удалит одинаковые каналы и | или категории.')}", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                    elif helpvalueo == "owner9":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} delroles", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Бот начнет удалять роли с одинаковым названием.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}delroles {get_language(ctx.guild.id,'{@роль}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{название роли}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}delroles {get_language(ctx.guild.id,'@роль')}`\n╰ {get_language(ctx.guild.id,'Удалит одинаковые роли.')}", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
                                    elif helpvalueo == "owner10":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} antimsg", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Включите или отключите автоматическое удаление сообщений оффлайн ботов. VEGA ⦡#7724 будет удалять сообщения неизвестных ботов, которые находятся не в сети.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Владелец')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}antimsg {get_language(ctx.guild.id,'{on}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{on}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{off}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}antimsg on`\n╰ {get_language(ctx.guild.id,'Антисообщения включатся.')}\n\n`{prefix}antimsg off`\n╰ {get_language(ctx.guild.id,'Антисообщения отключатся.')}", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back2])
            
                        elif helpvalue == "⚙️":
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Администратора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                            embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}log` — {get_language(ctx.guild.id,'указать канал логов.')}\n`{pre}channel` — {get_language(ctx.guild.id,'ограничить команды бота по каналам.')}\n`{pre}rmute` — {get_language(ctx.guild.id,'указать роль Мьюта.')}\n`{pre}settings` — {get_language(ctx.guild.id,'настройки бота.')}\n`{pre}list` — {get_language(ctx.guild.id,'существующие списки.')}\n`{pre}echo` — {get_language(ctx.guild.id,'текст от лица бота.')}\n`{pre}emb` — {get_language(ctx.guild.id,'текст в панели от лица бота.')}\n`{pre}slowmode` — {get_language(ctx.guild.id,'установить медленный режим в канале.')}", inline=False)
                            embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                            embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                            await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuadmin, back])
                            def check(inter):
                                return inter.message.id == msg.id
                            while True:
                                try:
                                    inter = await self.client.multiple_wait_for(
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenuadmin, back])
                                    elif button_id == "Назад":
                                        embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                        embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed1.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                    elif helpvaluea == "admin5":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} settings", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Вы можете посмотреть все настройки бота.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}settings`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{prefix}stg`', inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}settings`\n╰ {get_language(ctx.guild.id,'Посмотреть настройки.')}", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                                    elif helpvaluea == "admin6":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} list", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Посмотреть список ограниченных каналов, игнорируемых ботов, пропусков или количество ботов в белом списке.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Право у пользователя:')}", value=f"{get_language(ctx.guild.id,'Администратор')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}list {get_language(ctx.guild.id,'{channels}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{channels}')}`; `{get_language(ctx.guild.id,'{ignores}')}`; `{get_language(ctx.guild.id,'{pass}')}`; `{get_language(ctx.guild.id,'{wl}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"`{prefix}list channels`\n╰ {get_language(ctx.guild.id,'Список ограниченных каналов.')}\n\n`{prefix}list ignores`\n╰ {get_language(ctx.guild.id,'Список игнорируемых ботов.')}\n\n`{prefix}list pass`\n╰ {get_language(ctx.guild.id,'Боты, у которых есть пропуска на сервер.')}\n\n`{prefix}list wl`\n╰ {get_language(ctx.guild.id,'Белый список ботов.')}", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back3])
                        
                        elif helpvalue == "🛠":
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Для Модератора')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                            embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}checkwl` — {get_language(ctx.guild.id,'проверить бота в белом списке.')}\n`{pre}ban` — {get_language(ctx.guild.id,'забанить пользователя.')}\n`{pre}unban` — {get_language(ctx.guild.id,'разбанить пользователя.')}\n`{pre}kick` — {get_language(ctx.guild.id,'кикнуть пользователя.')}\n`{pre}clear` — {get_language(ctx.guild.id,'очистить чат.')}\n`{pre}uclear` — {get_language(ctx.guild.id,'очистить сообщения указанного пользователя.')}\n`{pre}rolen` — {get_language(ctx.guild.id,'посмотреть кол-во пользователей с ролью.')}\n`{pre}user` — {get_language(ctx.guild.id,'информация о пользователе.')}\n`{pre}mute` — {get_language(ctx.guild.id,'замьютить пользователя.')}\n`{pre}unmute` — {get_language(ctx.guild.id,'размьютить пользователя.')}", inline=False)
                            embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                            embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                            await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenumoder, back])
                            def check(inter):
                                return inter.message.id == msg.id
                            while True:
                                try:
                                    inter = await self.client.multiple_wait_for(
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenumoder, back])
                                    elif button_id == "Назад":
                                        embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                        embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed1.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back4])

                        elif helpvalue == "🎉":
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Группа: Веселье')}", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                ㅤ{get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}\n\n{get_language(ctx.guild.id, f'• Узнать информацию о команде:')} `{pre}{get_language(ctx.guild.id, 'help [команда]')}`", color=0xd81911)
                            embed.add_field(name=f"{get_language(ctx.guild.id, 'Команды:')}", value=f"`{pre}8ball` — {get_language(ctx.guild.id,'задать вопрос шару.')}\n`{pre}avatar` — {get_language(ctx.guild.id,'посмотреть аватар пользователя.')}\n`{pre}emoji` — {get_language(ctx.guild.id,'посмотреть эмодзи.')}\n`{pre}random` — {get_language(ctx.guild.id,'рандомное число, от и до.')}\n`{pre}math` — {get_language(ctx.guild.id,'обычный калькулятор.')}", inline=False)
                            embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                            embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                            await intermenu.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenufun, back])


                            def check(inter):
                                return inter.message.id == msg.id

                            while True:
                                try:
                                    inter = await self.client.multiple_wait_for(
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[helpmenufun, back])
                                    elif button_id == "Назад":
                                        embed1 = discord.Embed(title=f"{get_language(ctx.guild.id, ':wrench: Список доступных команд:')}", description=f"{get_language(ctx.guild.id, 'Префикс на сервере:')} `{prefix}`\n{get_language(ctx.guild.id,'Сменить язык:')} `{prefix}{get_language(ctx.guild.id,'lang en')}`\n\n<:info:860380081268588545> `{pre}help *info` — {get_language(ctx.guild.id, 'команды информации')}.\n\n<:owner:860380081594564688> `{pre}help *owner` — {get_language(ctx.guild.id, 'команды для Владельца')}.\n\n<:admin:860380081536761886> `{pre}help *admin` — {get_language(ctx.guild.id, 'команды для Администратора')}.\n\n<:moder:860380081627856906> `{pre}help *moder` — {get_language(ctx.guild.id, 'команды для Модератора')}.\n\n<:fun:860380081637031936> `{pre}help *fun` — {get_language(ctx.guild.id, 'команды веселья')}.", color=0xe21e1e)
                                        embed1.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed1.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back5])
                                    elif helpvaluef == "fun3":
                                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'❓ Команда:')} emoji", description=f"> {get_language(ctx.guild.id, '**{**_обязательный параметр_**}**')} ㅤ\
                                            {get_language(ctx.guild.id, '**[**_необязательный параметр_**]**')}", color=0xd81911)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Вы можете осмотреть и скачать эмодзи.')}", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Использование:')}", value=f"`{prefix}emoji {get_language(ctx.guild.id,'{эмодзи}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`{get_language(ctx.guild.id,'{эмодзи}')}`", inline=False)
                                        embed.add_field(name=f"{get_language(ctx.guild.id,'Примеры:')}", value=f"{prefix}emoji <:python:826158844555427891>\n╰ {get_language(ctx.guild.id,'Посмотреть эмодзи.')}", inline=False)
                                        embed.set_image(url="https://i.postimg.cc/tRrYVjbx/VEGA-line.png")
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
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
                                        embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                                        await inter.reply(type=ResponseType.UpdateMessage, embed=embed, components=[back5])
    """


def setup(client):
    client.add_cog(class_help(client))
