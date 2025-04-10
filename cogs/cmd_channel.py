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
    add = 1
    remove = 2

class class_channel(commands.Cog):
    def __init__(self, client):
        self.client = client


    #Добавить или убрать канал для команд бота
    @commands.slash_command(name="channel", description="Restrict the bot by channels | Ограничить бота по каналам")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def channel(self, inter, option: option = commands.Param(description="Select an option | Укажите опцию"), *, channel: discord.TextChannel = commands.Param(name="channel", description="Specify the channel or its ID | Укажите канал или его ID")):
        ctx=inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if option is not None:
                if option and channel:
                    w = gdata('vega', 'channel_rights')
                    if not str(ctx.guild.id) in w:
                        w.update({str(ctx.guild.id):''})
                    if option==1:
                        if not str(channel.id) in w[str(ctx.guild.id)]:
                            w.update({str(ctx.guild.id):w[str(ctx.guild.id)] + str(channel.id) + ' '})
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Канал')} **#{channel.name}** {get_language(ctx.guild.id,'разрешен для бота.')}", description=f"{self.client.user.mention} {get_language(ctx.guild.id,'станет отвечать на команды в данном канале!')}", color=0x4acb84)
                            embed.set_footer(text=f'ID: {channel.id}')
                            await ctx.send(embed=embed, delete_after=15.0)
                        else:
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Канал')} **#{channel.name}** {get_language(ctx.guild.id,'уже занесен в список!')}", color=0xcc1a1d)
                            embed.set_footer(text=f'ID: {channel.id}')
                            await ctx.send(embed=embed, ephemeral=True)
                    elif option==2:
                        if str(channel.id) in w[str(ctx.guild.id)]:
                            w.update({str(ctx.guild.id):w[str(ctx.guild.id)].replace(str(f"{channel.id} "), '')})
                            if len(w[str(ctx.guild.id)]) == 0:
                                del w[str(ctx.guild.id)]
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Канал')} **#{channel.name}** {get_language(ctx.guild.id,'удален из списка!')}", color=0xcc1a1d)
                            embed.set_footer(text=f'ID: {channel.id}')
                            await ctx.send(embed=embed, delete_after=15.0)
                        else:
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,':warning: Канал')} **#{channel.name}** {get_language(ctx.guild.id,'отсутствует в списке!')}", color=0xfcc21b)
                            embed.set_footer(text=f'ID: {channel.id}')
                            await ctx.send(embed=embed, ephemeral=True)
                    else:
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,':warning: Неизвестная опция!')}", color=0xfcc21b)
                        await ctx.send(embed=embed, ephemeral=True)
                    wdata('vega', 'channel_rights', w)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию и канал(чат)!')}", color=0x8899a6)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Вы можете ограничить бота по каналам.')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{#канал}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID канала}')}`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}channel add {get_language(ctx.guild.id,'#канал')}", inline=False)
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                await ctx.send(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(class_channel(client))