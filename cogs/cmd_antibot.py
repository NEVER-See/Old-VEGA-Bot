import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum


class Animal(int, Enum):
    on = 1
    off = 2


class class_antibot(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Автокик новых ботов текст
    @commands.slash_command(description="AntiBot function | Функция AntiBot")
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def antibot(
        self,
        inter,
        option: Animal = commands.Param(description="Select an option | Укажите опцию"),
    ):
        ctx = inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if ctx.author == ctx.guild.owner:
                """# Временно!
                embed = discord.Embed(
                    description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)"""

                if option is not None:
                    if option:
                        try:
                            enabled = antibotdata[ctx.guild.id]["enabled"]
                        except KeyError:
                            enabled = False
                        if option != None:
                            if option == 1:
                                if not enabled:
                                    antibot.add(ctx.guild.id, {"enabled": True})
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Автобан новых ботов включен!')}",
                                        color=0x43B581,
                                    )
                                    await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,':warning: Автобан новых ботов уже включен!')}",
                                        color=0xFCC21B,
                                    )
                                    await ctx.send(embed=embed, delete_after=10.0)
                                    ctx.command.reset_cooldown(ctx)
                            elif option == 2:
                                if enabled:
                                    antibot.add(ctx.guild.id, {"enabled": False})
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Автобан новых ботов выключен!')}",
                                        color=0xCC1A1D,
                                    )
                                    await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,':warning: Автобан новых ботов уже выключен!')}",
                                        color=0xFCC21B,
                                    )
                                    await ctx.send(embed=embed, delete_after=10.0)
                                    ctx.command.reset_cooldown(ctx)
                            else:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,':warning: Неизвестная опция!')}",
                                    color=0xFCC21B,
                                )
                                await ctx.send(embed=embed, delete_after=8.0)
                                ctx.command.reset_cooldown(ctx)
                        """else:
                            try:
                                enabled = data[str(ctx.guild.id)]
                            except KeyError:
                                enabled = False
                            if enabled:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Сейчас автобан новых ботов включен!')}",
                                    color=0x43B581,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)
                            else:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Сейчас автобан новых ботов выключен!')}",
                                    color=0xCC1A1D,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)"""
                else:
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию!')}",
                        color=0x8899A6,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Включите или отключите защиту от ботов. **AntiBot**')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                        value=f"`{get_language(ctx.guild.id,'on')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'off')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Пример:')}",
                        value=f"{ctx.prefix}antibot on",
                        inline=False,
                    )
                    embed.set_footer(
                        icon_url=ctx.author.avatar_url, text=f"{ctx.author}"
                    )
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: **Вы не являетесь Владельцем данного сервера!**')}",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_antibot(client))
