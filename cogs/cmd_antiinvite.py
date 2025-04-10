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

class Animal(int, Enum):
    on = 1
    off = 2

class class_antiinvite(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Анти приглашения
    @commands.slash_command(name="antiinvite", description="Anti-invitation function | Функция Анти приглашения")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def antiinvite(self, inter, option: Animal = commands.Param(description="Select an option | Укажите опцию")):
        ctx=inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                if ctx.author == ctx.guild.owner:
                    if option is not None:
                        if option:
                            data = gdata('vega', 'antiinvite')
                            if option != None:
                                try:
                                    enabled = data[str(ctx.guild.id)]
                                except KeyError:
                                    enabled = False
                                if option == 1:
                                    if not enabled:
                                        data[str(ctx.guild.id)] = True
                                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Анти приглашения были включены на вашем сервере!')}", color=0x43b581)
                                        await ctx.send(embed=embed, delete_after=12.0)
                                    else:
                                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Анти приглашения уже включены на вашем сервере!')}", color=0xfcc21b)
                                        await ctx.send(embed=embed, delete_after=10.0)
                                        ctx.command.reset_cooldown(ctx)
                                elif option == 2:
                                    if enabled:
                                        data[str(ctx.guild.id)] = False
                                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Анти приглашения были отключены на вашем сервере!')}", color=0xcc1a1d)
                                        await ctx.send(embed=embed, delete_after=12.0)
                                    else:
                                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Анти приглашения уже отключены на вашем сервере!')}", color=0xfcc21b)
                                        await ctx.send(embed=embed, delete_after=10.0)
                                        ctx.command.reset_cooldown(ctx)
                                else:
                                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Неизвестная опция!')}", color=0xfcc21b)
                                    await ctx.send(embed=embed, delete_after=8.0)
                                    ctx.command.reset_cooldown(ctx)
                                wdata('vega', 'antiinvite', data)
                    else:
                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию!')}", color=0x8899a6)
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Вы можете включить или отключить анти приглашения. Действует по всем каналам!')}", inline=False)
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'on')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'off')}`", inline=False)
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}antiinvite on", inline=False)
                        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                        await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: **Вы не являетесь Владельцем данного сервера!**')}", color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_antiinvite(client))