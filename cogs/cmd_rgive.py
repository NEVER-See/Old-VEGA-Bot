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
    all = 1

class class_rgive(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Выдать всем пользователям 1 роль
    @commands.slash_command(name="rgive", description="Assign a role to all users | Выдать роль всем пользователям", case_insensitive=True)
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True, manage_roles=True)
    @commands.cooldown(1, 300, commands.BucketType.guild)
    async def rgive(self, ctx, option: option = commands.Param(description="Select an option | Укажите опцию"), role: discord.Role=commands.Param(name="role", description="Specify the role or its ID | Укажите роль или её ID")):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                if ctx.author == ctx.guild.owner:
                    if option == 1 and role:
                        user = ctx.author
                        getrole = discord.utils.get(ctx.guild.roles, id = role.id)

                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется раздача роли пользователям...')}", color=0xf4900c)
                        await ctx.send(embed=embed)
                        try:
                            for member in ctx.guild.members:
                                if not member.bot:
                                    await member.add_roles(getrole)
                            if member:
                                embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Я выдал всем роль')} {role.mention}", color=0x43b581)
                                try:await ctx.edit_original_message(embed=embed)
                                except:pass
                        except:
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Я не смог выдать всем роль')} {role.mention}.\n— {get_language(ctx.guild.id,'Видимо моя роль находится ниже роли')} {role.mention}.", color=0xcc1a1d)
                            try:await ctx.edit_original_message(embed=embed)
                            except:pass
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
    client.add_cog(class_rgive(client))