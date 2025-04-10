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
from memory_profiler import memory_usage

class class_ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Пинг
    @commands.slash_command(name="ping", description="Ping bot | Пинг бота", pass_context = True)
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def ping(self, ctx):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            if ctx.author.id in config["owner_ids"]:
                latency = round(self.client.latency * 1000)
                for elem in self.client.shards:
                    print((elem, self.client.get_shard(elem).latency * 1000))

                everything_is_stable0 = "<a:everything_is_stable:821647213226491974>"
                possible_shutdown0 = "<a:possible_shutdown:821656324306763806>"
                lay_down_to_rest0 = "<a:lay_down_to_rest:821656324089577522>"

                everything_is_stable1 = "<a:everything_is_stable:821647213226491974>"
                possible_shutdown1 = "<a:possible_shutdown:821656324306763806>"
                lay_down_to_rest1 = "<a:lay_down_to_rest:821656324089577522>"

                everything_is_stable2 = "<a:everything_is_stable:821647213226491974>"
                possible_shutdown2 = "<a:possible_shutdown:821656324306763806>"
                lay_down_to_rest2 = "<a:lay_down_to_rest:821656324089577522>"

                everything_is_stable3 = "<a:everything_is_stable:821647213226491974>"
                possible_shutdown3 = "<a:possible_shutdown:821656324306763806>"
                lay_down_to_rest3 = "<a:lay_down_to_rest:821656324089577522>"

                interruption = "<:stable_ping:842449443043409970>"
                unstable_ping = "<:unstable_ping:821655777583562754>"
                stable_ping = "<:interruption:821655777881620510>"

                if round(self.client.get_shard(0).latency * 1000):
                    if 170 < round(self.client.get_shard(0).latency * 1000):
                        everything_is_stable0 = "<a:lay_down_to_rest:821656324089577522>"
                    elif 80 <= round(self.client.get_shard(0).latency * 1000):
                        everything_is_stable0 = "<a:possible_shutdown:821656324306763806>"
                if round(self.client.get_shard(1).latency * 1000):
                    if 170 < round(self.client.get_shard(1).latency * 1000):
                        everything_is_stable1 = "<a:lay_down_to_rest:821656324089577522>"
                    elif 80 <= round(self.client.get_shard(1).latency * 1000):
                        everything_is_stable1 = "<a:possible_shutdown:821656324306763806>"
                if round(self.client.get_shard(2).latency * 1000):
                    if 170 < round(self.client.get_shard(2).latency * 1000):
                        everything_is_stable2 = "<a:lay_down_to_rest:821656324089577522>"
                    elif 80 <= round(self.client.get_shard(2).latency * 1000):
                        everything_is_stable2 = "<a:possible_shutdown:821656324306763806>"
                if round(self.client.get_shard(3).latency * 1000):
                    if 170 < round(self.client.get_shard(3).latency * 1000):
                        everything_is_stable3 = "<a:lay_down_to_rest:821656324089577522>"
                    elif 80 <= round(self.client.get_shard(3).latency * 1000):
                        everything_is_stable3 = "<a:possible_shutdown:821656324306763806>"
                if latency:
                    if 170 < round(self.client.latency * 1000):
                        interruption = "<:interruption:821655777881620510>"
                    elif 80 < round(self.client.latency * 1000):
                        interruption = "<:unstable_ping:821655777583562754>"


                nchard = ctx.guild.shard_id
                rs = "<a:vega_r:810830190267072563> "
                if nchard == 0:
                    rs0 = rs
                else:
                    rs0 = "ㅤ "
                if nchard == 1:
                    rs1 = rs
                else:
                    rs1 = "ㅤ "
                if nchard == 2:
                    rs2 = rs
                else:
                    rs2 = "ㅤ "
                if nchard == 3:
                    rs3 = rs
                else:
                    rs3 = "ㅤ "


                g0 = len([g for g in self.client.guilds if g.shard_id == 0])
                g1 = len([g for g in self.client.guilds if g.shard_id == 1])
                g2 = len([g for g in self.client.guilds if g.shard_id == 2])
                g3 = len([g for g in self.client.guilds if g.shard_id == 3])


                ram = round(memory_usage()[0], 2)
                if 500 >= ram:
                    ram0 = "<:RAM_is_not_full:865485292537118780>"
                elif 2700 < ram:
                    ram0 = "<:RAM_is_almost_full:865485292429246484>"
                elif 3500 < ram:
                    ram0 = "<:RAM_is_full:865485292463063090>"


                embed = discord.Embed(title=f"<:connection_loading:903603773555998762> API {get_language(ctx.guild.id,'Соединение:')} <a:pilik1:821999858785058846><a:pilik2:821999859816202240>",
                    description=f"<:RAM_loading:903604651692290138> **{get_language(ctx.guild.id, f'ОЗУ:')} <a:pilik1:821999858785058846><a:pilik2:821999859816202240>**", color=0xf4900c)
                await ctx.message.reply(embed=embed)

                embed = discord.Embed(title=f"{interruption} API {get_language(ctx.guild.id,'Соединение:')} `{latency} {get_language(ctx.guild.id,'мс')}`",
                    description=f"{ram0} **{get_language(ctx.guild.id, f'ОЗУ:')} `{ram} MB`**", color=0x2F3136)
                embed.add_field(name=f"<:shards:903614394565525514> {get_language(ctx.guild.id,'Шардов')}:",
                    value=f"{rs0}{everything_is_stable0} {get_language(ctx.guild.id,'Шард')} **0**: `{round(self.client.get_shard(0).latency * 1000)} {get_language(ctx.guild.id,'мс')}`\
                    \n{rs1}{everything_is_stable1} {get_language(ctx.guild.id,'Шард')} **1**: `{round(self.client.get_shard(1).latency * 1000)} {get_language(ctx.guild.id,'мс')}`\
                    \n{rs2}{everything_is_stable2} {get_language(ctx.guild.id,'Шард')} **2**: `{round(self.client.get_shard(2).latency * 1000)} {get_language(ctx.guild.id,'мс')}`\
                    \n{rs3}{everything_is_stable3} {get_language(ctx.guild.id,'Шард')} **3**: `{round(self.client.get_shard(3).latency * 1000)} {get_language(ctx.guild.id,'мс')}`", inline=True)
                embed.add_field(name=f"<:servers:842447666625773568> {get_language(ctx.guild.id,'Серверов')}:",
                    value=f"{rs0}{get_language(ctx.guild.id,'Шард')} **0**: `{g0}`\
                        \n{rs1}{get_language(ctx.guild.id,'Шард')} **1**: `{g1}`\
                        \n{rs2}{get_language(ctx.guild.id,'Шард')} **2**: `{g2}`\
                        \n{rs3}{get_language(ctx.guild.id,'Шард')} **3**: `{g3}`", inline=True)
                #embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                await ctx.edit_original_message(embed=embed)
                    
        else:
            if await checkchannel(ctx):
                latency = round(self.client.latency * 1000)
                for elem in self.client.shards:
                    print((elem, self.client.get_shard(elem).latency * 1000))

                everything_is_stable0 = "<a:everything_is_stable:821647213226491974>"
                possible_shutdown0 = "<a:possible_shutdown:821656324306763806>"
                lay_down_to_rest0 = "<a:lay_down_to_rest:821656324089577522>"

                everything_is_stable1 = "<a:everything_is_stable:821647213226491974>"
                possible_shutdown1 = "<a:possible_shutdown:821656324306763806>"
                lay_down_to_rest1 = "<a:lay_down_to_rest:821656324089577522>"

                everything_is_stable2 = "<a:everything_is_stable:821647213226491974>"
                possible_shutdown2 = "<a:possible_shutdown:821656324306763806>"
                lay_down_to_rest2 = "<a:lay_down_to_rest:821656324089577522>"

                everything_is_stable3 = "<a:everything_is_stable:821647213226491974>"
                possible_shutdown3 = "<a:possible_shutdown:821656324306763806>"
                lay_down_to_rest3 = "<a:lay_down_to_rest:821656324089577522>"

                interruption = "<:stable_ping:842449443043409970>"
                unstable_ping = "<:unstable_ping:821655777583562754>"
                stable_ping = "<:interruption:821655777881620510>"

                if round(self.client.get_shard(0).latency * 1000):
                    if 170 < round(self.client.get_shard(0).latency * 1000):
                        everything_is_stable0 = "<a:lay_down_to_rest:821656324089577522>"
                    elif 80 <= round(self.client.get_shard(0).latency * 1000):
                        everything_is_stable0 = "<a:possible_shutdown:821656324306763806>"
                if round(self.client.get_shard(1).latency * 1000):
                    if 170 < round(self.client.get_shard(1).latency * 1000):
                        everything_is_stable1 = "<a:lay_down_to_rest:821656324089577522>"
                    elif 80 <= round(self.client.get_shard(1).latency * 1000):
                        everything_is_stable1 = "<a:possible_shutdown:821656324306763806>"

                if round(self.client.get_shard(2).latency * 1000):
                    if 170 < round(self.client.get_shard(2).latency * 1000):
                        everything_is_stable2 = "<a:lay_down_to_rest:821656324089577522>"
                    elif 80 <= round(self.client.get_shard(2).latency * 1000):
                        everything_is_stable2 = "<a:possible_shutdown:821656324306763806>"
                if round(self.client.get_shard(3).latency * 1000):
                    if 170 < round(self.client.get_shard(3).latency * 1000):
                        everything_is_stable3 = "<a:lay_down_to_rest:821656324089577522>"
                    elif 80 <= round(self.client.get_shard(3).latency * 1000):
                        everything_is_stable3 = "<a:possible_shutdown:821656324306763806>"
                if latency:
                    if 170 < round(self.client.latency * 1000):
                        interruption = "<:interruption:821655777881620510>"
                    elif 80 < round(self.client.latency * 1000):
                        interruption = "<:unstable_ping:821655777583562754>"


                nchard = ctx.guild.shard_id
                rs = "<a:vega_r:810830190267072563> "
                if nchard == 0:
                    rs0 = rs
                else:
                    rs0 = "ㅤ "
                if nchard == 1:
                    rs1 = rs
                else:
                    rs1 = "ㅤ "
                if nchard == 2:
                    rs2 = rs
                else:
                    rs2 = "ㅤ "
                if nchard == 3:
                    rs3 = rs
                else:
                    rs3 = "ㅤ "


                g0 = len([g for g in self.client.guilds if g.shard_id == 0])
                g1 = len([g for g in self.client.guilds if g.shard_id == 1])
                g2 = len([g for g in self.client.guilds if g.shard_id == 2])
                g3 = len([g for g in self.client.guilds if g.shard_id == 3])


                ram = round(memory_usage()[0], 2)
                if 500 >= ram:
                    ram0 = "<:RAM_is_not_full:865485292537118780>"
                elif 2700 < ram:
                    ram0 = "<:RAM_is_almost_full:865485292429246484>"
                elif 3500 < ram:
                    ram0 = "<:RAM_is_full:865485292463063090>"


                embed = discord.Embed(title=f"<:connection_loading:903603773555998762> API {get_language(ctx.guild.id,'Соединение:')} <a:pilik1:821999858785058846><a:pilik2:821999859816202240>",
                    description=f"<:RAM_loading:903604651692290138> **{get_language(ctx.guild.id, f'ОЗУ:')} <a:pilik1:821999858785058846><a:pilik2:821999859816202240>**", color=0xf4900c)
                await ctx.send(embed=embed)

                embed = discord.Embed(title=f"{interruption} API {get_language(ctx.guild.id,'Соединение:')} `{latency} {get_language(ctx.guild.id,'мс')}`",
                    description=f"{ram0} **{get_language(ctx.guild.id, f'ОЗУ:')} `{ram} MB`**", color=0x2F3136)
                embed.add_field(name=f"<:shards:903614394565525514> {get_language(ctx.guild.id,'Шардов')}:",
                    value=f"{rs0}{everything_is_stable0} {get_language(ctx.guild.id,'Шард')} **0**: `{round(self.client.get_shard(0).latency * 1000)} {get_language(ctx.guild.id,'мс')}`\
                    \n{rs1}{everything_is_stable1} {get_language(ctx.guild.id,'Шард')} **1**: `{round(self.client.get_shard(1).latency * 1000)} {get_language(ctx.guild.id,'мс')}`\
                    \n{rs2}{everything_is_stable2} {get_language(ctx.guild.id,'Шард')} **2**: `{round(self.client.get_shard(2).latency * 1000)} {get_language(ctx.guild.id,'мс')}`\
                    \n{rs3}{everything_is_stable3} {get_language(ctx.guild.id,'Шард')} **3**: `{round(self.client.get_shard(3).latency * 1000)} {get_language(ctx.guild.id,'мс')}`", inline=True)
                embed.add_field(name=f"<:servers:842447666625773568> {get_language(ctx.guild.id,'Серверов')}:",
                    value=f"{rs0}{get_language(ctx.guild.id,'Шард')} **0**: `{g0}`\
                        \n{rs1}{get_language(ctx.guild.id,'Шард')} **1**: `{g1}`\
                        \n{rs2}{get_language(ctx.guild.id,'Шард')} **2**: `{g2}`\
                        \n{rs3}{get_language(ctx.guild.id,'Шард')} **3**: `{g3}`", inline=True)
                #embed.set_footer(icon_url=ctx.author.avatar_url, text=f'{ctx.author}')
                await ctx.edit_original_message(embed=embed)
            else:
                embed = discord.Embed(description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}", color=0xfcc21b)
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)

def setup(client):
    client.add_cog(class_ping(client))