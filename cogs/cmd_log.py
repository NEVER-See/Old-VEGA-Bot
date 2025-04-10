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

class class_log(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Указать канал с логами
    @commands.slash_command(name="log", description="Set the log channel | Установить канал логов")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def log(self, ctx, option: option = commands.Param(description="Select an option | Укажите опцию"), channel: discord.TextChannel=None):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if option:
                if option==2: channel = False
            if option is not None and channel is not None:
                w = gdata('vega', 'logchannel')
    #                if not str(ctx.guild.id) in w:
    #                    w.update({str(ctx.guild.id):''})
                if option==1:
                    if not str(ctx.guild.id) in w:
                        w.update({str(ctx.guild.id):str(channel.id)})
                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Для логов указан канал:')} {channel.mention}", color=0x4acb84)
                        embed.set_footer(text=f'ID: {channel.id}')
                        await ctx.send(embed=embed, delete_after=15.0)
                    else:
                        c = self.client.get_channel(int(w[str(ctx.guild.id)]))
                        if c:
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Канал логов уже указан')} — {c.mention}!", color=0xcc1a1d)
                            embed.set_footer(text=f'ID: {c.id}')
                            await ctx.send(embed=embed, delete_after=10.0)
                        else:
                            del w[str(ctx.guild.id)]
                            w.update({str(ctx.guild.id):str(channel.id)})
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Для логов указан канал:')} {channel.mention}", color=0x4acb84)
                            embed.set_footer(text=f'ID: {channel.id}')
                            await ctx.send(embed=embed, delete_after=15.0)
                elif option==2:
                    if str(ctx.guild.id) in w:
                        del w[str(ctx.guild.id)]
                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Канал логов удален!')}", color=0xcc1a1d)
                        await ctx.send(embed=embed, delete_after=15.0)
                    else:
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,':warning: Канал логов не указан!')}", color=0xfcc21b)
                        await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,':warning: Неизвестная опция!')}", color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
                wdata('vega', 'logchannel', w)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию и канал(чат)!')}", color=0x8899a6)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Вы можете указать или отключить боту канал с логами.')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{#канал}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID канала}')}`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"`{ctx.prefix}log add {get_language(ctx.guild.id,'#канал')}` {get_language(ctx.guild.id,'или')} `{ctx.prefix}log remove`" , inline=False)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_log(client))