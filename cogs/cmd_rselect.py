import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *
from enum import Enum


class option(int, Enum):
    all = 1


class class_rselect(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Забрать у всех пользователей 1 роль
    @commands.slash_command(
        name="rselect",
        description="Take the role from all users | Забрать роль у всех пользователей",
        case_insensitive=True,
    )
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True, manage_roles=True)
    @commands.cooldown(1, 300, commands.BucketType.guild)
    async def rselect(
        self,
        ctx,
        option: option = commands.Param(description="Select an option | Укажите опцию"),
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
            if ctx.author == ctx.guild.owner:
                if option == 1 and role:
                    user = ctx.author
                    getrole = discord.utils.get(ctx.guild.roles, id=role.id)
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, выполняется изъятие роли у пользователей...')}",
                        color=0xF4900C,
                    )
                    await ctx.send(embed=embed)
                    try:
                        for member in ctx.guild.members:
                            if not member.bot:
                                await member.remove_roles(getrole)
                        if member:
                            embed = discord.Embed(
                                description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Я забрал у всех роль')} {role.mention}",
                                color=0x43B581,
                            )
                            try:
                                await ctx.edit_original_message(embed=embed)
                            except:
                                pass
                    except:
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Я не смог изъять у всех роль')} {role.mention}.\n— {get_language(ctx.guild.id,'Видимо моя роль находится ниже роли')} {role.mention}.",
                            color=0xCC1A1D,
                        )
                        try:
                            await ctx.edit_original_message(embed=embed)
                        except:
                            pass
                        ctx.command.reset_cooldown(ctx)
            else:
                msg = ctx.message
                await msg.add_reaction(":warning:")
                embed = discord.Embed(
                    description=f"{get_language(ctx.guild.id,':warning: **Вы не являетесь Владельцем данного сервера!**')}",
                    color=0xFCC21B,
                )
                await ctx.send(embed=embed, ephemeral=True)
                ctx.command.reset_cooldown(ctx)


def setup(client):
    client.add_cog(class_rselect(client))
