# -*- coding: utf-8 -*-
import disnake as discord
from disnake.channel import DMChannel
from disnake.ext import tasks
from disnake.utils import get
import asyncio
import datetime
import time
import random
import json
import os
import re
import requests
import pymongo
import typing
import aiohttp
#import word
#import config
#from discord import utils
from disnake.ext import commands
from random import randint
from helper import *
from cache import *


class class_info(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Информация о боте
    @commands.slash_command(name="info", description="Information about the VEGA⦡#7724 bot | Информация о боте VEGA ⦡#7724")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def info(self, inter):
        ctx=inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                prefix="/"
                timestamp = datetime.datetime.now()
                version_bot = open('important_information/version_bot.txt', 'r').readline()
                embed = discord.Embed(title='VEGA ⦡#7724', description=f"{get_language(ctx.guild.id,'Привет! Я создан для защиты сервера от неизвестных ботов. Пока что от селф ботов не защищаю. Моя защита строгая, если ее включить, я буду банить каждого неизвестного бота.')}\n\n{get_language(ctx.guild.id,'Только владелец может включить защиту от ботов! Команда для включения функции **AntiBot**:')} `{prefix}antibot on`\n \n{get_language(ctx.guild.id,'Мой префикс')} `{prefix}`. {get_language(ctx.guild.id,'Введите команду')} `{prefix}help` {get_language(ctx.guild.id,'для более подробной информации о командах.')}\n\n{get_language(ctx.guild.id,'Чтобы сменить язык на английский, напишите команду')} `{prefix}{get_language(ctx.guild.id,'language en`.')}", color=0xe21e1e)
                embed.add_field(name=f"{get_language(ctx.guild.id,'🗃 Версия бота:')}", value=f'{version_bot}', inline=True)
                embed.add_field(name=f"{get_language(ctx.guild.id,'<:vb_developer:931450178488107060> Разработчик:')}", value=f'{self.client.get_user(351020816466575372)}\n`ID: 351020816466575372`\n\n{self.client.get_user(750245767142441000)}\n`ID: 750245767142441000`', inline=True)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Зарегистрирован:')}", value=f"<t:{int(self.client.user.created_at.timestamp())}:F>", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'🔗 Ссылки:')}", value=f"[{get_language(ctx.guild.id,'Документация')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/')})\n[{get_language(ctx.guild.id,'Сайт бота')}]({get_language(ctx.guild.id,'https://vegabot.xyz/vegabot/')})\n[{get_language(ctx.guild.id,'Служба поддержки')}]({get_language(ctx.guild.id,'https://discord.gg/8YhmtsYvpK')})", inline=True)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Особые значки:')}", value=f"{get_language(ctx.guild.id,'<:vb_developer:931450178488107060> — Разработчик бота.')}\n{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}\n<:PREMIUM:933211411805536296> — {get_language(ctx.guild.id,'Premium.')}", inline=True)
                embed.add_field(name=f"<:update:842448151272620032>{get_language(ctx.guild.id,'Coming soon:')}", value=f"`/bot-color` — Embed color change <:PREMIUM_EN_L:933208475406839838><:PREMIUM_EN_R:933208475381694474>\nAutomatic checking of bots  <:PREMIUM_EN_L:933208475406839838><:PREMIUM_EN_R:933208475381694474>\nLocal language change <:PREMIUM_EN_L:933208475406839838><:PREMIUM_EN_R:933208475381694474>", inline=False)
                embed.set_thumbnail(url=self.client.get_user(795551166393876481).avatar.replace(size=1024, format="png"))
                embed.set_footer(icon_url=self.client.get_user(351020816466575372).avatar.replace(size=1024), text=f"{self.client.get_user(351020816466575372)} © 2021 - {timestamp.strftime(r'%Y')} {get_language(ctx.guild.id, 'Все права защищены!')}")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_info(client))