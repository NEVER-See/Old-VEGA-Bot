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


class class_emoji(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Эмодзи
    @commands.slash_command(name="emoji", description="View emoji | Посмотреть эмодзи")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def emoji(self, inter, see: str = commands.Param(name="emoji", description="Specify the server emoji | Укажите серверный эмодзи")):
        ctx=inter
        emoji=see
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                if emoji is not None:
                    if emoji:
                        em = get(ctx.guild.emojis, name=convert_em(emoji))
                        if em is not None:
                            """try:
                                row1 = ActionRow(Button(style=ButtonStyle.red, emoji=f"<a:{em.name}:{em.id}>"), Button(style=ButtonStyle.green, emoji=f"<a:{em.name}:{em.id}>"))
                                row2 = ActionRow(Button(style=ButtonStyle.blurple, emoji=f"<a:{em.name}:{em.id}>"), Button(style=ButtonStyle.grey, emoji=f"<a:{em.name}:{em.id}>"))
                                #row4 = ActionRow(Button(style=ButtonStyle.link, emoji=f"<a:{em.name}:{em.id}>", url=em.url))
                            except:
                                row1 = ActionRow(Button(style=ButtonStyle.red, emoji=f"<:{em.name}:{em.id}>"), Button(style=ButtonStyle.green, emoji=f"<:{em.name}:{em.id}>"))
                                row2 = ActionRow(Button(style=ButtonStyle.blurple, emoji=f"<:{em.name}:{em.id}>"), Button(style=ButtonStyle.grey, emoji=f"<:{em.name}:{em.id}>"))
                                #row4 = ActionRow(Button(style=ButtonStyle.link, emoji=f"<:{em.name}:{em.id}>", url=em.url))"""
                            embed = discord.Embed(title=f"{get_language(ctx.guild.id,'Эмодзи:')} {em}", color=0x2f3136)
                            embed.set_image(url=em.url)
                            embed.set_footer(text=f'ID: {em.id}')
                            await ctx.send(embed=embed)
                            #msg = await ctx.message.reply(embed=embed, components=[row1, row2])
                            #await msg.add_reaction(em)
                #            await ctx.message.delete()

                        else:
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Неизвестное эмодзи!')}", color=0xfcc21b)
                            await ctx.send(embed=embed, ephemeral=True)
                            ctx.command.reset_cooldown(ctx)
                else:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите эмодзи!')}", color=0x8899a6)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Можно указывать только те эмодзи, которые загружены на сервер.')}", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'{эмодзи}')}`", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{ctx.prefix}emoji <:python:826158844555427891>", inline=False)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_emoji(client))