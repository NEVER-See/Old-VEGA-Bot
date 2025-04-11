import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum


class option(int, Enum):
    ru = 1
    en = 2


class class_language(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Смена языка (RU; EN)
    @commands.slash_command(
        name="language",
        description="Change the language of the bot | Сменить язык боту",
    )
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def language(
        self,
        inter,
        option: option = commands.Param(description="Select an option | Укажите опцию"),
    ):
        ctx = inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if option is not None:
                if option:
                    """# Временно!
                    embed = discord.Embed(
                        description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)"""

                    if option != None:
                        try:
                            enabled = languagedata[ctx.guild.id]["language"]
                        except KeyError:
                            enabled = False
                        if option == 1:
                            if not enabled:
                                language.add(ctx.guild.id, {"language": True})
                                embed = discord.Embed(
                                    description=f"<a:vega_check_mark:821700784927801394> Русский язык успешно установлен!",
                                    color=0x43B581,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)
                            else:
                                embed = discord.Embed(
                                    description=f":warning: Русский язык уже установлен!",
                                    color=0xFCC21B,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)
                        elif option == 2:
                            if enabled:
                                language.add(ctx.guild.id, {"language": False})
                                embed = discord.Embed(
                                    description=f"<a:vega_check_mark:821700784927801394> English language has been successfully installed!",
                                    color=0x43B581,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)
                            else:
                                embed = discord.Embed(
                                    description=f":warning: English is already installed!",
                                    color=0xFCC21B,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)
                    else:
                        try:
                            enabled = languagedata[ctx.guild.id]["language"]
                        except KeyError:
                            enabled = False
                        if enabled:
                            embed = discord.Embed(
                                description=f"<a:vega_check_mark:821700784927801394> Русский язык уже установлен!",
                                color=0x43B581,
                            )
                            await ctx.send(embed=embed, ephemeral=True)
                        else:
                            embed = discord.Embed(
                                description=f"<a:vega_check_mark:821700784927801394> English is already installed!",
                                color=0x43B581,
                            )
                            await ctx.send(embed=embed, ephemeral=True)
            else:
                try:
                    enabled = languagedata[ctx.guild.id]["language"]
                except KeyError:
                    enabled = False
                if enabled:
                    # ru
                    embed = discord.Embed(
                        description="<a:loupe:811137886141153320> Укажите язык!",
                        color=0x8899A6,
                    )
                    embed.add_field(
                        name="Описание:",
                        value=f"Установите язык для бота на вашем сервере.",
                        inline=False,
                    )
                    embed.add_field(
                        name="Аргумены:", value=f"`ru | en`", inline=False
                    )
                    embed.add_field(
                        name="Подобные:",
                        value=f"`{ctx.prefix}lang ru`",
                        inline=False,
                    )
                    embed.add_field(
                        name="Пример:",
                        value=f"{ctx.prefix}language ru",
                        inline=False,
                    )
                    embed.set_footer(
                        icon_url=ctx.author.avatar_url, text=f"{ctx.author}"
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
                else:
                    # en
                    embed = discord.Embed(
                        description="<a:loupe:811137886141153320> Specify the language!",
                        color=0x8899A6,
                    )
                    embed.add_field(
                        name="Description:",
                        value=f"Set the language for the bot on your server.",
                        inline=False,
                    )
                    embed.add_field(
                        name="Arguments:", value=f"`ru | en`", inline=False
                    )
                    embed.add_field(
                        name="Similar:",
                        value=f"`{ctx.prefix}lang en`",
                        inline=False,
                    )
                    embed.add_field(
                        name="Example:",
                        value=f"{ctx.prefix}language en",
                        inline=False,
                    )
                    embed.set_footer(
                        icon_url=ctx.author.avatar_url, text=f"{ctx.author}"
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_language(client))
