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


class class_unmute(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Роль размьюта
    @commands.slash_command(name="unmute", description="Unmute a user | Размьют пользователя", pass_context = True)
    @commands.guild_only()
    @commands.bot_has_permissions(manage_roles=True, send_messages=True)
    @commands.has_permissions(view_audit_log=True)
    async def unmute(self, ctx, member:discord.Member=commands.Param(description="Specify the user or his ID | Укажите пользователя или его ID")):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                mr = gdata('vega', 'muterole')
                w = gdata('vega', 'mute_users')
                user = ctx.author
                if member in ctx.guild.members and member != user and member != self.client.user and user.top_role <= member.top_role:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Невозможно размьютить пользователя, роль которого выше или равна вашей!')}", color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
                elif member == user:
                    embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Невозможно размьютить себя!')}", color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
                elif member == self.client.user:
                    embed = discord.Embed(description=f":warning: {self.client.user.mention} {get_language(ctx.guild.id,'не может себя размьютить!')}", color=0xfcc21b)
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    try:
                        muterole = ctx.guild.get_role(int(mr[str(ctx.guild.id)]))
                    except:
                        emb = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Укажите роль мьюта!')}", color=0xfcc21b)
                        emb.add_field(name=f"{get_language(ctx.guild.id,'Команда:')}", value=f"`{ctx.prefix}rmute add {get_language(ctx.guild.id,'@роль')}`", inline=True)
                        await ctx.send(embed=emb, ephemeral=True)
                    if muterole in member.roles:
                        if str(member.id) in w[str(ctx.guild.id)]:
                            w.update({str(ctx.guild.id):w[str(ctx.guild.id)].replace(str(f"{member.id} "), '')})
                            #unmuterole = discord.utils.get(ctx.guild.roles,name=muterole)
                            unmuterole = muterole
                            #emb = discord.Embed(title="<:voice:842447248264134756> Размьют", color=0x818386)
                            #emb.add_field(name='Модератор:', value=ctx.message.author.mention, inline=True)
                            #emb.add_field(name='Нарушитель:', value=member.mention, inline=True)
                            await member.remove_roles(unmuterole)
                            embed = discord.Embed(description=f'<:voice:842447248264134756> Пользователь {member.mention} размьючен!', color=0x43b581)
                            await ctx.send(embed=embed)
                    else:
                        w.update({str(ctx.guild.id):w[str(ctx.guild.id)].replace(str(f"{member.id} "), '')})
                        emb = discord.Embed(description=f":warning: Пользователь {member.mention} не замьючен!", color=0xfcc21b)
                        await ctx.send(embed=emb, ephemeral=True)
                    wdata('vega', 'mute_users', w)
            else:
                embed = discord.Embed(description=f':warning: Эта команда доступна только в определенных каналах!', color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_unmute(client))