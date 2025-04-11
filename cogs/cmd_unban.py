import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Разбан пользователя
    @commands.slash_command(
        name="unban",
        description="Unban a user | Разбанить пользователя",
        pass_context=True,
    )
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True, send_messages=True)
    @commands.has_permissions(ban_members=True)
    async def unban(
        self,
        inter,
        member: discord.User = commands.Param(
            description="Specify the user or his ID | Укажите пользователя или его ID"
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
            if member:
                user = ctx.author
                if member == user:
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,':warning: **Ошибка команды**!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)

                elif member == self.client.user:
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,':warning: **Ошибка команды**!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    already = False
                    for unban_entry in [m async for m in ctx.guild.bans()]:
                        user = unban_entry.user
                        if user == member:
                            already = True
                            await ctx.guild.unban(user)
                            user = ctx.author
                            emb = discord.Embed(
                                title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Разбан')}",
                                color=0x43B581,
                            )
                            emb.add_field(
                                name=f"{get_language(ctx.guild.id,'Модератор:')}",
                                value=f"{ctx.user.mention}\n{ctx.user}",
                                inline=True,
                            )
                            emb.add_field(
                                name=f"{get_language(ctx.guild.id,'Пользователь:')}",
                                value=f"{member.mention}\n{member}",
                                inline=True,
                            )
                            if member.avatar != None:
                                emb.set_thumbnail(
                                    url=member.avatar.replace(size=1024)
                                )
                            await ctx.send(embed=emb)
                            break

                    if not already:
                        emb = discord.Embed(
                            description=f"{get_language(ctx.guild.id,':warning: Пользователь')} {member.name} {get_language(ctx.guild.id,'не забанен!')}",
                            color=0xFF2B2B,
                        )
                        await ctx.send(embed=emb, ephemeral=True)


def setup(client):
    client.add_cog(class_unban(client))
