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

# import word
# import config
# from discord import utils
from disnake.ext import commands
from random import randint
from helper import *
from cache import *


class class_user(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Информация о пользователе
    @commands.slash_command(
        name="userinfo", description="User information | Информация о пользователе"
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    @commands.bot_has_permissions(send_messages=True)
    async def user(self, ctx, *, user: disnake.Member = None):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if await checkchannel(ctx):
                w = gdata("vega", "mute_users")
                if user == None:
                    user = ctx.author

                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется обработка данных...')}",
                    color=0xF4900C,
                )
                await ctx.send(embed=embed)

                # Статусы
                statuses = {
                    disnake.Status.online: f"{get_language(ctx.guild.id,'<:online:841950162904678401>В сети')}",
                    disnake.Status.idle: f"{get_language(ctx.guild.id,'<:idle:841950163080970260>Не активен')}",
                    disnake.Status.dnd: f"{get_language(ctx.guild.id,'<:dnd:841950162862735401>Не беспокоить')}",
                    disnake.Status.offline: f"{get_language(ctx.guild.id,'<:offline:841950163147685898>Не в сети')}"
                }
                status = statuses[user.status]

                roles = [role for role in user.roles]
                req = await self.client.http.request(
                    discord.http.Route("GET", "/users/{uid}", uid=user.id)
                )
                if user.bot:
                    banner_color = 0x2F3136
                else:
                    banner_color = req["accent_color"]

                """denied = '`*~_<>|'
                denied.split()
                declined = False
                for s in user.name:
                    if s in denied:
                        declined = True
                if not declined:
                    declined=user
                else:
                    for si in denied.split():
                        declined=f"\{si}"""

                try:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'Информация о пользователе')}",
                        description="<:redline:838450844571271189><:redline:838450844571271189><:redline:838450844571271189><:redline:838450844571271189>",
                        color=banner_color
                    )
                except:
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,'Информация о пользователе')}",
                        description="<:redline:838450844571271189><:redline:838450844571271189><:redline:838450844571271189><:redline:838450844571271189>",
                        color=0x2F3136
                    )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Ник:')}",
                    value=f"<@!{user.id}>\n {user}",
                    inline=True
                )
                if len(roles) > 1:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Профиль:')}",
                        value=f"{status}",
                        inline=True
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'<:roles:842446865320378388>Ролей:')} ` {len(roles)} `",
                        value=f"**{get_language(ctx.guild.id,'Наивысшая роль:')}**\n{user.top_role.mention}",
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Профиль:')}",
                        value=f"{status}\n{get_language(ctx.guild.id,'<:roles:842446865320378388>Ролей:')} {len(roles)}",
                        inline=True
                    )

                # Профиль
                try:
                    artists_string = ""
                    # activities = 'Отсутствует'
                    if len(user.activities) != 0:
                        activities = ""
                    for activity in user.activities:
                        if isinstance(activity, disnake.Spotify):
                            if activity != None:
                                for artist in activity.artists:
                                    if activity.artists.index(
                                        artist
                                    ) != activity.artists.index(activity.artists[-1]):
                                        artists_string += f'[{artist}]({urlspotify(f"https://open.spotify.com/search/{artist}")}), '
                                    else:
                                        artists_string += f'[{artist}]({urlspotify(f"https://open.spotify.com/search/{artist}")})'
                                activities += f"{get_language(ctx.guild.id,'**Слушает:**')} <:spotify:811191409184473138> [{activity.title}]({urlspotify(f'https://open.spotify.com/search/{activity.title}')}) — ({artists_string})\n"
                        elif activity.type == disnake.ActivityType.playing:
                            if activity != None:
                                activities += f"{get_language(ctx.guild.id,'**Играет в:**')} [{activity.name}]({url_game_search(f'https://www.google.com/search?q={activity.name}')})\n"
                        elif activity.type == disnake.ActivityType.streaming:
                            if activity != None:
                                activities += f"{get_language(ctx.guild.id,'**Стримит:**')} <:streaming:842043258879737898>[{activity.name}]({activity.url})\n"
                        elif activity.type == disnake.ActivityType.watching:
                            if activity != None:
                                activities += f"{get_language(ctx.guild.id,'**Смотрит:**')} {activity.name}\n"
                        elif activity.type == disnake.ActivityType.custom:
                            if activity != None:
                                # an = activity.name.replace("https://" or "http://", " ")
                                try:
                                    if (
                                        activity.emoji in self.client.emojis
                                        or not activity.emoji.id
                                    ):
                                        if activity.name == None:
                                            activities += f"{get_language(ctx.guild.id,'**Пользовательский статус:**')} {activity.emoji}\n"
                                        else:
                                            activities += f"{get_language(ctx.guild.id,'**Пользовательский статус:**')} {activity.emoji} {activity.name}\n"
                                    else:
                                        if activity.name == None:
                                            pass
                                        else:
                                            activities += f"{get_language(ctx.guild.id,'**Пользовательский статус:**')} {activity.name}\n"
                                except:
                                    if activity.name == None:
                                        pass
                                    else:
                                        activities += f"{get_language(ctx.guild.id,'**Пользовательский статус:**')} {activity.name}\n"
                    if len(activities) > 0:
                        try:
                            if user.voice.channel:
                                embed.add_field(
                                    name=f"{get_language(ctx.guild.id,'Активность:')}",
                                    value=f"{activities}{get_language(ctx.guild.id,'**Находится в канале:**')}\n{user.voice.channel.mention}",
                                    inline=False
                                )
                        except:
                            embed.add_field(
                                name=f"{get_language(ctx.guild.id,'Активность:')}",
                                value=activities,
                                inline=False
                            )
                except:
                    try:
                        if user.voice.channel:
                            embed.add_field(
                                name=f"{get_language(ctx.guild.id,'Активность:')}",
                                value=f"{get_language(ctx.guild.id,'**Находится в канале:**')}\n{user.voice.channel.mention}",
                                inline=False
                            )
                    except:
                        pass
                """except:
                    try:
                        if user.voice.channel:
                            embed.add_field(name=f"{get_language(ctx.guild.id,'Активность:')}", value=f"{activities}{get_language(ctx.guild.id,'**Находится в канале:**')} {user.voice.channel.mention}", inline=False)
                    except:
                        pass"""

                try:
                    if str(user.id) in w[str(ctx.guild.id)]:
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,':warning: Пользователь')} {get_language(ctx.guild.id,'уже замьючен!')}",
                            value=f"ㅤ",
                            inline=False
                        )
                    else:
                        pass
                except:
                    pass

                """try:
                    oldestMessage = None
                    for channel in ctx.guild.text_channels:
                        fetchMessage = await channel.history().find(lambda m: m.author.id == user.id)
                        if fetchMessage is None:
                            continue
                        if oldestMessage is None:
                            oldestMessage = fetchMessage
                        else:
                            if fetchMessage.created_at > oldestMessage.created_at:
                                oldestMessage = fetchMessage

                    if (oldestMessage is not None) and user.voice.channel:
                        embed.add_field(name=f"{get_language(ctx.guild.id,'Активность:')}", value=f"{get_language(ctx.guild.id,'**Находится в канале:**')} {user.voice.channel.mention}\n{get_language(ctx.guild.id,'**Последнее сообщение:**')} [{get_language(ctx.guild.id,'📥 перейти к сообщению')}]({oldestMessage.jump_url})", inline=False)
                except:
                    try:
                        if user.voice.channel:
                            embed.add_field(name=f"{get_language(ctx.guild.id,'Активность:')}", value=f"{get_language(ctx.guild.id,'**Находится в канале:**')} {user.voice.channel.mention}", inline=False)
                    except:
                        oldestMessage = None
                        for channel in ctx.guild.text_channels:
                            fetchMessage = await channel.history().find(lambda m: m.author.id == user.id)
                            if fetchMessage is None:
                                continue
                            if oldestMessage is None:
                                oldestMessage = fetchMessage
                            else:
                                if fetchMessage.created_at > oldestMessage.created_at:
                                    oldestMessage = fetchMessage
                        if (oldestMessage is not None):
                            embed.add_field(name=f"{get_language(ctx.guild.id,'Активность:')}", value=f"{get_language(ctx.guild.id,'**Последнее сообщение:**')} [{get_language(ctx.guild.id,'📥 перейти к сообщению')}]({oldestMessage.jump_url})", inline=False)"""

                # embed.add_field(name='Наивысшая роль:', value=user.top_role.mention, inline=True)
                # embed.add_field(name=f"{get_language(ctx.guild.id,'Присоединился к серверу:')}", value=f"{str(user.joined_at.strftime('%d.%m.%Y, %H:%M:%S GMT'))} ({(datetime.datetime.now() - user.joined_at).days} {get_language(ctx.guild.id,'дней назад')})", inline=False)
                # embed.add_field(name=f"{get_language(ctx.guild.id,'Аккаунт создан:')}", value=f"{str(user.created_at.strftime('%d.%m.%Y, %H:%M:%S GMT'))} ({(datetime.datetime.now() - user.created_at).days} {get_language(ctx.guild.id,'дней назад')})", inline=False)
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Аккаунт:')}",
                    value=f"**{get_language(ctx.guild.id,'Присоединился:')}** <t:{int(user.joined_at.timestamp())}:D> *(<t:{int(user.joined_at.timestamp())}:R>)*\n**{get_language(ctx.guild.id,'Создан:')}** <t:{int(user.created_at.timestamp())}:D> *(<t:{int(user.created_at.timestamp())}:R>)*",
                    inline=False
                )
                if user.bot:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'<:BOT:842444823604363324> Бот?')}",
                        value=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}",
                        inline=True
                    )
                else:
                    # embed.add_field(name='<:BOT:842444823604363324> Бот?', value='<a:vega_x:810843492266803230> Нет', inline=True)
                    if user == ctx.guild.owner:
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'<:owner:860380081594564688> Владелец?')}",
                            value=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}",
                            inline=True
                        )
                    else:
                        pass
                        # embed.add_field(name=f"{get_language(ctx.guild.id,'<:owner:860380081594564688> Владелец?')}", value=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}", inline=True)
                if user.guild_permissions.administrator:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'<:admin:860380081536761886> Администратор?')}",
                        value=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Да')}",
                        inline=True
                    )
                else:
                    pass
                    # embed.add_field(name=f"{get_language(ctx.guild.id,'<:admin:860380081536761886> Администратор?')}", value=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Нет')}", inline=True)

                badges = {
                    351020816466575372: f"{get_language(ctx.guild.id,'<:vb_developer:931450178488107060> — Разработчик бота.')}",
                    750245767142441000: f"{get_language(ctx.guild.id,'<:vb_developer:931450178488107060> — Разработчик бота.')}",
                    313972726681567242: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                    426663999136858113: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                    301295716066787332: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                    722288513206321263: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                    596201949708156958: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                    838037604955193354: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}",
                    729639044757192786: f"{get_language(ctx.guild.id,'<:beta_testing:840479052669517855> — Бета-тестер.')}"
                }

                if user.id in badges:
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Дополнительная информация:')}",
                        value=badges[user.id],
                        inline=False
                    )

                embed.set_footer(text=f"ID: {user.id}")
                try:
                    embed.set_thumbnail(
                        url=user.avatar.replace(size=1024, format="gif")
                    )
                except:
                    embed.set_thumbnail(
                        url=user.avatar.replace(size=1024, format="png")
                    )

                """req = await self.client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
                banner_id = req["banner"]
                if banner_id:
                    try:
                        embed.set_image(url=f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}.gif?size=1024")
                    except:
                        embed.set_image(url=f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}.png?size=1024")"""
                try:
                    user = await self.client.fetch_user(user.id)
                    if not user.bot:
                        if user.banner:
                            embed.set_image(url=user.banner)
                        else:
                            pass
                    else:
                        pass
                except:
                    pass

                # await ctx.send('🎫  {}, информация о пользователе отправлена тебе в личку.'.format(ctx.message.author.mention), delete_after=15.0)
                await ctx.edit_original_message(embed=embed)
                # await ctx.author.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: Эта команда доступна только в определенных каналах!')}",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_user(client))
