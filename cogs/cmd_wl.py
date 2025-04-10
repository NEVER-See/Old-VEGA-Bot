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

class class_wl(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Занести или удалить бота из белого списка
    @commands.slash_command(name="wl", description="Whitelist management | Управление белым списком", default_permission=False)
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.guild_only()
    @commands.guild_permissions(826022179568615445, users={351020816466575372: True})
    async def wl(self, ctx, option: option = commands.Param(description="Select an option | Укажите опцию"), user:discord.User=commands.Param(description="Specify the user or his ID | Укажите пользователя или его ID"), link: str = commands.Param(name="link", description="Specify the link | Укажите ссылку") == None):
        if ctx.author.id == 351020816466575372:
            if user.bot:
                w = gdata('vega', 'wlbots')
                if not str("Bots") in w:
                    w.update({str("Bots"):''})
                if option==1:
                    if str(user.id) in w[str("Bots")]:
                        embed = discord.Embed(description=f'<a:vega_x:810843492266803230> Бот **{user}** уже есть в списке!', color=0xcc1a1d)
                        await ctx.send(embed=embed, delete_after=10.0)
                    else:
                        w.update({str("Bots"):w[str("Bots")] + str(user.id) + ', '})
                        embed = discord.Embed(description=f'<a:vega_check_mark:821700784927801394> Бот **{user}** занесен в белый список!', color=0x43b581)
                        await ctx.send(embed=embed, delete_after=12.0)

                        embed = discord.Embed(title="<a:vega_check_mark:821700784927801394> Whitelisted:", description=f'[{user}]({link}) <:EN_verified_BOT1:842450142060871721><:EN_verified_BOT2:842450142271635486>\n\n`ID: {user.id}`', color=0x43b581)
                        embed.set_thumbnail(url=user.avatar.replace(size=1024))
                        await self.client.get_channel(837623697888116767).send(embed=embed)

                        
                        if link:
                            reason = f"\n {link}"
                        else:
                            reason = ""

                        server = self.client.get_guild(909463311937056788)
                        await server.ban(user, reason=f"В белом списке!{reason}")
                        
                        emb = discord.Embed(title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Бан')}", color=0xff2b2b)
                        emb.add_field(name=f"{get_language(ctx.guild.id,'Модератор:')}", value=f'{ctx.author.mention}\n{ctx.author}', inline=True)
                        emb.add_field(name=f"{get_language(ctx.guild.id,'Нарушитель:')}", value=f'{user.mention}\n{user}', inline=True)
                        if reason != None:
                            emb.add_field(name=f"{get_language(ctx.guild.id,'Причина:')}", value=f"В белом списке!{reason}", inline=False)
                        emb.set_thumbnail(url='https://cdn.discordapp.com/attachments/713751423128698950/810933957197037588/ban.png')
                        await self.client.get_channel(911205950176772137).send(embed=emb)

                elif option==2:
                    if str(user.id) in w[str("Bots")]:
                        w.update({str("Bots"):w[str("Bots")].replace(str(f"{user.id}, "), '')})
                        #requests.get({str(user.id), ''})
                        embed = discord.Embed(description=f':warning: Бот **{user}** удален из белого списка!', color=0xfcc21b)
                        await ctx.send(embed=embed, delete_after=12.0)

                        embed = discord.Embed(title="<a:vega_x:810843492266803230> Removed from the white list:", description=f'{user} <:EN_verified_BOT1:842450142060871721><:EN_verified_BOT2:842450142271635486>\n\n`ID: {user.id}`', color=0xcc1a1d)
                        embed.set_thumbnail(url=user.avatar.replace(size=1024))
                        await self.client.get_channel(837623697888116767).send(embed=embed)

                        server = self.client.get_guild(909463311937056788)
                        await server.unban(user)
                        emb = discord.Embed(title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Разбан')}", color=0x43b581)
                        emb.add_field(name=f"{get_language(ctx.guild.id,'Модератор:')}", value=f'{ctx.author.mention}\n{ctx.author}', inline=True)
                        emb.add_field(name=f"{get_language(ctx.guild.id,'Пользователь:')}", value=f'{user.mention}\n{user}', inline=True)
                        await self.client.get_channel(911205950176772137).send(embed=emb)
                    else:
                        embed = discord.Embed(description=f'<a:vega_x:810843492266803230> Бот **{user}** не найден!', color=0xcc1a1d)
                        await ctx.send(embed=embed, delete_after=10.0)
                else:
                    embed = discord.Embed(title=f':warning: Неизвестная опция!', color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
                wdata('vega', 'wlbots', w)
            else:
                pass
        else:
            pass

def setup(client):
    client.add_cog(class_wl(client))