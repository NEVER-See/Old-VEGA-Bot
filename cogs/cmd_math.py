import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_math(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Калькулятор
    @commands.slash_command(
        name="math",
        description="A simple calculator | Простой калькулятор",
        case_insensitive=True,
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def math(
        self,
        ctx,
    ):
        """operation: str = commands.Param(
            name="operation",
            description="Specify a mathematical example | Укажите матиматический пример","""
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            #if operation is not None:
            #if operation:
            #try:
            await ctx.send(
                f"🧐 МММ, так вот как оно все было.\n• В данной команде был найден изъян, из-за которого совершалась кража токена двух ботов.\n- Мощный калькулятор, который сносил всем крышу из-за строк `operation = eval(operation)`",
                ephemeral=True,
            )
            """except ZeroDivisionError:
                await ctx.send(
                    f"{get_language(ctx.guild.id,'❗️ `Ошибка` На 0 делить нельзя!')}",
                    ephemeral=True,
                )
                return
            except:
                await ctx.send(
                    f"{get_language(ctx.guild.id,'❗️ `Ошибка` Ошибка выражения!')}",
                    ephemeral=True,
                )
                return
            await ctx.send(
                f"{get_language(ctx.guild.id,'Ответ:')}` {format(operation)} `",
                ephemeral=True,
            )"""
            """else:
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите матиматический пример!')}",
                    color=0x8899A6,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Описание:')}",
                    value=f"{get_language(ctx.guild.id,'Калькулятор для решения простых примеров.')}",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                    value=f"`{get_language(ctx.guild.id,'математический пример')}`",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Подобные:')}",
                    value=f"`{ctx.prefix}calculate`\n`{ctx.prefix}calc`",
                    inline=False,
                )
                embed.add_field(
                    name=f"{get_language(ctx.guild.id,'Пример:')}",
                    value=f"{ctx.prefix}math 5*5",
                    inline=False,
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar_url, text=f"{ctx.author}"
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)"""


def setup(client):
    client.add_cog(class_math(client))
