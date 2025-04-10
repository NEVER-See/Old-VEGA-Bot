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

class class_ignore(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Добавить all, чтобы можно было добавлять всех ботов с сервера в игнор. Необязательно!

    #Игнор ботов
    @commands.slash_command(name="ignore", description="Add a bot to the ignored list | Добавить бота в игнорируемый список")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def ignore(self, inter, option: option = commands.Param(description="Select an option | Укажите опцию"),
        user:discord.User = commands.Param(name="user", description="Specify the bot or its ID | Укажите бота или его ID")
    ):
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
                    if option and user:
                        if user.bot:
                            p = gdata('vega', 'passbots')
                            w = gdata('vega', 'ignorebots')
                            wl = gdata('vega', 'wlbots')
                            if not str(ctx.guild.id) in w:
                                w.update({str(ctx.guild.id):''})
                            if option==1:
                                if str(user.id) in wl[str("Bots")]:
                                    try:
                                        p.update({str(ctx.guild.id):p[str(ctx.guild.id)].replace(str(f"{user.id} "), '')})
                                    except:
                                        pass
                                    w.update({str(ctx.guild.id):w[str(ctx.guild.id)].replace(str(f"{user.id} "), '')})
                                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})", color=0x43b581)
                                    embed.set_footer(text=f'ID: {user.id}')
                                    await ctx.send(embed=embed, delete_after=12.0)
                                elif not str(user.id) in w[str(ctx.guild.id)]:
                                    try:
                                        p.update({str(ctx.guild.id):p[str(ctx.guild.id)].replace(str(f"{user.id} "), '')})
                                    except:
                                        pass
                                    w.update({str(ctx.guild.id):w[str(ctx.guild.id)] + str(user.id) + ' '})
                                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Теперь действия бота')} **{user}** {get_language(ctx.guild.id,'игнорируются!')}", color=0x43b581)
                                    embed.set_footer(text=f'ID: {user.id}')
                                    await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'уже игнорируется!')}", color=0xcc1a1d)
                                    embed.set_footer(text=f'ID: {user.id}')
                                    await ctx.send(embed=embed, delete_after=10.0)
                            elif option==2:
                                if str(user.id) in wl[str("Bots")]:
                                    try:
                                        p.update({str(ctx.guild.id):p[str(ctx.guild.id)].replace(str(f"{user.id} "), '')})
                                    except:
                                        pass
                                    w.update({str(ctx.guild.id):w[str(ctx.guild.id)].replace(str(f"{user.id} "), '')})
                                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})", color=0x43b581)
                                    embed.set_footer(text=f'ID: {user.id}')
                                    await ctx.send(embed=embed, delete_after=12.0)
                                elif str(user.id) in w[str(ctx.guild.id)]:
                                    try:
                                        p.update({str(ctx.guild.id):p[str(ctx.guild.id)].replace(str(f"{user.id} "), '')})
                                    except:
                                        pass
                                    w.update({str(ctx.guild.id):w[str(ctx.guild.id)].replace(str(f"{user.id} "), '')})
                                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Теперь действия бота')} **{user}** {get_language(ctx.guild.id,'не игнорируются!')}", color=0xfcc21b)
                                    embed.set_footer(text=f'ID: {user.id}')
                                    await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'не найден!')}", color=0xcc1a1d)
                                    embed.set_footer(text=f'ID: {user.id}')
                                    await ctx.send(embed=embed, delete_after=10.0)
                            else:
                                embed = discord.Embed(title=f"{get_language(ctx.guild.id,':warning: Неизвестная опция!')}", color=0xfcc21b)
                                await ctx.send(embed=embed, ephemeral=True)
                            wdata('vega', 'ignorebots', w)
                            wdata('vega', 'passbots', p)
                        else:
                            embed = discord.Embed(description=f"<a:vega_x:810843492266803230> **{user.id}** {get_language(ctx.guild.id,'не является ботом!')}", color=0xcc1a1d)
                            await ctx.send(embed=embed, ephemeral=True)
                            ctx.command.reset_cooldown(ctx)
                    else:
                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию и бота!')}", color=0x8899a6)
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Бот (не) будет игнорировать действия указанного бота. Действует на ботов, которые не находятся в белом списке!')}", inline=False)
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{ID бота}')}`", inline=False)
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}ignore add {get_language(ctx.guild.id,'ID бота')}", inline=False)
                        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.command.reset_cooldown(ctx)
                else:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: **Вы не являетесь Владельцем данного сервера!**')}", color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_ignore(client))
    