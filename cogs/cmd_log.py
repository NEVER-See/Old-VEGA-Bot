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


class class_log(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Указать канал с логами
    @commands.slash_command(
        name="log", description="Set the log channel | Установить канал логов"
    )
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def log(
        self,
        ctx,
        option: option = commands.Param(description="Select an option | Укажите опцию"),
        channel: discord.TextChannel = commands.Param(
            description="Specify the channel | Укажите канал"
        ),
    ):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if option:
                if option == 2:
                    channel = False
            if option is not None and channel is not None:
                w = logchanneldata
                if option == 1:
                    """# Временно!
                    embed = discord.Embed(
                        description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.slash_command.reset_cooldown(ctx)"""
                    if ctx.guild.id not in w:
                        logchannel.add(ctx.guild.id, {"logchannel": str(channel.id)})
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Для логов указан канал:')} {channel.mention}",
                            color=0x4ACB84,
                        )
                        embed.set_footer(text=f"ID: {channel.id}")
                        await ctx.send(embed=embed, delete_after=15.0)
                    else:
                        c = self.client.get_channel(int(w[ctx.guild.id]["logchannel"]))
                        if c:
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Канал логов уже указан')} — {c.mention}!",
                                color=0xCC1A1D,
                            )
                            embed.set_footer(text=f"ID: {c.id}")
                            await ctx.send(embed=embed, delete_after=10.0)
                        else:
                            logchannel.remove(ctx.guild.id)
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Для логов указан канал:')} {channel.mention}",
                                color=0x4ACB84,
                            )
                            embed.set_footer(text=f"ID: {channel.id}")
                            await ctx.send(embed=embed, delete_after=15.0)
                elif option == 2:
                    """# Временно!
                    embed = discord.Embed(
                        description=f":warning: **{get_language(ctx.guild.id,'Команда недоступна из-за технических шоколадок!')}**",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.slash_command.reset_cooldown(ctx)"""
                    if ctx.guild.id in w:
                        logchannel.remove(ctx.guild.id)
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Канал логов удален!')}",
                            color=0xCC1A1D,
                        )
                        await ctx.send(embed=embed, delete_after=15.0)
                    else:
                        embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,':warning: Канал логов не указан!')}",
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
                    ctx.slash_command.reset_cooldown(ctx)"""
                    embed = discord.Embed(
                        title=f"{get_language(ctx.guild.id,':warning: Неизвестная опция!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    ctx.slash_command.reset_cooldown(ctx)
            else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите опцию и канал(чат)!')}",
                    color=0x8899A6,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Описание:')}",
                    value=f"{get_language(ctx.guild.id,'Вы можете указать или отключить боту канал с логами.')}",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                    value=f"`{get_language(ctx.guild.id,'{add}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{remove}')}` {get_language(ctx.guild.id,'и')} `{get_language(ctx.guild.id,'{#канал}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID канала}')}`",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Пример:')}",
                    value=f"`{ctx.prefix}log add {get_language(ctx.guild.id,'#канал')}` {get_language(ctx.guild.id,'или')} `{ctx.prefix}log remove`",
                    inline=False,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.slash_command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_log(client))
