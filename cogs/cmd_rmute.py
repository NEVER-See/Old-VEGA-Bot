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

class class_rmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Указать роль мьюта
    @commands.slash_command(name="rmute", description="Specify the role of the muted | Указать роль мьюта")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def rmute(self, ctx, option: option = commands.Param(description="Select an option | Укажите опцию"), role: discord.Role=commands.Param(name="role", description="Specify the role or its ID | Укажите роль или её ID")):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if option is not None:
                if option and role:
                    w = gdata('vega', 'muterole')
    #                if not str(ctx.guild.id) in w:
    #                    w.update({str(ctx.guild.id):''})
                    if option==1:
                        if not str(ctx.guild.id) in w:
                            w.update({str(ctx.guild.id):str(role.id)})
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Для мьюта указана роль:')} {role.mention}", color=0x4acb84)
                            embed.set_footer(text=f'ID: {role.id}')
                            await ctx.send(embed=embed, delete_after=15.0)
                        else:
                            c = ctx.guild.get_role(int(w[str(ctx.guild.id)]))
                            if c is not None:
                                embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Роль мьюта уже указана')} — {c.mention}!", color=0xcc1a1d)
                                embed.set_footer(text=f'ID: {c.id}')
                                await ctx.send(embed=embed, delete_after=10.0)
                            else:
                                del w[str(ctx.guild.id)]
                                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Прежняя роль мьюта была удалена. Пожалуйста, укажите её снова.')}", color=0xfcc21b)
                                embed.add_field(name=f"{get_language(ctx.guild.id,'Команда:')}", value=f"`{ctx.prefix}rmute add {get_language(ctx.guild.id,'@роль')}`", inline=False)
                                await ctx.send(embed=embed, ephemeral=True)
                    elif option==2:
                        if str(ctx.guild.id) in w:
                            del w[str(ctx.guild.id)]
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Роль мьюта убрана!')}", color=0xcc1a1d)
                            await ctx.send(embed=embed, delete_after=15.0)
                        else:
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,':warning: Роль мьюта не указана!')}", color=0xfcc21b)
                            await ctx.send(embed=embed, ephemeral=True)
                    else:
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,':warning: Неизвестная опция!')}", color=0xfcc21b)
                        await ctx.send(embed=embed, ephemeral=True)
                    wdata('vega', 'muterole', w)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию и роль!')}", color=0x8899a6)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Администраторы сервера могут указать 1 роль мьюта для бота.')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}rmute add {get_language(ctx.guild.id,'@роль')}", inline=False)
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_rmute(client))