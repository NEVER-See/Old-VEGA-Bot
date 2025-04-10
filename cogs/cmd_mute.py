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

prefix = "/"

class class_mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Мьют пользователя
    @commands.slash_command(name="mute", description="Mute the user | Замьютить пользователя", pass_context = True)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True, send_messages=True)
    @commands.has_permissions(view_audit_log=True)
    async def mute(self, ctx, member:discord.Member=commands.Param(name="member", description="Specify the user or his ID | Укажите пользователя или его ID"), *, reason=None):
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
                        mr = gdata('vega', 'muterole')
                        w = gdata('vega', 'mute_users')
                        if not str(ctx.guild.id) in w:
                            w.update({str(ctx.guild.id):''})

                        user = ctx.author
                        if member in ctx.guild.members and member != user and member != self.client.user and user.top_role <= member.top_role:
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Невозможно замьютить пользователя, роль которого выше или равна вашей!')}", color=0xfcc21b)
                            await ctx.send(embed=embed, ephemeral=True)
                        elif member == user:
                            embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Невозможно замьютить себя!')}", color=0xfcc21b)
                            await ctx.send(embed=embed, ephemeral=True)
                        elif member == self.client.user:
                            embed = discord.Embed(description=f":warning: {self.client.user.mention} {get_language(ctx.guild.id,'не может себя замьютить!')}", color=0xfcc21b)
                            await ctx.send(embed=embed, ephemeral=True)

                        else:
                            if str(ctx.guild.id) in mr:
                                muterole = ctx.guild.get_role(int(mr[str(ctx.guild.id)]))
                                if not muterole in member.roles:
                                    w.update({str(ctx.guild.id):w[str(ctx.guild.id)].replace(str(member.id), '').strip()})
                                if not str(member.id) in w[str(ctx.guild.id)]:
                                    w.update({str(ctx.guild.id):w[str(ctx.guild.id)].strip() + str(member.id) + ' '})
                                    emb = discord.Embed(title=f"{get_language(ctx.guild.id,'<:muted:842447248277241867> Мьют')}", color=0xfde910)
                                    emb.add_field(name=f"{get_language(ctx.guild.id,'Модератор:')}", value=ctx.author.mention, inline=True)
                                    emb.add_field(name=f"{get_language(ctx.guild.id,'Нарушитель:')}", value=member.mention, inline=True)
                                    emb.set_thumbnail(url=member.avatar.replace(size=1024))
                                    if reason != None:
                                        emb.add_field(name=f"{get_language(ctx.guild.id,'Причина:')}", value=reason, inline=False)
                                    await member.add_roles(muterole)
                                    await ctx.send(embed=emb)
                                else:
                                    emb = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Пользователь')} {member.mention} {get_language(ctx.guild.id,'уже замьючен!')}", color=0xfcc21b)
                                    await ctx.send(embed=emb, ephemeral=True)
                                wdata('vega', 'mute_users', w)
                            else:
                                emb = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Укажите роль мьюта!')}", color=0xfcc21b)
                                emb.add_field(name=f"{get_language(ctx.guild.id,'Команда:')}", value=f"`{prefix}rmute add {get_language(ctx.guild.id,'@роль')}`", inline=True)
                                await ctx.send(embed=emb, ephemeral=True)
                    except:
                        embed = discord.Embed(description=f":warning: **ERROR**\n{get_language(ctx.guild.id,'Проверьте права у бота, а так же расположение ролей!')}", color=0xfcc21b)
                        await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите пользователя!')}", color=0x8899a6)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Описание:')}", value=f"{get_language(ctx.guild.id,'Замьютьте пользователя. Причину можно не указывать.')}\n{get_language(ctx.guild.id,'Вы сами должны настроить роль мьюта!')}", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Аргумены:')}", value=f"`{get_language(ctx.guild.id,'{@пользователь}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID пользователя}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'[причина]')}`", inline=False)
                    embed.add_field(name=f"{get_language(ctx.guild.id,'Пример:')}", value=f"{prefix}mute {get_language(ctx.guild.id,'@пользователь')} {get_language(ctx.guild.id,'Спам!')}", inline=False)
                    embed.set_footer(icon_url=ctx.author.avatar, text=f'{ctx.author}')
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_mute(client))