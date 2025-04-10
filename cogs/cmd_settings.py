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

prefix = "/"

class class_settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Посмотреть настройки бота
    @commands.slash_command(name="settings", description="Bot settings | Настройки бота", case_insensitive=True)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def settings(self, ctx):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            lang = gdata('vega', 'language')
            try:
                enabled = lang[str(ctx.guild.id)]
            except KeyError:
                enabled = False
            if enabled:
                slang = "Русский"
            else:
                slang = "English"

            ab = gdata('vega', 'antibot')
            try:
                enabled = ab[str(ctx.guild.id)]
            except KeyError:
                enabled = False
            if enabled:
                abon = "<a:on:863478700891963402>"
            else:
                abon = "<a:off:863478700845694987>"

            amsg = gdata('vega', 'antimsg')
            try:
                enabled = amsg[str(ctx.guild.id)]
            except KeyError:
                enabled = False
            if enabled:
                amsg0 = "<a:on:863478700891963402>"
            else:
                amsg0 = "<a:off:863478700845694987>"
            
            ai = gdata('vega', 'antiinvite')
            try:
                enabled = ai[str(ctx.guild.id)]
            except KeyError:
                enabled = False
            if enabled:
                aion = "<a:on:863478700891963402>"
            else:
                aion = "<a:off:863478700845694987>"
            
            log = gdata('vega', 'logchannel')
            try:
                l = self.client.get_channel(int(log[str(ctx.guild.id)]))
                if str(ctx.guild.id) in log:
                    logch = f"{l.mention}"
                else:
                    logch = "`None`"
            except:
                logch = "`None`"

            mr = gdata('vega', 'muterole')
            try:
                c = ctx.guild.get_role(int(mr[str(ctx.guild.id)]))
                if str(ctx.guild.id) in mr and c:
                    muter = f"{c.mention}"
                else:
                    muter = "`None`"
            except:
                muter = "`None`"

            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'🔧 Настройки бота')}", description=f"{get_language(ctx.guild.id,'**🔎 Префикс:**')}  `{prefix}`        <:language:863473448771387402> {get_language(ctx.guild.id,'**Язык:**')} `{slang}`\nㅤ", color=0x202225)
            embed.add_field(name=f"{get_language(ctx.guild.id,'Каналы & Роли:')}", value=f"{get_language(ctx.guild.id,'**📃 Логи:**')} {logch}\n\n<:muted:842447248277241867> {get_language(ctx.guild.id,'**Роль мьюта:**')} {muter}ㅤ", inline=True)
            embed.add_field(name=f"{get_language(ctx.guild.id,'Выключатели:')}", value=f"{abon} **AntiBot**\n\n{amsg0} **AntiMSGBot**\n\n{aion} {get_language(ctx.guild.id,'**Анти приглашение**')}", inline=True)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(class_settings(client))