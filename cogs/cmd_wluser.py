import disnake as discord
import json

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum

prefix = "/"

class option(int, Enum):
    add = 1
    remove = 2


class class_wluser(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Добавить all, чтобы можно было добавлять всех ботов с сервера в игнор. Необязательно!

    # Игнор ботов
    @commands.slash_command(
        name="wluser",
        description="Add a bot to the ignored list | Добавить бота в игнорируемый список",
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def wluser(
        self,
        inter,
        option: option = commands.Param(description="Select an option | Укажите опцию"),
        user: discord.User = commands.Param(
            name="user",
            description="Specify the bot or its ID | Укажите бота или его ID",
        ),
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
                with open('json/msg_appeal.json', 'r') as f:
                    ma = json.load(f)
                if str(ctx.guild.id) in ma:
                    if not user.bot:
                        if option == 1:
                            """# Временно!
                            embed = discord.Embed(
                                description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                                color=0xFCC21B,
                            )
                            await ctx.send(embed=embed, ephemeral=True)
                            ctx.command.reset_cooldown(ctx)"""
                            if user != ctx.guild.owner:
                                if ctx.guild.id in wluserdata:
                                    if "members" in wluserdata[ctx.guild.id]:
                                        if user.id not in wluserdata[ctx.guild.id]["members"]:
                                            try:
                                                wlu = wluserdata[ctx.guild.id]["members"]
                                            except KeyError:
                                                wlu = []
                                            wlu.append(user.id)
                                            embed = discord.Embed(
                                                description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Пользователь')} **{user}** {get_language(ctx.guild.id,'добавлен в белый список!')}",
                                                color=0x43B581,
                                            )
                                            embed.set_footer(text=f"ID: {user.id}")
                                            wluser.add(ctx.guild.id, {"members": wlu})
                                            await ctx.send(embed=embed, delete_after=12.0)
                                        else:
                                            embed = discord.Embed(
                                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Пользователь')} **{user}** {get_language(ctx.guild.id,'уже в белом списке!')}",
                                                color=0xCC1A1D,
                                            )
                                            embed.set_footer(text=f"ID: {user.id}")
                                            await ctx.send(embed=embed, delete_after=10.0)
                                    else:
                                        try:
                                            wlu = wluserdata[ctx.guild.id]["members"]
                                        except KeyError:
                                            wlu = []
                                        wlu.append(user.id)
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Пользователь')} **{user}** {get_language(ctx.guild.id,'добавлен в белый список!')}",
                                            color=0x43B581,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        wluser.add(ctx.guild.id, {"members": wlu})
                                        await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    try:
                                        wlu = wluserdata[ctx.guild.id]["members"]
                                    except KeyError:
                                        wlu = []
                                    wlu.append(user.id)
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Пользователь')} **{user}** {get_language(ctx.guild.id,'добавлен в белый список!')}",
                                        color=0x43B581,
                                    )
                                    embed.set_footer(text=f"ID: {user.id}")
                                    wluser.add(ctx.guild.id, {"members": wlu})
                                    await ctx.send(embed=embed, delete_after=12.0)
                            else:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,':warning: Невозможно добавить Владельца сервера в белый список!')}",
                                    color=0xFCC21B,
                                )
                                await ctx.send(embed=embed, ephemeral=True)
                                ctx.command.reset_cooldown(ctx)
                        elif option == 2:
                            """# Временно!
                            embed = discord.Embed(
                                description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                                color=0xFCC21B,
                            )
                            await ctx.send(embed=embed, ephemeral=True)
                            ctx.command.reset_cooldown(ctx)"""
                            if user != ctx.guild.owner:
                                if ctx.guild.id in wluserdata:
                                    if "members" in wluserdata[ctx.guild.id]:
                                        if user.id in wluserdata[ctx.guild.id]["members"]:
                                            wluser.delete(ctx.guild.id, {"members": user.id})
                                            newwu = wluserdata[ctx.guild.id]["members"]
                                            del newwu[user.id]
                                            wlbots.add(ctx.guild.id, {"members": newwu})

                                            embed = discord.Embed(
                                                description=f"{get_language(ctx.guild.id,':warning: Пользователь')} **{user}** {get_language(ctx.guild.id,'удален из белого списка!')}",
                                                color=0xFCC21B,
                                            )
                                            embed.set_footer(text=f"ID: {user.id}")
                                            # try:
                                            #     wlu = wluserdata[ctx.guild.id]["members"]
                                            # except KeyError:
                                            #     wlu = []
                                            if "members" not in wluserdata[ctx.guild.id]:
                                                wluser.remove(ctx.guild.id)
                                            # else:
                                            #     wluser.add(ctx.guild.id, {"members": wlu})

                                            await ctx.send(embed=embed, delete_after=12.0)
                                        else:
                                            embed = discord.Embed(
                                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Пользователь')} **{user}** {get_language(ctx.guild.id,'не найден!')}",
                                                color=0xCC1A1D,
                                            )
                                            embed.set_footer(text=f"ID: {user.id}")
                                            await ctx.send(embed=embed, delete_after=10.0)
                                    else:
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Пользователь')} **{user}** {get_language(ctx.guild.id,'не найден!')}",
                                            color=0xCC1A1D,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, delete_after=10.0)
                                else:
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Пользователь')} **{user}** {get_language(ctx.guild.id,'не найден!')}",
                                        color=0xCC1A1D,
                                    )
                                    embed.set_footer(text=f"ID: {user.id}")
                                    await ctx.send(embed=embed, delete_after=10.0)
                            else:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,':warning: Невозможно удалить Владельца сервера из белого списка!')}",
                                    color=0xFCC21B,
                                )
                                await ctx.send(embed=embed, ephemeral=True)
                                ctx.command.reset_cooldown(ctx)
                        else:
                            """# Временно!
                            embed = discord.Embed(
                                description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                                color=0xFCC21B,
                            )
                            await ctx.send(embed=embed, ephemeral=True)
                            ctx.command.reset_cooldown(ctx)"""
                            embed = discord.Embed(
                                title=f"{get_language(ctx.guild.id,':warning: Неизвестная опция!')}",
                                color=0xFCC21B,
                            )
                            await ctx.send(embed=embed, ephemeral=True)
                    else:
                        """# Временно!
                        embed = discord.Embed(
                            description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.command.reset_cooldown(ctx)"""
                        embed = discord.Embed(
                            description=f"<a:vega_x:810843492266803230> **{user.id}** {get_language(ctx.guild.id,'является ботом!')}",
                            color=0xCC1A1D,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.command.reset_cooldown(ctx)
                else:
                    """# Временно!
                    embed = discord.Embed(
                        description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.command.reset_cooldown(ctx)"""
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
    client.add_cog(class_wluser(client))