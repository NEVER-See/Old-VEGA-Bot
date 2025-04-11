import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_rolen(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Посчитать количество участников с указанной ролью
    @commands.slash_command(
        name="rolen",
        description="Number of users with the role | Количество пользователей с ролью",
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True)
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 15, commands.BucketType.member)
    async def rolen(
        self,
        ctx,
        role: discord.Role = commands.Param(
            name="role",
            description="Specify the role or its ID | Укажите роль или её ID",
        ),
    ):
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            embed = discord.Embed(
                title=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Кол-во пользователей с ролями:')}",
                color=0x2F3136,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'Пользователей:')} ` {len(role.members)} `",
                value=f"▬▬▬▬▬▬▬▬▬▬",
                inline=False,
            )
            embed.add_field(
                name=f"{get_language(ctx.guild.id,'Роль у пользователей:')}",
                value=f"{role.mention}\n\n{get_language(ctx.guild.id,'**Название:**')} ` {role.name} `\n{get_language(ctx.guild.id,'**ID роли:**')} ` {role.id} `",
                inline=False,
            )
            embed.set_footer(
                icon_url=ctx.author.avatar.replace(size=1024), text=f"{ctx.author}"
            )
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(class_rolen(client))
