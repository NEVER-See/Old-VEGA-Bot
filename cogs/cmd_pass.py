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


class class_pass(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Добавить all, чтобы можно было добавлять всех ботов с сервера в игнор. Необязательно!

    # Игнор ботов
    @commands.slash_command(
        name="pass",
        description="Issue a pass to the bot | Выдать пропуск боту",
        pass_context=True,
    )
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def _pass_(
        self,
        ctx,
        option: option = commands.Param(description="Select an option | Укажите опцию"),
        user: discord.User = commands.Param(
            name="user",
            description="Specify the user or his ID | Укажите пользователя или его ID",
        ),
    ):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if ctx.author == ctx.guild.owner:
                try:
                    enabled = antibotdata[ctx.guild.id]["enabled"]
                except KeyError:
                    enabled = False
                if enabled:
                    if option and user:
                        if user.bot:
                            if option == 1:
                                """# Временно!
                                embed = discord.Embed(
                                    description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                                    color=0xFCC21B,
                                )
                                await ctx.send(embed=embed, ephemeral=True)
                                ctx.command.reset_cooldown(ctx)"""
                                if not ctx.guild.get_member(user.id):
                                    if ctx.guild.id in passbotsdata:
                                        if "rights" in passbotsdata[ctx.guild.id]:
                                            if user.id not in passbotsdata[ctx.guild.id]["rights"]:
                                                if user.id not in wlbotsdata[0]["Bots"]:
                                                    if "rights" in ignorebotsdata[ctx.guild.id]:
                                                        if user.id not in ignorebotsdata[ctx.guild.id]["rights"]:
                                                            try:
                                                                ps = passbotsdata[ctx.guild.id]["rights"]
                                                            except KeyError:
                                                                ps = []
                                                            ps.append(user.id)
                                                            embed = discord.Embed(
                                                                description=f"{get_language(ctx.guild.id,'Это одноразовый пропуск.')}\n{get_language(ctx.guild.id,'Как только бот зайдет на сервер, пропуск автоматически истечет.')}",
                                                                color=0xCCD6DE,
                                                            )
                                                            embed.set_author(
                                                                name=f"{get_language(ctx.guild.id, 'Пропуск выдан')} {user}",
                                                                icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                            )
                                                            if user.avatar.replace != None:
                                                                embed.set_thumbnail(
                                                                    url=user.avatar.replace(
                                                                        size=1024
                                                                    )
                                                                )
                                                            embed.set_footer(
                                                                text=f"ID: {user.id}"
                                                            )
                                                            passbots.add(ctx.guild.id, {"rights": ps})
                                                            await ctx.send(embed=embed)
                                                        else:
                                                            embed = discord.Embed(
                                                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'уже игнорируется!')}",
                                                                color=0xCC1A1D,
                                                            )
                                                            if user.avatar.replace != None:
                                                                embed.set_thumbnail(
                                                                    url=user.avatar.replace(
                                                                        size=1024
                                                                    )
                                                                )
                                                            embed.set_footer(
                                                                text=f"ID: {user.id}"
                                                            )
                                                            await ctx.send(
                                                                embed=embed, delete_after=10.0
                                                            )
                                                    else:
                                                        try:
                                                            ps = passbotsdata[ctx.guild.id]["rights"]
                                                        except KeyError:
                                                            ps = []
                                                        ps.append(user.id)
                                                        embed = discord.Embed(
                                                            description=f"{get_language(ctx.guild.id,'Это одноразовый пропуск.')}\n{get_language(ctx.guild.id,'Как только бот зайдет на сервер, пропуск автоматически истечет.')}",
                                                            color=0xCCD6DE,
                                                        )
                                                        embed.set_author(
                                                            name=f"{get_language(ctx.guild.id, 'Пропуск выдан')} {user}",
                                                            icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                        )
                                                        if user.avatar.replace != None:
                                                            embed.set_thumbnail(
                                                                url=user.avatar.replace(
                                                                    size=1024
                                                                )
                                                            )
                                                        embed.set_footer(
                                                            text=f"ID: {user.id}"
                                                        )
                                                        passbots.add(ctx.guild.id, {"rights": ps})
                                                        await ctx.send(embed=embed)
                                                else:
                                                    embed = discord.Embed(
                                                        description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})",
                                                        color=0x43B581,
                                                    )
                                                    if user.avatar.replace != None:
                                                        embed.set_thumbnail(
                                                            url=user.avatar.replace(size=1024)
                                                        )
                                                    embed.set_footer(text=f"ID: {user.id}")
                                                    await ctx.send(
                                                        embed=embed, delete_after=10.0
                                                    )
                                            else:
                                                embed = discord.Embed(
                                                    description=f"{get_language(ctx.guild.id,'У данного бота уже есть пропуск!')}\n{get_language(ctx.guild.id,'Как только бот зайдет на сервер, пропуск автоматически истечет.')}",
                                                    color=0xCC1A1D,
                                                )
                                                embed.set_author(
                                                    name=f"{get_language(ctx.guild.id, 'У')} {user} {get_language(ctx.guild.id, 'есть пропуск')}",
                                                    icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                )
                                                if user.avatar.replace != None:
                                                    embed.set_thumbnail(
                                                        url=user.avatar.replace(size=1024)
                                                    )
                                                embed.set_footer(text=f"ID: {user.id}")
                                                await ctx.send(embed=embed, ephemeral=True)
                                        else:
                                            if user.id not in wlbotsdata[0]["Bots"]:
                                                if "rights" in ignorebotsdata[ctx.guild.id]:
                                                    if user.id not in ignorebotsdata[ctx.guild.id]["rights"]:
                                                        try:
                                                            ps = passbotsdata[ctx.guild.id]["rights"]
                                                        except KeyError:
                                                            ps = []
                                                        ps.append(user.id)
                                                        embed = discord.Embed(
                                                            description=f"{get_language(ctx.guild.id,'Это одноразовый пропуск.')}\n{get_language(ctx.guild.id,'Как только бот зайдет на сервер, пропуск автоматически истечет.')}",
                                                            color=0xCCD6DE,
                                                        )
                                                        embed.set_author(
                                                            name=f"{get_language(ctx.guild.id, 'Пропуск выдан')} {user}",
                                                            icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                        )
                                                        if user.avatar.replace != None:
                                                            embed.set_thumbnail(
                                                                url=user.avatar.replace(
                                                                    size=1024
                                                                )
                                                            )
                                                        embed.set_footer(
                                                            text=f"ID: {user.id}"
                                                        )
                                                        passbots.add(ctx.guild.id, {"rights": ps})
                                                        await ctx.send(embed=embed)
                                                    else:
                                                        embed = discord.Embed(
                                                            description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'уже игнорируется!')}",
                                                            color=0xCC1A1D,
                                                        )
                                                        if user.avatar.replace != None:
                                                            embed.set_thumbnail(
                                                                url=user.avatar.replace(
                                                                    size=1024
                                                                )
                                                            )
                                                        embed.set_footer(
                                                            text=f"ID: {user.id}"
                                                        )
                                                        await ctx.send(
                                                            embed=embed, delete_after=10.0
                                                        )
                                                else:
                                                    try:
                                                        ps = passbotsdata[ctx.guild.id]["rights"]
                                                    except KeyError:
                                                        ps = []
                                                    ps.append(user.id)
                                                    embed = discord.Embed(
                                                        description=f"{get_language(ctx.guild.id,'Это одноразовый пропуск.')}\n{get_language(ctx.guild.id,'Как только бот зайдет на сервер, пропуск автоматически истечет.')}",
                                                        color=0xCCD6DE,
                                                    )
                                                    embed.set_author(
                                                        name=f"{get_language(ctx.guild.id, 'Пропуск выдан')} {user}",
                                                        icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                    )
                                                    if user.avatar.replace != None:
                                                        embed.set_thumbnail(
                                                            url=user.avatar.replace(
                                                                size=1024
                                                            )
                                                        )
                                                    embed.set_footer(
                                                        text=f"ID: {user.id}"
                                                    )
                                                    passbots.add(ctx.guild.id, {"rights": ps})
                                                    await ctx.send(embed=embed)
                                            else:
                                                embed = discord.Embed(
                                                    description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})",
                                                    color=0x43B581,
                                                )
                                                if user.avatar.replace != None:
                                                    embed.set_thumbnail(
                                                        url=user.avatar.replace(size=1024)
                                                    )
                                                embed.set_footer(text=f"ID: {user.id}")
                                                await ctx.send(
                                                    embed=embed, delete_after=10.0
                                                )
                                    else:
                                        if user.id not in wlbotsdata[0]["Bots"]:
                                            if "rights" in ignorebotsdata[ctx.guild.id]:
                                                if user.id not in ignorebotsdata[ctx.guild.id]["rights"]:
                                                    try:
                                                        ps = passbotsdata[ctx.guild.id]["rights"]
                                                    except KeyError:
                                                        ps = []
                                                    ps.append(user.id)
                                                    embed = discord.Embed(
                                                        description=f"{get_language(ctx.guild.id,'Это одноразовый пропуск.')}\n{get_language(ctx.guild.id,'Как только бот зайдет на сервер, пропуск автоматически истечет.')}",
                                                        color=0xCCD6DE,
                                                    )
                                                    embed.set_author(
                                                        name=f"{get_language(ctx.guild.id, 'Пропуск выдан')} {user}",
                                                        icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                    )
                                                    if user.avatar.replace != None:
                                                        embed.set_thumbnail(
                                                            url=user.avatar.replace(
                                                                size=1024
                                                            )
                                                        )
                                                    embed.set_footer(
                                                        text=f"ID: {user.id}"
                                                    )
                                                    passbots.add(ctx.guild.id, {"rights": ps})
                                                    await ctx.send(embed=embed)
                                                else:
                                                    embed = discord.Embed(
                                                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'уже игнорируется!')}",
                                                        color=0xCC1A1D,
                                                    )
                                                    if user.avatar.replace != None:
                                                        embed.set_thumbnail(
                                                            url=user.avatar.replace(
                                                                size=1024
                                                            )
                                                        )
                                                    embed.set_footer(
                                                        text=f"ID: {user.id}"
                                                    )
                                                    await ctx.send(
                                                        embed=embed, delete_after=10.0
                                                    )
                                            else:
                                                try:
                                                    ps = passbotsdata[ctx.guild.id]["rights"]
                                                except KeyError:
                                                    ps = []
                                                ps.append(user.id)
                                                embed = discord.Embed(
                                                    description=f"{get_language(ctx.guild.id,'Это одноразовый пропуск.')}\n{get_language(ctx.guild.id,'Как только бот зайдет на сервер, пропуск автоматически истечет.')}",
                                                    color=0xCCD6DE,
                                                )
                                                embed.set_author(
                                                    name=f"{get_language(ctx.guild.id, 'Пропуск выдан')} {user}",
                                                    icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                )
                                                if user.avatar.replace != None:
                                                    embed.set_thumbnail(
                                                        url=user.avatar.replace(
                                                            size=1024
                                                        )
                                                    )
                                                embed.set_footer(
                                                    text=f"ID: {user.id}"
                                                )
                                                passbots.add(ctx.guild.id, {"rights": ps})
                                                await ctx.send(embed=embed)
                                        else:
                                            embed = discord.Embed(
                                                description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})",
                                                color=0x43B581,
                                            )
                                            if user.avatar.replace != None:
                                                embed.set_thumbnail(
                                                    url=user.avatar.replace(size=1024)
                                                )
                                            embed.set_footer(text=f"ID: {user.id}")
                                            await ctx.send(
                                                embed=embed, delete_after=10.0
                                            )
                                else:
                                    if "rights" in passbotsdata[ctx.guild.id]:
                                        if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                            passbots.delete(ctx.guild.id, {"rights": user.id})
                                    embed = discord.Embed(
                                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Невозможно выдать пропуск, так как бот уже находиться на сервере!')}",
                                        color=0xCC1A1D,
                                    )
                                    await ctx.send(embed=embed, delete_after=10.0)

                            elif option == 2:
                                """# Временно!
                                embed = discord.Embed(
                                    description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                                    color=0xFCC21B,
                                )
                                await ctx.send(embed=embed, ephemeral=True)
                                ctx.command.reset_cooldown(ctx)"""
                                if not ctx.guild.get_member(user.id):
                                    if ctx.guild.id in passbotsdata:
                                        if "rights" in passbotsdata[ctx.guild.id]:
                                            if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                if user.id not in wlbotsdata[0]["Bots"]:
                                                    if "rights" in ignorebotsdata[ctx.guild.id]:
                                                        if user.id not in ignorebotsdata[ctx.guild.id]["rights"]:
                                                            if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                                passbots.delete(ctx.guild.id, {"rights": user.id})
                                                            embed = discord.Embed(
                                                                description=f"{get_language(ctx.guild.id,'Пропуск был изъят!')}\n{get_language(ctx.guild.id,'Теперь бот не сможет зайти на сервер!')}",
                                                                color=0xCCD6DE,
                                                            )
                                                            embed.set_author(
                                                                name=f"{get_language(ctx.guild.id, 'Пропуск изъят у')} {user}",
                                                                icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                            )
                                                            if user.avatar.replace != None:
                                                                embed.set_thumbnail(
                                                                    url=user.avatar.replace(
                                                                        size=1024
                                                                    )
                                                                )
                                                            embed.set_footer(
                                                                text=f"ID: {user.id}"
                                                            )
                                                            await ctx.send(embed=embed)
                                                        else:
                                                            embed = discord.Embed(
                                                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Бот')} **{user}** {get_language(ctx.guild.id,'уже игнорируется!')}",
                                                                color=0xCC1A1D,
                                                            )
                                                            if user.avatar.replace != None:
                                                                embed.set_thumbnail(
                                                                    url=user.avatar.replace(
                                                                        size=1024
                                                                    )
                                                                )
                                                            embed.set_footer(
                                                                text=f"ID: {user.id}"
                                                            )
                                                            await ctx.send(
                                                                embed=embed, delete_after=10.0
                                                            )
                                                    else:
                                                        if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                            passbots.delete(ctx.guild.id, {"rights": user.id})
                                                        embed = discord.Embed(
                                                            description=f"{get_language(ctx.guild.id,'Пропуск был изъят!')}\n{get_language(ctx.guild.id,'Теперь бот не сможет зайти на сервер!')}",
                                                            color=0xCCD6DE,
                                                        )
                                                        embed.set_author(
                                                            name=f"{get_language(ctx.guild.id, 'Пропуск изъят у')} {user}",
                                                            icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                        )
                                                        if user.avatar.replace != None:
                                                            embed.set_thumbnail(
                                                                url=user.avatar.replace(
                                                                    size=1024
                                                                )
                                                            )
                                                        embed.set_footer(
                                                            text=f"ID: {user.id}"
                                                        )
                                                        await ctx.send(embed=embed)
                                                else:
                                                    embed = discord.Embed(
                                                        description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Бот')} **{user}** {get_language(ctx.guild.id,'находится в белом списке!')}\n[{get_language(ctx.guild.id,'Найти бота в белом списке?')}]({get_language(ctx.guild.id,'https://never-see.gitbook.io/vega-bot/v/russian/various/whitelist-of-bots?q=')}{user.id})",
                                                        color=0x43B581,
                                                    )
                                                    if user.avatar.replace != None:
                                                        embed.set_thumbnail(
                                                            url=user.avatar.replace(size=1024)
                                                        )
                                                    embed.set_footer(text=f"ID: {user.id}")
                                                    await ctx.send(
                                                        embed=embed, delete_after=10.0
                                                    )
                                            else:
                                                if "rights" in passbotsdata[ctx.guild.id]:
                                                    if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                        passbots.delete(ctx.guild.id, {"rights": user.id})
                                                embed = discord.Embed(color=0xCC1A1D)
                                                embed.set_author(
                                                    name=f"{get_language(ctx.guild.id, 'У данного бота нет пропуска!')}",
                                                    icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                                )
                                                embed.set_footer(text=f"ID: {user.id}")
                                                await ctx.send(embed=embed, ephemeral=True)
                                        else:
                                            if "rights" in passbotsdata[ctx.guild.id]:
                                                if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                    passbots.delete(ctx.guild.id, {"rights": user.id})
                                            embed = discord.Embed(color=0xCC1A1D)
                                            embed.set_author(
                                                name=f"{get_language(ctx.guild.id, 'У данного бота нет пропуска!')}",
                                                icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                            )
                                            embed.set_footer(text=f"ID: {user.id}")
                                            await ctx.send(embed=embed, ephemeral=True)
                                    else:
                                        if "rights" in passbotsdata[ctx.guild.id]:
                                            if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                                passbots.delete(ctx.guild.id, {"rights": user.id})
                                        embed = discord.Embed(color=0xCC1A1D)
                                        embed.set_author(
                                            name=f"{get_language(ctx.guild.id, 'У данного бота нет пропуска!')}",
                                            icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                        )
                                        embed.set_footer(text=f"ID: {user.id}")
                                        await ctx.send(embed=embed, ephemeral=True)
                                else:
                                    if "rights" in passbotsdata[ctx.guild.id]:
                                        if user.id in passbotsdata[ctx.guild.id]["rights"]:
                                            passbots.delete(ctx.guild.id, {"rights": user.id})
                                    embed = discord.Embed(color=0xCC1A1D)
                                    embed.set_author(
                                        name=f"{get_language(ctx.guild.id, 'У данного бота нет пропуска!')}",
                                        icon_url="https://cdn.discordapp.com/attachments/713751423128698950/861577473997537311/ticket.png",
                                    )
                                    embed.set_footer(text=f"ID: {user.id}")
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
                                description=f"<a:vega_x:810843492266803230> **{user.id}** {get_language(ctx.guild.id,'не является ботом!')}",
                                color=0xCC1A1D,
                            )
                            await ctx.send(embed=embed, delete_after=12.0)
                    else:
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию и бота!')}",
                            color=0x8899A6,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Описание:')}",
                            value=f"{get_language(ctx.guild.id,'Выдайте или заберите пропуск у бота. Пропуск можно выдавать только тем ботам, которые не занесены в игнорируемый и белый список. Команда работает только с включенной функцией **AntiBot**!')}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                            value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{ID бота}')}`",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Пример:')}",
                            value=f"{ctx.prefix}pass add {get_language(ctx.guild.id,'ID бота')}",
                            inline=False,
                        )
                        embed.set_footer(
                            icon_url=ctx.author.avatar_url, text=f"{ctx.author}"
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.command.reset_cooldown(ctx)
                else:
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Невозможно использовать команду с выключенной функцией **AntiBot**!')}",
                        color=0xCC1A1D,
                    )
                    await ctx.send(embed=embed, delete_after=10.0)
                    ctx.command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: **Вы не являетесь Владельцем данного сервера!**')}",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_pass(client))
