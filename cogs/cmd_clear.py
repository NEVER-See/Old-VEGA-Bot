# -*- coding: utf-8 -*-
import disnake as discord
from disnake.channel import DMChannel
from disnake.ext import tasks
from disnake.utils import get
from datetime import datetime, timedelta
import asyncio
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


class class_clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Очищает кол-во сообщений
    @commands.slash_command(name="clear", description="Clear messages | Очитстить сообщения")
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def clear(self, inter, limit: int = commands.Param(description="Number of messages to delete | Количество собщений для удаления")):
        ctx=inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            #message = []
            #if limit:
            """def check_user(message):
                return message.author == user and message.created_at.timestamp() > time.time() - (86400*7)"""
                #lambda message: message.author == ctx.author
                #return message.author == user
                #return ctx.message

            if limit < 1:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,'❗️ Минимальное количество сообщений для очистки **1**!')}", color=0xbe1931)
                await ctx.send(embed=embed, ephemeral=True)

            elif limit <= 200:
                embed = discord.Embed(description=f"<a:b_loading:857131960223662104> {get_language(ctx.guild.id,'Пожалуйста подождите, выполняется очистка')}<a:loading:929703010781757472>", color=0xf4900c)
                await ctx.send(embed=embed, ephemeral=True)
                #try:
                embed = discord.Embed(color=0xfcc21b)
                #if user is None:
                #week_ago = datetime.utcnow() - timedelta(days=7)
                deleted = await ctx.channel.purge(limit=limit)
                embed.description = f"{get_language(ctx.guild.id,'♻️ Очищено')} **{len(deleted)}**  {get_language(ctx.guild.id,'сообщений!')}"
                await ctx.edit_original_message(embed=embed)
                """except:
                    print("7")
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'❗️ Сообщения за последнюю неделю не обнаружены!')}", color=0xbe1931)
                    await ctx.send(embed=embed, ephemeral=True)"""
                """else:
                    try:
                        #async for check in ctx.channel.history():
                        #    if len(message) == limit:
                        #        break
                        #    if check.author == user:
                        #        message.append(check)
                        #    await ctx.channel.delete_messages(message)

                        #deleted = await ctx.channel.purge(limit=limit, check=lambda message: message.author == user)
                        #    embed.description = f"{get_language(ctx.guild.id,'♻️ Очищено')} **{len(message)}**  {get_language(ctx.guild.id,'сообщений пользователя!')} {user.mention}."
                        embed.description = f":warning: {get_language(ctx.guild.id,'Разработчик заблокировал данную функцию для исправления ошибок!')}"
                    except:
                        embed.description = f":warning: {get_language(ctx.guild.id,'Возникла ошибка при очистке сообщений пользователя!')}\n— {get_language(ctx.guild.id,'Было очищено несколько сообщений!')}"
                    await ctx.send(embed=embed, ephemeral=True)"""

                    #with ctx.channel.typing():
                    #    deleted = await ctx.channel.purge(limit=limit, check=check)
                    #    embed = discord.Embed(description=f'♻️ Очищено **{len(deleted):,}**  сообщений пользователя {user.mention}.', color=0xfcc21b)
                    #    await ctx.send(embed=embed, delete_after=10.0)           
            else:
                if 200 < limit < 1e10:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'❗️ Максимальное количество сообщений для очистки **200**!')}", color=0xbe1931)
                    await ctx.send(embed=embed, ephemeral=True)
                """if user is None:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'❗️ Пользователь не найден!')}", color=0xbe1931)
                    await ctx.send(embed=embed, ephemeral=True)"""

def setup(client):
    client.add_cog(class_clear(client))