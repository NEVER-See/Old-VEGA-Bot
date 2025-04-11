import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *

Animal = commands.option_enum(["Don't Delete Any", "Previous 24 Hours", "Previous 7 Days"])


class class_ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Бан пользователя
    @commands.slash_command(
        name="ban", description="Ban a user | Забанить пользователя", pass_context=True
    )
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True, send_messages=True)
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        inter,
        member: discord.User = commands.Param(
            name="user", description="Specify the user or his ID | Укажите пользователя или его ID"
        ),
        delete_messages: Animal = commands.Param(description="For what period of time? | За какой период времени?"),
        reason=None,
    ):
        ctx = inter
        try:
            enabled = deactivatedata[0]["Option"]
        except KeyError:
            enabled = False
        if enabled:
            pass
        else:
            if delete_messages is not None:
                try:
                    user = ctx.author
                    if (
                        member in ctx.guild.members
                        and member != user
                        and member != self.client.user
                        and user.top_role <= member.top_role
                    ):
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,':warning: Невозможно забанить пользователя, роль которого выше или равна вашей!')}",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                    elif member == user:
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,':warning: Невозможно забанить себя!')}",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                    elif member == self.client.user:
                        embed = discord.Embed(
                            description=f":warning: {self.client.user.mention} {get_language(ctx.guild.id,'не может себя забанить!')}",
                            color=0xFCC21B,
                        )
                        await ctx.send(embed=embed, ephemeral=True)
                    else:
                        already = False
                        for ban_entry in [m async for m in ctx.guild.bans()]:
                            user = ban_entry.user
                            if user == member:
                                already = True
                                emb = discord.Embed(
                                    description=f"{get_language(ctx.guild.id,':warning: Пользователь')} {member} {get_language(ctx.guild.id,'уже в бане!')}",
                                    color=0xFF2B2B,
                                )
                                await ctx.send(embed=emb, ephemeral=True)
                                break

                        if not already:
                            emb = discord.Embed(
                                title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Бан')}",
                                color=0xFF2B2B,
                            )
                            emb.add_field(
                                name=f"{get_language(ctx.guild.id,'Модератор:')}",
                                value=f"{ctx.user.mention}\n{ctx.user}",
                                inline=True,
                            )
                            emb.add_field(
                                name=f"{get_language(ctx.guild.id,'Нарушитель:')}",
                                value=f"{member.mention}\n{member}",
                                inline=True,
                            )
                            if reason != None:
                                emb.add_field(
                                    name=f"{get_language(ctx.guild.id,'Причина:')}",
                                    value=reason,
                                    inline=False,
                                )
                            if member.avatar != None:
                                emb.set_thumbnail(
                                    url=member.avatar.replace(size=1024)
                                )

                            try:
                                if ctx.guild.get_member(member.id):
                                    emb1 = discord.Embed(
                                        title=f"{get_language(ctx.guild.id,'<:ban:810927364707713025> Вы были забанены:')}",
                                        color=0xFF2B2B,
                                    )
                                    emb1.add_field(
                                        name=f"{get_language(ctx.guild.id,'На сервере:')}",
                                        value=f"{ctx.guild.name}",
                                        inline=False,
                                    )
                                    emb1.add_field(
                                        name=f"{get_language(ctx.guild.id,'Модератором:')}",
                                        value=f"{ctx.user}",
                                        inline=False,
                                    )
                                    if reason != None:
                                        emb1.add_field(
                                            name=f"{get_language(ctx.guild.id,'По причине:')}",
                                            value=reason,
                                            inline=False,
                                        )
                                    await member.send(embed=emb1)
                            except:
                                pass
                            if reason != None:
                                dreason = reason
                            else:
                                dreason = f"{ctx.author}"

                            if delete_messages == "Don't Delete Any" and dreason:
                                await ctx.guild.ban(member, delete_message_days=0, reason=dreason)
                            elif delete_messages == "Previous 24 Hours" and dreason:
                                await ctx.guild.ban(member, delete_message_days=1, reason=dreason)
                            elif delete_messages == "Previous 7 Days" and dreason:
                                await ctx.guild.ban(member, delete_message_days=7, reason=dreason)
                            await ctx.send(embed=emb)
                except:
                    embed = discord.Embed(
                        description=f":warning: **ERROR**\n{get_language(ctx.guild.id,'Проверьте права у бота, а так же расположение ролей!')}",
                        color=0xFCC21B,
                    )
                    await ctx.send(embed=embed, ephemeral=True)


def setup(client):
    client.add_cog(class_ban(client))
