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
    channels = 1
    ignores = 2
    passings = 3
    wl = 4

class class_list(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Посмотреть лист
    @commands.slash_command(name="list", description="Lists of channels and bots | Списки каналов и ботов")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def list(self, ctx, option: option = commands.Param(description="Select an option | Укажите опцию")):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if option is not None:
                if option:

                    #Считает кол-во ботов в белом списке в файле
                    wl = gdata('vega', 'wlbots')
                    count = wl["Bots"].count(",")

                    if count:
                        print(f'[ Проверка ]  Ботов в белом списке: {count}')
                    else:
                        print('[ ОШИБКА ]  Ботов в белом списке не обнаружено!')


                    w = gdata('vega', 'channel_rights')
                    i = gdata('vega', 'ignorebots')
        #                l = gdata('vega', 'logchannel')
                    channels = []
                    ig = []
        #                log = []
                    if str(ctx.guild.id) in w:
                        for channel in w[str(ctx.guild.id)].split():
                            try:
                                c = self.client.get_channel(int(channel))
                                channels.append(c.mention)
                            except:
                                pass
                    if str(ctx.guild.id) in i:
                        for bot in i[str(ctx.guild.id)].split():
                            try:
                                b = self.client.get_user(int(bot))
                                ig.append(b.mention)
                            except:
                                pass
        #                if str(ctx.guild.id) in l:
        #                    for channel in w[str(ctx.guild.id)].split(' '):
        #                        try:
        #                            c = self.client.get_channel(int(channel))
        #                            try:
        #                                channels.append(c.mention)
        #                            except:
        #                                channels.append(c.id)
        #                        except:
        #                            pass
                    if option==1:
                        try:
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'Разрешённые каналы:')}", color=0x2f3136)
                            if len(channels) == 0:
                                embed.description = f"{get_language(ctx.guild.id,'Каналы отсутствуют')}"
                            else:
                                embed.description = ', '.join(channels) # если надо в столбик, то '\n'.join(channels)
                            await ctx.send(embed=embed)
                        except:
                            with open("ignored-channels.log", "w") as file:
                                file.write(', '.join(channels))
                            with open("ignored-channels.log", "rb") as file:
                                await ctx.send(f"{get_language(ctx.guild.id,'Разрешённые каналы:')}", file=discord.File(file, "ignored-channels.log"))
                    if option==2:
                        try:
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'Игнорируемые боты:')}", color=0x2f3136)
                            if len(ig) == 0:
                                embed.description = f"{get_language(ctx.guild.id,'Боты отсутствуют')}"
                            else:
                                embed.description = ', '.join(ig) # если надо в столбик, то '\n'.join(ig)
                            await ctx.send(embed=embed)
                        except:
                            with open("ignored-bots.log", "w") as file:
                                file.write(', '.join(ig))
                            with open("ignored-bots.log", "rb") as file:
                                await ctx.send(f"{get_language(ctx.guild.id,'Игнорируемые боты:')}", file=discord.File(file, "ignored-bots.log"))
                    elif option==3:
                        p = gdata('vega', 'passbots')
                        try:
                            pass0 = p[str(ctx.guild.id)]
                            pass0 = pass0[0: -2]
                            try:
                                if len(pass0) == 0:
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'Пропуск есть у:')}", description=f"{get_language(ctx.guild.id,'Боты отсутствуют')}", color=0x2f3136)
                                    await ctx.send(embed=embed)
                                else:
                                    embed = discord.Embed(title=f"{get_language(ctx.guild.id,'Пропуск есть у:')}", description=f"{pass0}.", color=0x2f3136)
                                    await ctx.send(embed=embed)
                            except:
                                with open("pass-bots.log", "w") as file:
                                    file.write(f"{pass0}")
                                with open("pass-bots.log", "rb") as file:
                                    await ctx.send(f"{get_language(ctx.guild.id,'Пропуск есть у:')}", file=discord.File(file, "pass-bots.log"))
                        except:
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'Пропуск есть у:')}", description=f"{get_language(ctx.guild.id,'Боты отсутствуют')}", color=0x2f3136)
                            await ctx.send(embed=embed)
                    elif option==4:
                        embed = discord.Embed(title=f"{get_language(ctx.guild.id,'🤖 Ботов в белом списке:')} `{count}`", description=f"{get_language(ctx.guild.id,'<:verified_BOT1:842449509682118676><:verified_BOT2:842449509351161915> Все боты из списка были проверены!')}\n\n\
                        [{get_language(ctx.guild.id,'🔗 Белый список ботов')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots')})", color=0x2f3136)
                        await ctx.send(embed=embed)
        #            elif option.lower() == 'logchannel':
        #                embed = discord.Embed(title='Канал с логами:', color=0x2f3136)
        #                if len(log) == 0:
        #                    embed.description = 'Канал отсутствует'
        #                else:
        #                    embed.description = ', '.join(log) # если надо в столбик, то '\n'.join(log)
        #                    await ctx.send(embed=embed)
        #            elif option.lower() in ["members", "участников"]:
        #                for guild in bot.guilds:
        #                    for member in guild.members:
        #                        await ctx.send(member)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию!')}", color=0x8899a6)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Данной командой можно посмотреть список ограниченных каналов, игнорируемых ботов, пропусков и количество ботов в белом списке.')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Аргументы:')}", value=f"`channels`; `ignores`; `pass`; `wl`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}list channels", inline=False)
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_list(client))