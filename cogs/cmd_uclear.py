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


class class_uclear(commands.Cog):
    def __init__(self, client):
        self.client = client

    """#Команда недоработана! Очистка чата упомянутого пользователя
    @commands.slash_command(name="uclear", description="Clear user messages | Очистить сообщения пользователя")
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def uclear(self, ctx, user:discord.Member=commands.Param(description="Specify the user or his ID | Укажите пользователя или его ID")):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            def _check(message):
                return message.author == user and message.created_at.timestamp() > time.time() - (86400*7)

            if user:
        #    if 0 < limit <= 100:
                with ctx.channel.typing():
        #            deleted = await ctx.channel.purge(limit=limit, check=_check)
                    deleted = await ctx.channel.purge(limit=None, check=_check)
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'♻️ Очищено')} **{len(deleted):,}**  {get_language(ctx.guild.id,'сообщений пользователя')} {user.mention} {get_language(ctx.guild.id,' ')}", color=0xfcc21b)
                    await ctx.send(embed=embed, delete_after=10.0)
        #    else:
        #        msg = ctx.message
        #        user = msg.author
        #        await msg.add_reaction('❗')
        #        embed = discord.Embed(description='❗️ Максимальное количество сообщений для очистки **100**!', color=0xbe1931)
        #        await ctx.send(embed=embed, delete_after=7.0)

        #---------------------------------------------------------------------------------------------------------------------------
        #    await ctx.message.delete()
        #    await ctx.channel.purge(limit=1, check=lambda m: m.author==user)
        #    await ctx.send('♻️ Сообщения были очищены!', delete_after=7.0)
        #---------------------------------------------------------------------------------------------------------------------------"""
def setup(client):
    client.add_cog(class_uclear(client))