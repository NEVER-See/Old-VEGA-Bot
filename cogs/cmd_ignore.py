import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum


class option(int, Enum):
    add = 1
    remove = 2


class class_ignore(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Добавить all, чтобы можно было добавлять всех ботов с сервера в игнор. Необязательно!

    # Игнор ботов
    @commands.slash_command(
        name="ignore",
        description="Add a bot to the ignored list | Добавить бота в игнорируемый список",
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def ignore(
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
                """# Временно!
                embed = discord.Embed(
                    description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)"""

                if option and user:
                    if user.bot:
                        if option == 1:
                            if ctx.guild.id in ignorebotsdata:
                                if "rights" not in ignorebotsdata[ctx.guild.id]:
                                    if user.id in wlbotsdata[0]["Bots"]:
                                        if ctx.guild.id in passbotsdata:
                                            if "rights" in passbotsdata[ctx.guild.id]:
                                                if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                    passbots.delete(ctx.guild.id, {"rights": user.id})
                                        if ctx.guild.id in ignorebotsdata:
                                            if "rights" in ignorebotsdata[ctx.guild.id]:
                                                if user.id in ignorebotsdata[ctx.guild.id]["rights"]:
                                                    ignorebots.delete(ctx.guild.id, {"rights": user.id})
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})",
                                            color=0x43B581,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, delete_after=12.0)
                                    else:
                                        if ctx.guild.id in passbotsdata:
                                            if "rights" in passbotsdata[ctx.guild.id]:
                                                if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                    passbots.delete(ctx.guild.id, {"rights": user.id})
                                        try:
                                            ig = ignorebotsdata[ctx.guild.id]["rights"]
                                        except KeyError:
                                            ig = []
                                        ig.append(user.id)
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Теперь действия бота')} **{user}** {get_language(ctx.guild.id,'игнорируются!')}",
                                            color=0x43B581,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        ignorebots.add(ctx.guild.id, {"rights": ig})
                                        await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    if user.id in wlbotsdata[0]["Bots"]:
                                        if ctx.guild.id in passbotsdata:
                                            if "rights" in passbotsdata[ctx.guild.id]:
                                                if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                    passbots.delete(ctx.guild.id, {"rights": user.id})
                                        if ctx.guild.id in ignorebotsdata:
                                            if "rights" in ignorebotsdata[ctx.guild.id]:
                                                if user.id in ignorebotsdata[ctx.guild.id]["rights"]:
                                                    ignorebots.delete(ctx.guild.id, {"rights": user.id})
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})",
                                            color=0x43B581,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, delete_after=12.0)
                                    elif user.id not in ignorebotsdata[ctx.guild.id]["rights"]:
                                        if ctx.guild.id in passbotsdata:
                                            if "rights" in passbotsdata[ctx.guild.id]:
                                                if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                    passbots.delete(ctx.guild.id, {"rights": user.id})
                                        try:
                                            igb = ignorebotsdata[ctx.guild.id]["rights"]
                                        except KeyError:
                                            igb = []
                                        igb.append(user.id)
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Теперь действия бота')} **{user}** {get_language(ctx.guild.id,'игнорируются!')}",
                                            color=0x43B581,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        ignorebots.add(ctx.guild.id, {"rights": igb})
                                        await ctx.send(embed=embed, delete_after=12.0)
                                    else:
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'уже игнорируется!')}",
                                            color=0xCC1A1D,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, delete_after=10.0)
                            else:
                                if user.id in wlbotsdata[0]["Bots"]:
                                    if ctx.guild.id in passbotsdata:
                                        if "rights" in passbotsdata[ctx.guild.id]:
                                            if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                passbots.delete(ctx.guild.id, {"rights": user.id})
                                    if ctx.guild.id in ignorebotsdata:
                                        if "rights" in ignorebotsdata[ctx.guild.id]:
                                            if user.id in ignorebotsdata[ctx.guild.id]["rights"]:
                                                ignorebots.delete(ctx.guild.id, {"rights": user.id})
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})",
                                        color=0x43B581,
                                    )
                                    embed.set_footer(text=f"ID: {user.id}")
                                    await ctx.send(embed=embed, delete_after=12.0)
                                else:
                                    if ctx.guild.id in passbotsdata:
                                        if "rights" in passbotsdata[ctx.guild.id]:
                                            if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                passbots.delete(ctx.guild.id, {"rights": user.id})
                                    try:
                                        igb = ignorebotsdata[ctx.guild.id]["rights"]
                                    except KeyError:
                                        igb = []
                                    igb.append(user.id)
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Теперь действия бота')} **{user}** {get_language(ctx.guild.id,'игнорируются!')}",
                                        color=0x43B581,
                                    )
                                    embed.set_footer(text=f"ID: {user.id}")
                                    ignorebots.add(ctx.guild.id, {"rights": igb})
                                    await ctx.send(embed=embed, delete_after=12.0)

                        elif option == 2:
                            if ctx.guild.id in ignorebotsdata:
                                if "rights" not in ignorebotsdata[ctx.guild.id]:
                                    if user.id in wlbotsdata[0]["Bots"]:
                                        if ctx.guild.id in passbotsdata:
                                            if "rights" in passbotsdata[ctx.guild.id]:
                                                if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                    passbots.delete(ctx.guild.id, {"rights": user.id})
                                        if ctx.guild.id in ignorebotsdata:
                                            if "rights" in ignorebotsdata[ctx.guild.id]:
                                                if user.id in ignorebotsdata[ctx.guild.id]["rights"]:
                                                    ignorebots.delete(ctx.guild.id, {"rights": user.id})
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})",
                                            color=0x43B581,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, delete_after=12.0)
                                    else:
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'не найден!')}",
                                            color=0xCC1A1D,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, delete_after=10.0)
                                else:
                                    if user.id in wlbotsdata[0]["Bots"]:
                                        if ctx.guild.id in passbotsdata:
                                            if "rights" in passbotsdata[ctx.guild.id]:
                                                if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                    passbots.delete(ctx.guild.id, {"rights": user.id})
                                        if ctx.guild.id in ignorebotsdata:
                                            if "rights" in ignorebotsdata[ctx.guild.id]:
                                                if user.id in ignorebotsdata[ctx.guild.id]["rights"]:
                                                    ignorebots.delete(ctx.guild.id, {"rights": user.id})
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})",
                                            color=0x43B581,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, delete_after=12.0)
                                    elif user.id in ignorebotsdata[ctx.guild.id]["rights"]:
                                        if ctx.guild.id in passbotsdata:
                                            if "rights" in passbotsdata[ctx.guild.id]:
                                                if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                    passbots.delete(ctx.guild.id, {"rights": user.id})
                                        if ctx.guild.id in ignorebotsdata:
                                            if "rights" in ignorebotsdata[ctx.guild.id]:
                                                if user.id in ignorebotsdata[ctx.guild.id]["rights"]:
                                                    ignorebots.delete(ctx.guild.id, {"rights": user.id})
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,':warning: Теперь действия бота')} **{user}** {get_language(ctx.guild.id,'не игнорируются!')}",
                                            color=0xFCC21B,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, delete_after=12.0)
                                    else:
                                        embed = discord.Embed(
                                            description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'не найден!')}",
                                            color=0xCC1A1D,
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, delete_after=10.0)
                            else:
                                embed = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'не найден!')}",
                                    color=0xCC1A1D,
                                )
                                embed.set_footer(text=f"ID: {user.id}")
                                await ctx.send(embed=embed, delete_after=10.0)
                        else:
                            embed = discord.Embed(
                                title=f"{get_language(ctx.guild.id,':warning: Неизвестная опция!')}",
                                color=0xFCC21B,
                            )
                            await ctx.send(embed=embed, ephemeral=True)
                    else:
                        embed = discord.Embed(
                            description=f"<a:vega_x:810843492266803230> **{user.id}** {get_language(ctx.guild.id,'не является ботом!')}",
                            color=0xCC1A1D,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.command.reset_cooldown(ctx)
                else:
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию и бота!')}",
                        color=0x8899A6,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Бот (не) будет игнорировать действия указанного бота. Действует на ботов, которые не находятся в белом списке!')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                        value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{ID бота}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Пример:')}",
                        value=f"{ctx.prefix}ignore add {get_language(ctx.guild.id,'ID бота')}",
                        inline=False,
                    )
                    embed.set_footer(
                        icon_url=ctx.author.avatar_url, text=f"{ctx.author}"
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
    client.add_cog(class_ignore(client))
