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


class class_kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Кик пользователя
    @commands.slash_command(name="kick", description="Kick the user | Кикнуть пользователя")
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True, send_messages=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter, member:discord.Member = commands.Param(name="member", description="Specify the user or his ID | Укажите пользователя или его ID"), *, reason=None):
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
                    try:
                        user = ctx.author
                        if member in ctx.guild.members and member != user and member != self.client.user and user.top_role <= member.top_role:
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Невозможно кикнуть пользователя, роль которого выше или равна вашей!')}", color=0xfcc21b)
                            await ctx.send(embed=embed, ephemeral=True)
                        elif member == user:
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Невозможно кикнуть себя!')}", color=0xfcc21b)
                            await ctx.send(embed=embed, ephemeral=True)
                        elif member == self.client.user:
                            embed = discord.Embed(description=f":warning: {self.client.user.mention} {get_language(ctx.guild.id,'не может себя кикнуть!')}", color=0xfcc21b)
                            await ctx.send(embed=embed, ephemeral=True)
                        else:
                            try:                        
                                emb1 = discord.Embed(title=f"{get_language(ctx.guild.id,'<:kick:842447666990153828> Вы были изгнаны:')}", color=0xf1a019)
                                emb1.add_field(name=f"{get_language(ctx.guild.id,'С сервера:')}", value=f'{ctx.guild.name}', inline=False)
                                emb1.add_field(name=f"{get_language(ctx.guild.id,'Модератором:')}", value=f'{ctx.author}', inline=False)
                                if reason != None:
                                    emb1.add_field(name=f"{get_language(ctx.guild.id,'По причине:')}", value=reason, inline=False)
                                await member.send(embed=emb1)
                                await member.kick()
                                
                                emb = discord.Embed(title=f"{get_language(ctx.guild.id,'<:kick:842447666990153828> Кик')}", color=0xf1a019)
                                emb.add_field(name=f"{get_language(ctx.guild.id,'Модератор:')}", value=f'{ctx.author.mention}\n{ctx.author}', inline=True)
                                emb.add_field(name=f"{get_language(ctx.guild.id,'Нарушитель:')}", value=f'{member.mention}\n{member}', inline=True)
                                if reason != None:
                                    emb.add_field(name=f"{get_language(ctx.guild.id,'Причина:')}", value=reason, inline=False)
                                emb.set_thumbnail(url='https://i.postimg.cc/vZ12gJY4/kick.png')
                                await ctx.send(embed=emb)
                            except:
                                emb = discord.Embed(title=f"{get_language(ctx.guild.id,'<:kick:842447666990153828> Кик')}", color=0xf1a019)
                                emb.add_field(name=f"{get_language(ctx.guild.id,'Модератор:')}", value=f'{ctx.author.mention}\n{ctx.author}', inline=True)
                                emb.add_field(name=f"{get_language(ctx.guild.id,'Нарушитель:')}", value=f'{member.mention}\n{member}', inline=True)
                                if reason != None:
                                    emb.add_field(name=f"{get_language(ctx.guild.id,'Причина:')}", value=reason, inline=False)
                                emb.set_thumbnail(url='https://i.postimg.cc/vZ12gJY4/kick.png')
                                await member.kick()
                                await ctx.send(embed=emb)
                    except:
                        embed = discord.Embed(description=f":warning: **ERROR**\n{get_language(ctx.guild.id,'Проверьте права у бота, а так же расположение ролей!')}", color=0xfcc21b)
                        await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите пользователя и причину!')}", color=0x8899a6)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Кикните нарушителся с сервера. Причина в команде не обязательна!')}", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}kick {get_language(ctx.guild.id,'@пользователь')} {get_language(ctx.guild.id,'Пиар в лс.')}", inline=False)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_kick(client))