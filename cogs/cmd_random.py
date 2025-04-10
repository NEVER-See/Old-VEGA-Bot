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


class class_random(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Рандомное число от А до Б
    @commands.slash_command(name="random", description="Randomizer of numbers | Рандомайзер чисел")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.bot_has_permissions(send_messages=True)
    async def random(self, ctx, a:int=commands.Param(name="a", description="Specify the smallest number | Укажите наименьшие число"), b:int=commands.Param(name="b", description="Specify the largest number | Укажите наибольшее число")):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                if a is not None:
                    if a and b:
                        if int(a) >= 0:
                            if int(b) <= 1e+9:
                                """def check(msg):
                                    return msg.author == ctx.author and msg.content.isdigit() and msg.channel == ctx.channel"""
                                
                                x = int(a)
                                y = int(b)
                                if x < y:
                                    value = random.randint(x,y)
                                    await ctx.send(f"{get_language(ctx.guild.id,'Я выбрал:')} **{value}**", ephemeral=True)
                                else:
                                    await ctx.send(f"{get_language(ctx.guild.id,':warning: Пожалуйста, убедитесь, что первое число меньше второго.')}", ephemeral=True)
                                    ctx.command.reset_cooldown(ctx)
                            else:
                                await ctx.send(f"{get_language(ctx.guild.id,':warning: Пожалуйста, убедитесь, что ` второе число ≤ 1000000000 `.')}", ephemeral=True)
                                ctx.command.reset_cooldown(ctx)
                        else:
                            await ctx.send(f"{get_language(ctx.guild.id,':warning: Пожалуйста, убедитесь, что ` первое число ≥ 0 `.')}", ephemeral=True)
                            ctx.command.reset_cooldown(ctx)
                else:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите наименьшее и наибольшее число!')}", color=0x8899a6)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Если хотите выбрать рандомное число, то воспользуйтесь данной командой.')}", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`a` {get_language(ctx.guild.id,'и')} `b`", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Подобные:')}", value=f'`{ctx.prefix}r`\n`{ctx.prefix}rand`', inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}rand 5 10", inline=False)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_random(client))