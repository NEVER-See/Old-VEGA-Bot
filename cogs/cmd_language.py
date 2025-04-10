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
    ru = 1
    en = 2

class class_language(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Смена языка (RU; EN)
    @commands.slash_command(name="language", description="Change the language of the bot | Сменить язык боту")
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def language(self, inter, option: option = commands.Param(description="Select an option | Укажите опцию")):
        ctx=inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                if option is not None:
                    if option:
                        data = gdata('vega', 'language')
                        if option != None:
                            try:
                                enabled = data[str(ctx.guild.id)]
                            except KeyError:
                                enabled = False
                            if option==1:
                                if not enabled:
                                    data[str(ctx.guild.id)] = True
                                    embed = discord.Embed(description=f'<a:vega_check_mark:821700784927801394> Русский язык успешно установлен!', color=0x43b581)
                                    await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    embed = discord.Embed(description=f':warning: Русский язык уже установлен!', color=0xfcc21b)
                                    await ctx.send(embed=embed, delete_after=12.0)
                            elif option==2:
                                if enabled:
                                    data[str(ctx.guild.id)] = False
                                    embed = discord.Embed(description=f'<a:vega_check_mark:821700784927801394> English language has been successfully installed!', color=0x43b581)
                                    await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    embed = discord.Embed(description=f':warning: English is already installed!', color=0xfcc21b)
                                    await ctx.send(embed=embed, delete_after=12.0)
                            wdata('vega', 'language', data)
                        else:
                            try:
                                enabled = data[str(ctx.guild.id)]
                            except KeyError:
                                enabled = False
                            if enabled:
                                embed = discord.Embed(description=f'<a:vega_check_mark:821700784927801394> Русский язык уже установлен!', color=0x43b581)
                                await ctx.send(embed=embed, ephemeral=True)
                            else:
                                embed = discord.Embed(description=f'<a:vega_check_mark:821700784927801394> English is already installed!', color=0x43b581)
                                await ctx.send(embed=embed, ephemeral=True)
                else:
                    data = gdata('vega', 'language')
                    try:
                        enabled = data[str(ctx.guild.id)]
                    except KeyError:
                        enabled = False
                    if enabled:
                        #ru
                        embed = discord.Embed(description='<a:loupe:811137886141153320> Укажите язык!', color=0x8899a6)
                        embed.add_field(name='Описание:', value=f"Установите язык для бота на вашем сервере.", inline=False)
                        embed.add_field(name='Аргумены:', value=f"`ru | en`", inline=False)
                        embed.add_field(name='Подобные:', value=f"`{ctx.prefix}lang ru`", inline=False)
                        embed.add_field(name='Пример:', value=f"{ctx.prefix}language ru", inline=False)
                        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.command.reset_cooldown(ctx)
                    else:
                        #en
                        embed = discord.Embed(description='<a:loupe:811137886141153320> Specify the language!', color=0x8899a6)
                        embed.add_field(name='Description:', value=f"Set the language for the bot on your server.", inline=False)
                        embed.add_field(name='Arguments:', value=f"`ru | en`", inline=False)
                        embed.add_field(name='Similar:', value=f"`{ctx.prefix}lang en`", inline=False)
                        embed.add_field(name='Example:', value=f"{ctx.prefix}language en", inline=False)
                        embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.command.reset_cooldown(ctx)
            else:
                data = gdata('vega', 'language')
                try:
                    enabled = data[str(ctx.guild.id)]
                except KeyError:
                    enabled = False
                if enabled:
                    #RU
                    embed = discord.Embed(description=f':warning: Эта команда доступна только в определенных каналах!', color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
                else:
                    #EN
                    embed = discord.Embed(description=f':warning: This command is only available in certain channels!', color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_language(client))