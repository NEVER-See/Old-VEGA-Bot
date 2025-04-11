import disnake as discord
import datetime

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_info(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Информация о боте
    @commands.slash_command(
        name="info",
        description="Information about the VEGA⦡#7724 bot | Информация о боте VEGA ⦡#7724",
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def info(self, inter):
        ctx = inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            prefix = "/"
            timestamp = datetime.datetime.now()
            version_bot = open(
                "important_information/version_bot.txt", "r"
            ).readline()
            embed = discord.Embed(
                title="VEGA ⦡#7724",
                description=f"{get_language(ctx.guild.id,'Привет! Я создан для защиты сервера от участников и неизвестных ботов. Моя защита строгая, если ее включить, я буду банить каждого неизвестного бота, а также участников.')}\n\n{get_language(ctx.guild.id,'Только владелец может включить защиту от ботов и участников! Команда для включения функции **AntiBot**: `/antibot on`. Команда для включения функции **AntiCrash**: `/anticrash on`. (Включить) Запретить редактирование сервера: `/edit-server on`.')}\n\n{get_language(ctx.guild.id,'Мой префикс')} `{prefix}`. {get_language(ctx.guild.id,'Введите команду')} `{prefix}help` {get_language(ctx.guild.id,'для более подробной информации о командах.')}\n\n{get_language(ctx.guild.id,'Чтобы сменить язык на английский, напишите команду')} `{prefix}{get_language(ctx.guild.id,'language en`.')}",
                color=0xE21E1E,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'🗃 Версии:')}",
                value=f"<:VEGA:826158043620311051> {get_language(ctx.guild.id,'Версия бота:')} `{version_bot}`\n\n<:python:826158844555427891> {get_language(ctx.guild.id,'Версия Python:')} `3.8.12`\n\n:books: {get_language(ctx.guild.id,'Библиотека:')} `disnake.py`",
                inline=True,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'<:vb_developer:931450178488107060> Разработчик:')}",
                value=f"{self.client.get_user(351020816466575372)}\n`ID: 351020816466575372`\n\n{self.client.get_user(750245767142441000)}\n`ID: 750245767142441000`",
                inline=True,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'Зарегистрирован:')}",
                value=f"<t:{int(self.client.user.created_at.timestamp())}:F>",
                inline=False,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'🔗 Ссылки:')}",
                value=f"[{get_language(ctx.guild.id,'Документация')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/')})\n[{get_language(ctx.guild.id,'Сайт бота')}]({get_language(ctx.guild.id,'https://vega-bot.ru/')})\n[{get_language(ctx.guild.id,'Служба поддержки')}]({get_language(ctx.guild.id,'https://discord.gg/8YhmtsYvpK')})",
                inline=True,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'Особые значки:')}",
                value=f"{get_language(ctx.guild.id,'<:vb_developer:931450178488107060> — Разработчик бота.')}\n{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}\n<:PREMIUM:933211411805536296> — {get_language(ctx.guild.id,'Premium.')}",
                inline=True,
            )
            embed.add_field(
                name=f"<:update:842448151272620032>{get_language(ctx.guild.id,'Coming soon:')}",
                value=f"`/bot-color` — Embed color change <:PREMIUM_EN_L:933208475406839838><:PREMIUM_EN_R:933208475381694474>\nAutomatic checking of bots  <:PREMIUM_EN_L:933208475406839838><:PREMIUM_EN_R:933208475381694474>\nLocal language change <:PREMIUM_EN_L:933208475406839838><:PREMIUM_EN_R:933208475381694474>",
                inline=False,
            )
            """url=self.client.get_user(795551166393876481).avatar.replace(
                    size=1024, format="png"
                )"""
            """embed.set_thumbnail(
                url="https://i.ibb.co/48Xknx7/VEGA-shild.gif"
            )"""
            embed.set_footer(
                icon_url=self.client.get_user(351020816466575372).avatar.replace(
                    size=1024
                ),
                text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}",
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(class_info(client))
