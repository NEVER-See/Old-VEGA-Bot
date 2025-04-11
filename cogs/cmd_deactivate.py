import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum


class option(int, Enum):
    on = 1
    off = 2


class class_deactivate(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Деактивировать бота, все команды будут отключени и автоматические действия тоже.
    @commands.slash_command(
        name="deactivate",
        description="Deactivate the bot | Деактивировать бота",
        guild_ids=[826022179568615445],
    )
    @commands.guild_only()
    #@commands.guild_permissions(826022179568615445, users={351020816466575372: True})
    async def deactivate(
        self,
        inter,
        option: option = commands.Param(description="Select an option | Укажите опцию"),
    ):
        ctx = inter
        if ctx.author.id == 351020816466575372:
            if option is not None:
                if option:
                    if option != None:
                        try:
                            enabled = deactivatedata[0]["Option"]
                        except KeyError:
                            enabled = False
                        if option == 1:
                            if not enabled:
                                deactivate.add(0, {"Option": True})
                                # await self.client.change_presence(status=discord.Status.idle, activity=discord.Game("DEACTIVATED"))
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот деактивирован!')}",
                                    color=0xCC1A1D,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)
                                print(f"[ ИНФО ]  Бот деактивирован!\n")
                            else:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот уже деактивирован!')}",
                                    color=0xCC1A1D,
                                )
                                await ctx.send(embed=embed, delete_after=10.0)
                                ctx.command.reset_cooldown(ctx)
                        elif option == 2:
                            if enabled:
                                deactivate.add(0, {"Option": False})
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Теперь бот в рабочем состоянии!')}",
                                    color=0x43B581,
                                )
                                await ctx.send(embed=embed, delete_after=12.0)
                                print(f"[ ИНФО ]  Теперь бот в рабочем состоянии!\n")
                            else:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,':warning: Бот активен!')}",
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
                    else:
                        try:
                            enabled = deactivatedata[str("Option")]
                        except KeyError:
                            enabled = False
                        if enabled:
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Сейчас бот активен!')}",
                                color=0x43B581,
                            )
                            await ctx.send(embed=embed, delete_after=12.0)
                        else:
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Сейчас бот деактивирован!')}",
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
                    value=f"{get_language(ctx.guild.id,'Включить или отключить бота.')}",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                    value=f"`{get_language(ctx.guild.id,'on')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'off')}`",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Пример:')}",
                    value=f"{ctx.prefix}deactivate on",
                    inline=False,
                )
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author}")
                await ctx.message.reply(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                description=f"**{get_language(ctx.guild.id,'Команда только для РАЗРАБОТЧИКОВ!')}**",
                color=0xCC1A1D,
            )
            await ctx.send(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(class_deactivate(client))
