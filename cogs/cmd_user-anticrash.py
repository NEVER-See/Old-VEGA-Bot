import disnake as discord
import json

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


class class_user_anticrash(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Автокик новых ботов текст
    @commands.slash_command(name="anticrash", description="AntiCrash function | Функция AntiCrash")
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def anticrash(
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

                with open('json/msg_appeal.json', 'r') as f:
                    ma = json.load(f)
                if str(ctx.guild.id) in ma:
                    try:
                        enabled = user_anticrashdata[ctx.guild.id]["enabled"]
                    except KeyError:
                        enabled = False
                    if option == 1:
                        if not enabled:
                            user_anticrash.add(ctx.guild.id, {"enabled": True})
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Антикраш от участников включен!')}",
                                color=0x43B581,
                            )
                            await ctx.send(embed=embed, delete_after=12.0)
                        else:
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,':warning: Антикраш уже включен!')}",
                                color=0xFCC21B,
                            )
                            await ctx.send(embed=embed, delete_after=10.0)
                            ctx.command.reset_cooldown(ctx)
                    elif option == 2:
                        if enabled:
                            user_anticrash.add(ctx.guild.id, {"enabled": False})
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Антикраш от участников выключен!')}",
                                color=0xCC1A1D,
                            )
                            await ctx.send(embed=embed, delete_after=12.0)
                        else:
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,':warning: Антикраш уже выключен!')}",
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
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Невозможно использовать команду без апелляции(сообщения)!')}",
                        color=0xCC1A1D,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Обязательно!')}",
                        value=f"{get_language(ctx.guild.id,'Используйте команду `/msg-appeal`')}",
                        inline=False,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: **Вы не являетесь Владельцем данного сервера!**')}",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_user_anticrash(client))
