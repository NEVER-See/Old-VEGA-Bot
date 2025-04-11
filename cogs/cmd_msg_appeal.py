import disnake as discord
import json

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_msg_appeal(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Автокик новых ботов текст
    @commands.slash_command(name="msg-appeal", description="Allow/Prohibit server editing. | Разрешить/Запретить редактирование сервера.")
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.guild_only()
    async def msg_appeal(
        self,
        inter,
        text: str = commands.Param(
            name="text",
            description="Enter the text of the appeal (for ban) | Введите текст апелляции (на бан)",
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

                with open('json/msg_appeal.json', 'r') as f:
                    ma = json.load(f)
                if str(ctx.guild.id) in ma:
                    if len(text) <= 1024:
                        # Редактировать текст
                        ma[str(ctx.guild.id)] = ({
                            "appeal": text
                        })
                        with open('json/msg_appeal.json', 'w') as f:
                            json.dump(ma, f, indent=4)

                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,':warning: Текст был отредактирован!')}",
                            color=0xFCC21B,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Апелляция:')}",
                            value=f"{text}",
                            inline=False,
                        )
                        await ctx.send(embed=embed, delete_after=12.0)

                        embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                            color=0xFF2B2B,
                        )
                        embed.set_author(
                            name=f"{get_language(ctx.guild.id,'Пример сообщения:')}",
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'На сервере:')}",
                            value=f"{ctx.guild.name}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Модератором:')}",
                            value=f"VEGA ⦡#7724",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'По причине:')}",
                            value=f"{get_language(ctx.guild.id,'[AntiCrash] Удаление каналов!')}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Владелец сервера:')}",
                            value=f"{ctx.guild.owner}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Апелляция:')}",
                            value=f"{text}",
                            inline=False,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                    else:
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,':warning: Максимальное количество символов в тексте **1024**!')}",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                        ctx.command.reset_cooldown(ctx)
                else:
                    if len(text) <= 1024:
                        # Сохранить текст
                        ma[str(ctx.guild.id)] = ({
                            "appeal": text
                        })
                        with open('json/msg_appeal.json', 'w') as f:
                            json.dump(ma, f, indent=4)

                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Текст сохранен!')}",
                            color=0x43B581,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Апелляция:')}",
                            value=f"{text}",
                            inline=False,
                        )
                        await ctx.send(embed=embed, delete_after=12.0)

                        embed = discord.Embed(
                            title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                            color=0xFF2B2B,
                        )
                        embed.set_author(
                            name=f"{get_language(ctx.guild.id,'Пример сообщения:')}",
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'На сервере:')}",
                            value=f"{ctx.guild.name}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Модератором:')}",
                            value=f"VEGA ⦡#7724",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'По причине:')}",
                            value=f"{get_language(ctx.guild.id,'[AntiCrash] Удаление каналов!')}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Владелец сервера:')}",
                            value=f"{ctx.guild.owner}",
                            inline=False,
                        )
                        embed.add_field(
                            name=f"{get_language(ctx.guild.id,'Апелляция:')}",
                            value=f"{text}",
                            inline=False,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                    else:
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,':warning: Максимальное количество символов в тексте **1024**!')}",
                            color=0xFCC21B,
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
    client.add_cog(class_msg_appeal(client))
