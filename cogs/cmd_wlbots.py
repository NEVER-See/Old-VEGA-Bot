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


class class_wlbots(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Скачать или посмотреть белый список ботов
    @commands.slash_command(name="wlbots", description="White list of bots | Белый список ботов")
    @commands.cooldown(1, 20, commands.BucketType.member)
    @commands.guild_only()
    async def wlbots(self, ctx):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                #try:
                wl = gdata('vega', 'wlbots')
                wlbots0 = wl[str("Bots")]
                wlbots0 = wlbots0[0: -2]
                embed = discord.Embed(description=f"🔗 [{get_language(ctx.guild.id,'Окрыть белый список ботов')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots')})", color=0x2f3136)
                with open("wlbots.txt", "w") as file:
                    file.write(f"{wlbots0}")
                with open("wlbots.txt", "rb") as file:
                    await ctx.author.send(f"**{get_language(ctx.guild.id,'📔 Белый список ботов:')}**", embed=embed, file=discord.File(file, "wlbots.txt"))
                await ctx.send(f"🎫  {(ctx.author.mention)}, {get_language(ctx.guild.id,'я отправил информацию тебе в личку.')}", ephemeral=True)
                #except:
                #    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: **Cообщение небыло доставлено!**')}\n{get_language(ctx.guild.id,'Пожалуйста, включите доступ на отправку личных сообщений.')}\n— {get_language(ctx.guild.id,'Проверьте, не заблокирован ли у вас бот?')}\n\n[<:discord:848272401913217075> support.discord.com]({get_language(ctx.guild.id,'https://support.discord.com/hc/ru/articles/217916488-Блокировка-Настройки-Конфиденциальности')})", color=0xfcc21b)
                #    embed.set_image(url=f"{get_language(ctx.guild.id,'https://media.discordapp.net/attachments/713751423128698950/859751617942519878/unknown.png')}")
                #    await ctx.message.reply(embed=embed, delete_after=25.0)
                #    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_wlbots(client))