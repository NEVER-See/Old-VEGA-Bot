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


class class_echo(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Написать от лица бота
    @commands.slash_command(name="echo", description="Message from the bot's side | Сообщение от лица бота")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(administrator=True)
    async def echo(self, inter, *, msg: str = commands.Param(name="msg", description="Enter the text | Введите текст")):
        ctx=inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if msg is not None:
                if msg:
                    await ctx.send(msg)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите текст!')}", color=0x8899a6)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Отправляейте сообщения от лица бота.')}", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'{текст}')}`", inline=False)
                embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}echo {get_language(ctx.guild.id,'Макароны! Нет, пельмени!')}", inline=False)
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                await ctx.send(embed=embed, delete_after=15.0)
                ctx.command.reset_cooldown(ctx)

    #Написать от лица бота в определнный канал
    #@self.client.command(name='advecho')
    #@commands.cooldown(1, 5, commands.BucketType.member)
    #@commands.bot_has_permissions(send_messages=True)
    #@commands.has_permissions(administrator=True)
    #async def advecho(ctx, channel: discord.TextChannel, *, message):
    #    await channel.send(f'{message}')
    #    await ctx.message.delete()

def setup(client):
    client.add_cog(class_echo(client))