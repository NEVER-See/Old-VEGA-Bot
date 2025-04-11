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


class class_antimsg(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Автокик новых ботов текст
    @commands.slash_command(
        name="antimsg", description="AntiMSGBot function | Функция AntiMSGBot"
    )
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def antimsg(
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
                # Временно!
                embed = discord.Embed(
                    description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)
                """
                if option is not None:
                    if option:
                        data = gdata("vega", "antimsg")
                        if option != None:
                            try:
                                enabled = data[str(ctx.guild.id)]
                            except KeyError:
                                enabled = False
                            if option == 1:
                                if not enabled:
                                    data[str(ctx.guild.id)] = True
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Автоочистка сообщений оффлайн ботов включена!')}",
                                        color=0x43B581,
                                    )
                                    await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,':warning: Автоочистка сообщений оффлайн ботов уже включена!')}",
                                        color=0xFCC21B,
                                    )
                                    await ctx.send(embed=embed, delete_after=10.0)
                                    ctx.command.reset_cooldown(ctx)
                            elif option == 2:
                                if enabled:
                                    data[str(ctx.guild.id)] = False
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Автоочистка сообщений оффлайн ботов выключена!')}",
                                        color=0xCC1A1D,
                                    )
                                    await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,':warning: Автоочистка сообщений оффлайн ботов уже выключена!')}",
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
                            wdata("vega", "antimsg", data)
                        else:
                            try:
                                enabled = data[str(ctx.guild.id)]
                            except KeyError:
                                enabled = False
                            if enabled:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Сейчас автоочистка сообщений оффлайн ботов включена!')}",
                                    color=0x43B581,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)
                            else:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Сейчас автоочистка сообщений оффлайн ботов выключена!')}",
                                    color=0xCC1A1D,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)
                else:
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию!')}",
                        color=0x8899A6,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Включите или отключите автоочистку сообщений оффлайн ботов. **AntiMSGBot**')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                        value=f"`{get_language(ctx.guild.id,'on')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'off')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Пример:')}",
                        value=f"{ctx.prefix}antimsg on",
                        inline=False,
                    )
                    embed.set_footer(
                        icon_url=ctx.author.avatar_url, text=f"{ctx.author}"
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                """
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: **Вы не являетесь Владельцем данного сервера!**')}",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_antimsg(client))
