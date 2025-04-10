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
from memory_profiler import memory_usage

class class_ram(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Проверка потребления памяти в хероку
    @commands.command()
    @commands.guild_only()
    async def ram(self, ctx):
        if ctx.author.id in config["owner_ids"]:
            await ctx.message.delete()
            ram = round(memory_usage()[0], 2)
            if 500 >= ram:
                ram0 = "https://cdn.discordapp.com/attachments/713751423128698950/865491367731527700/RAM_is_not_full.png"
            elif 500 < ram:
                ram0 = "https://cdn.discordapp.com/attachments/713751423128698950/865491370231463936/RAM_is_almost_full.png"
            elif 900 < ram:
                ram0 = "https://cdn.discordapp.com/attachments/713751423128698950/865491371976294410/RAM_is_full.png"
            embed = discord.Embed(description=f"{get_language(ctx.guild.id, f'Использовано:')} **{ram} MB**",  color=0xd9728d)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/713751423128698950/859811042229354536/c3cc66cf15e70eb3866018146e20cba7.png")
            embed.set_author(name=f"{get_language(ctx.guild.id, 'Оперативная память:')}", icon_url=f"{ram0}")
            await ctx.send(embed=embed, delete_after=15)
        else:
            pass

def setup(client):
    client.add_cog(class_ram(client))