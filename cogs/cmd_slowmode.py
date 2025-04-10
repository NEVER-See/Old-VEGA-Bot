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
from enum import Enum

class option(int, Enum):
    set = 1
    remove = 2

class class_slowmode(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Медленный режим для канала
    @commands.slash_command(name="slowmode", description="Set slow mode | Установить медленный режим")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(send_messages=True, manage_channels=True)
    @commands.has_permissions(administrator=True)
    async def slowmode(self, ctx, option: option = commands.Param(description="Select an option | Укажите опцию"), seconds=None):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if option == 1:
                seconds = int(seconds)
                if 0 <= seconds <= 21600:
                    await ctx.channel.edit(slowmode_delay=seconds)
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Медленный режим установлен на')} `{seconds}` {get_language(ctx.guild.id,'сек')}.", color=0x43b581)
                    await ctx.send(embed=embed, delete_after=8.0)
                else:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Максимальное число `21600`, а минимальное `0`!')}", color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
            elif option == 2:
                    await ctx.channel.edit(slowmode_delay=0)
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Медленный режим установлен на')} `None`.", color=0x43b581)
                    await ctx.send(embed=embed, delete_after=8.0)
def setup(client):
    client.add_cog(class_slowmode(client))