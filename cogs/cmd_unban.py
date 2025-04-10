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


class class_unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Разбан пользователя
    @commands.slash_command(name="unban", description="Unban a user | Разабанить пользователя", pass_context = True)
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True, send_messages=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, inter, member: discord.User=commands.Param(description="Specify the user or his ID | Укажите пользователя или его ID")):
        ctx=inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                if member:
                    user = ctx.author
                    if member == user:
                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: **Ошибка команды**!')}", color=0xfcc21b)
                        await ctx.send(embed=embed, ephemeral=True)

                    elif member == self.client.user:
                        embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: **Ошибка команды**!')}", color=0xfcc21b)
                        await ctx.send(embed=embed, ephemeral=True)
                    else:
                        banned_users = await ctx.guild.bans()
                        already = False
                        for unban_entry in banned_users:
                            user = unban_entry.user
                            if user == member:
                                already = True
                                await ctx.guild.unban(user)
                                user = ctx.author
                                emb = discord.Embed(title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Разбан')}", color=0x43b581)
                                emb.add_field(name=f"{get_language(ctx.guild.id,'Модератор:')}", value=f'{ctx.user.mention}\n{ctx.user}', inline=True)
                                emb.add_field(name=f"{get_language(ctx.guild.id,'Пользователь:')}", value=f'{member.mention}\n{member}', inline=True)
                                await ctx.send(embed=emb)
                                break

                        if not already:
                            emb = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Пользователь')} {member.name} {get_language(ctx.guild.id,'не забанен!')}", color=0xff2b2b)
                            await ctx.send(embed=emb, ephemeral=True)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_unban(client))