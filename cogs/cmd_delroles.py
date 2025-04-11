import disnake as discord

# import word
# import config
# from discord import utils
from disnake.ext import commands
from helper import *
from cache import *


class class_delroles(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Удаление спам ролей
    @commands.slash_command(
        name="delroles", description="Removing spam roles | Удаление спам ролей"
    )
    @commands.bot_has_permissions(manage_messages=True, manage_roles=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def delroles(
        self,
        inter,
        *,
        role: discord.Role = commands.Param(
            name="role",
            description="Specify the role or its ID | Укажите роль или её ID",
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
                if role is not None:
                    success = 0
                    fail = 0
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:b_loading:857131960223662104> Пожалуйста подождите, идет процесс удаления ролей...')}",
                        color=0xF4900C,
                    )
                    await ctx.send(embed=embed, ephemeral=True)
                    for i in ctx.guild.roles:
                        if i.name == f"{role.name}":
                            try:
                                await i.delete()
                                success += 1
                            except:
                                fail += 1
                    if not success == 0 and success + fail > success:
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,':warning: Не все спам роли')} **{role.name}** {get_language(ctx.guild.id,'удалены!')}\n\n{get_language(ctx.guild.id,'Удалено')} ` {success} ` {get_language(ctx.guild.id,'из')} ` {success+fail} `",
                            color=0xFCC21B,
                        )
                        await ctx.edit_original_message(embed=embed)
                    elif success + fail == success:
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,'<a:vega_check_mark:821700784927801394> Спам роли')} **{role.name}** {get_language(ctx.guild.id,'успешно удалены!')}\n\n{get_language(ctx.guild.id,'Удалено')} ` {success} ` {get_language(ctx.guild.id,'из')} ` {success+fail} `",
                            color=0x43B581,
                        )
                        await ctx.edit_original_message(embed=embed)
                    else:
                        embed = discord.Embed(
                            description=f"{get_language(ctx.guild.id,'<a:vega_x:810843492266803230> Я не смог удалить роль')} {role.mention}.\n— {get_language(ctx.guild.id,'Видимо моя роль находится ниже роли')} {role.mention}.\n\n{get_language(ctx.guild.id,'Удалено')} ` {success} ` {get_language(ctx.guild.id,'из')} ` {success+fail} `",
                            color=0xCC1A1D,
                        )
                        await ctx.edit_original_message(embed=embed)
                        ctx.command.reset_cooldown(ctx)
                else:
                    embed = discord.Embed(
                        description=f"{get_language(ctx.guild.id,'<a:loupe:811137886141153320> Укажите спам роль!')}",
                        color=0x8899A6,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Описание:')}",
                        value=f"{get_language(ctx.guild.id,'Бот начнет удалять роли с одинаковым названием.')}",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Аргумены:')}",
                        value=f"`{get_language(ctx.guild.id,'{название роли}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{@роль}')}` {get_language(ctx.guild.id,'или')} `{get_language(ctx.guild.id,'{ID роли}')}`",
                        inline=False,
                    )
                    embed.add_field(
                        name=f"{get_language(ctx.guild.id,'Пример:')}",
                        value=f"{ctx.prefix}delroles {get_language(ctx.guild.id,'@роль')}",
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
    client.add_cog(class_delroles(client))
