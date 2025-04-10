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


class class_delchannels(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Уадиление спам каналов и категорий
    @commands.slash_command(name="delchannels", description="Removing spam channels and categories | Удаление спам каналов и категорий")
    @commands.bot_has_permissions(manage_messages=True, manage_channels=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def delchannels(self, inter, *, channel: str = commands.Param(name="channel", description="Write the name of the channel | Напишите название канала")):
        ctx=inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if ctx.author == ctx.guild.owner:
                if channel is not None:
                    if channel in [c.name for c in ctx.guild.channels]:
                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, идет процесс удаления каналов...')}", color=0xf4900c)
                        await ctx.send(embed=embed, ephemeral=True)

                        for i in ctx.guild.channels:
                            if i.name == f'{channel}':
                                await i.delete()
                            
                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Спам каналы')} **{channel}** {get_language(ctx.guild.id,'успешно удалены!')}", color=0x43b581)
                        await ctx.send(embed=embed, delete_after=15.0)
                    else:
                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Каналы не обнаружены!')}", color=0xcc1a1d)
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.command.reset_cooldown(ctx)
                else:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите спам канал или категорию!')}", color=0x8899a6)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Бот начнет удалять каналы и | или категории с одинаковым названием.')}", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'{название канала}')}`", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}delchannels {get_language(ctx.guild.id,'Тест')}", inline=False)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: **Вы не являетесь Владельцем данного сервера!**')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_delchannels(client))