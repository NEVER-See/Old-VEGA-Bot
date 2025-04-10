# -*- coding: utf-8 -*-
import disnake as discord
import disnake
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
from urllib.parse import quote_plus


class links(disnake.ui.View):
    def __init__(self, ctx):
        super().__init__()

        url = f"{get_language(ctx.guild.id,'https://discord.com/invite/8YhmtsYvpK')}"
        self.add_item(disnake.ui.Button(label=f"{get_language(ctx.guild.id,'🔗 Сервер поддержки')}", url=url))

        url1 = f"{get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/')}"
        self.add_item(disnake.ui.Button(label=f"{get_language(ctx.guild.id,'📚 Документация')}", url=url1))

        url2 = "https://vegabot.xyz/vegabot"
        self.add_item(disnake.ui.Button(label=f"{get_language(ctx.guild.id,'🌐 Сайт')}", url=url2))


class class_links(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Ссылки
    @commands.slash_command(name="links", description="Useful links | Полезные ссылки")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def links(self, ctx):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                try:
                    await ctx.author.send(f"{get_language(ctx.guild.id,'Полезные ссылки:')}", view=links(ctx))
                    await ctx.send(f"🎫  {ctx.author.mention}, {get_language(ctx.guild.id,'я отправил информацию тебе в личку.')}", ephemeral=True)

                except:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: **Cообщение небыло доставлено!**')}\n{get_language(ctx.guild.id,'Пожалуйста, включите доступ на отправку личных сообщений.')}\n— {get_language(ctx.guild.id,'Проверьте, не заблокирован ли у вас бот?')}\n\n[support.discord.com]({get_language(ctx.guild.id,'https://support.discord.com/hc/ru/articles/217916488-Блокировка-Настройки-Конфиденциальности')})", color=0xfcc21b)
                    embed.set_image(url=f"{get_language(ctx.guild.id,'https://media.discordapp.net/attachments/713751423128698950/859751617942519878/unknown.png')}")
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_links(client))